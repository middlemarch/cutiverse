from __future__ import unicode_literals, absolute_import

# Standard Library
import logging
import multiprocessing
import random

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
    method_whitelist=['HEAD', 'GET', 'PUT', 'POST', 'PATCH', 'DELETE']
)

# Instantiate a 'global' HTTPAdapter to allow connection pooling.
adapter = HTTPAdapter(
    pool_connections=100,
    pool_maxsize=100,
    max_retries=retry_strategy,
)


class BaseSearchBackend(object):

    def __init__(self, search_obj):
        # Setup a requests session
        self.session = Session()
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.threads = multiprocessing.cpu_count()

        # Add a fake header
        self.session.headers.update({
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                ' (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
            )
        })

        self.search_obj = search_obj

    @staticmethod
    def is_good(url):
        """Ensure given URL doesn't contain uncute language."""
        if BAD_URL_RE.match(url):
            return False
        return True

    def get_links(self):
        raise NotImplementedError

    @property
    def good_urls(self):
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
