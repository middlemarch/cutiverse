# Standard
import logging
import multiprocessing
import random
from urllib.parse import urlparse
from typing import List

# Third Party
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Project
from dopameme.constants import BAD_URL_RE
from dopameme.testlib import TestUrl

LOG = logging.getLogger(__name__)


retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 408, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "PUT", "POST", "PATCH", "DELETE"],
)

# Instantiate a 'global' HTTPAdapter to allow connection pooling.
adapter = HTTPAdapter(
    pool_connections=100,
    pool_maxsize=100,
    max_retries=retry_strategy,
)


USER_AGENTS: List[str] = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/605.1.15 Edg/96.0.1054.62",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/605.1.15",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (X11; Ubuntu; Arch x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
]


def get_user_agent() -> str:
    """Generate a pseudo-random user agent string to avoid ban hammers."""

    agent_idx = random.randint(0, len(USER_AGENTS) - 1)
    agent = USER_AGENTS[agent_idx]

    if "AppleWebKit/537.36" in agent:
        new_major = random.randint(400, 800)
        new_minor = random.randint(1, 99)
        agent = agent.replace("AppleWebKit/537.36", f"AppleWebKit/{new_major}.{new_minor}")

    if "Chrome/96.0.4664.110" in agent:
        new_major = random.randint(60, 99)
        new_minor = random.randint(0, 100)
        new_patch = random.randint(1000, 5000)
        new_release = random.randint(100, 500)
        agent = agent.replace("Chrome/96.0.4664.110", f"Chrome/{new_major}.{new_minor}.{new_patch}.{new_release}")

    if "Firefox/95.0" in agent:
        new_major = random.randint(90, 200)
        new_minor = random.randint(0, 100)
        agent = agent.replace("Firefox/95.0", f"Firefox/{new_major}.{new_minor}")
        if "rv:95.0" in agent:
            agent = agent.replace("rv:95.0", f"rv:{new_major}.{new_minor}")

    if "Safari/605.1.15" in agent:
        new_major = random.randint(500, 900)
        new_minor = random.randint(0, 100)
        new_patch = random.randint(0, 100)
        agent = agent.replace("Safari/605.1.15", f"Safari/{new_major}.{new_minor}.{new_patch}")

    if "Edg/96.0.1054.62" in agent:
        new_major = random.randint(60, 99)
        new_minor = random.randint(0, 100)
        new_patch = random.randint(1000, 5000)
        new_release = random.randint(100, 500)
        agent = agent.replace("Edg/96.0.1054.62", f"Edg/{new_major}.{new_minor}.{new_patch}.{new_release}")

    if "Gecko/20100101" in agent:
        year = random.randint(1999, 2200)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        agent = agent.replace("Gecko/20100101", f"Gecko/{year}{month:02d}{day:02d}")

    return agent


class BaseSearchBackend:
    def __init__(self, search_obj):
        # Setup a requests session
        self.session = Session()
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        threads = multiprocessing.cpu_count()
        if threads > 8:
            self.threads = 8  # Don't use an insane number, it looks suspicious
        else:
            self.threads = threads

        self.user_agent = get_user_agent()  # Get a random new useragent string every time
        LOG.debug("Using user agent string: %s", self.user_agent)

        # Add a fake header
        self.session.headers.update({"User-Agent": self.user_agent})

        self.search_obj = search_obj

    @staticmethod
    def is_good(url) -> bool:
        """Ensure given URL doesn't contain uncute language and is valid."""
        if BAD_URL_RE.match(url):
            return False
        try:
            parsed_url = urlparse(url)
        except Exception:
            LOG.debug("Ignoring invalid url %s", url)
            return False
        if parsed_url.scheme not in ("http", "https"):
            LOG.debug("Ignoring url with invalid scheme %s", url)
            return False
        return True

    def get_links(self) -> List[str]:
        raise NotImplementedError

    @property
    def good_urls(self) -> List[str]:
        """Return a list of good tested urls."""
        links = [x for x in self.get_links() if self.is_good(x)]

        # Randomly select some links and test them in parallel
        good_links = []  # Global link list (appending to lists is threadsafe)
        while True:
            thread_pool = []  # Track all running threads to join to later
            for item in range(self.threads):
                if not links:
                    break
                link_idx = random.randint(0, len(links) - 1)
                try:
                    url = links.pop(link_idx)
                except IndexError:
                    continue

                t = TestUrl(self.session, url, good_links)
                t.start()
                thread_pool.append(t)

            # Block until all checks are finished
            for t in thread_pool:
                t.join()
            if good_links:
                break
            else:
                if not links:
                    break  # We ran out of links to try
        return good_links
