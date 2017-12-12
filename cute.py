# Standard Library
import json
import logging
import random
import re
import sys
import threading
import uuid
import webbrowser

# Request Library
import requests

LOG = logging.getLogger(__name__)
IMAGE_ONLY = True
THREADS = 8  # Threads to use when checking URLS
LOG_LEVEL = 'INFO'  # Log output level
ADJECTIVES = (
    'adorable',
    'aegyo',
    'baby',
    'charming',
    'cute',
    'darling',
    'kawaii',
    'little',
    'snuggly',
    'sweet',
    'tiny',
)
"""Search term - adjectives."""

NOUNS = (
    'alpaca',
    'axolotl',
    'baby duck',
    'baby sloth',
    'bear',
    'bird',
    'birdy',
    'bunny',
    'cat',
    'deer',
    'doe',
    'dog',
    'doggie',
    'dolphin',
    'duckling',
    'echidna',
    'fawn',
    'frog',
    'hampster',
    'harp seal',
    'hedgehog',
    'junco',
    'kitten',
    'kitty',
    'koala',
    'newt',
    'owl',
    'pangolin',
    'piggy',
    'puppy',
    'quokka',
    'rabbit',
    'raccoon',
    'seal',
    'squirrel',
    'turtle',
    'wolf pup',
    'wolf',
)
"""Search term - nouns."""

MODIFIERS = (
    'cuddle',
    'cuddling',
    'hat',
    'house',
    'playing',
    'sleeping',
    'wearing onesie',
)
"""Optional search terms - modifiers."""

EXCLUDE = (
    '-disgusting',
    '-gross',
    '-icky',
    '-poop',
    '-porn',
    '-sexy',
    '-shit',
    '-ugly',
    '-xxx',
)
"""Terms to exclude from searches"""

# Strings that shouldn't appear in any URLs:
URL_EXCLUDE = (
    '?show_error=true',
    'google.com/search',
    'redtube',
    'teepublic',
    'tube8',
    'xnxx',
    'xxx',
    'youporn',
    'zillow',
)
"""Url substrings to exlude."""

RE_STR = r'^.+?({0}).+?'.format('|'.join([re.escape(x) for x in URL_EXCLUDE]))
"""All bad url data concatenated into a regular expression strings."""

BAD_URL_RE = re.compile(RE_STR)
"""Compiled regular expression of bad url substrings."""

# LINK_RE = re.compile(r'["]ou["]: ?["](https?.+?)["].*?')
# """Regex to find destination links in image results."""

# ORIG_LINK_RE = re.compile(r'["]ru["]: ?["](https?.+?)["].*?')
# """Regex to find destination links in image results."""

# JSON_RE = re.compile(r'{ ?["] ?.+? ?["] ?}')
JSON_RE = re.compile(r'{.+?}')
"""Regex to find JSON in page."""


def _good(url):
    """Ensure given URL doesn't contain uncute language."""
    if BAD_URL_RE.match(url):
        return False
    return True


class TestUrl(threading.Thread):

    def __init__(self, url, url_list, *args, **kwargs):
        """
        Test a url.

        This works by being given a URL and a list to add the URL to if the url
        checks out as a good one. This class is executed as a thread but
        appending to a list is thread safe; all TestUrl threads are given the
        same list instance to append to.
        """
        self.url = url
        self.url_list = url_list
        self.session = requests.Session()
        super(TestUrl, self).__init__(*args, **kwargs)

    def run(self):
        """Execute the thread."""
        LOG.debug('Testing "%s"', self.url)
        try:
            r = self.session.head(self.url)
        except Exception:
            pass  # Probably a bad url yo
        else:
            if r.status_code == 200:
                if r.url == self.url:
                    self.url_list.append(r.url)
                else:
                    redirect_url = r.url
                    LOG.debug(u'%s redirects to %s', self.url, redirect_url)
                    try:
                        r = self.session.head(redirect_url)
                    except Exception:
                        pass  # A bad url
                    else:
                        if r.status_code == 200:
                            self.url_list.append(redirect_url)


def run():
    """Find and open a cute link."""

    # Randomly select an index for each type
    adjective_idx = random.randint(0, len(ADJECTIVES) - 1)
    noun_idx = random.randint(0, len(NOUNS) - 1)
    modifier_idx = random.randint(0, len(MODIFIERS) - 1)

    # Initial search terms
    term_list = ADJECTIVES[adjective_idx].split(' ')

    # Add in nouns
    term_list.extend(NOUNS[noun_idx].split(' '))

    # Add a modifier (sometimes)
    add_modifier = bool(random.randint(0, 1))
    if add_modifier:
        term_list.extend(MODIFIERS[modifier_idx].split(' '))

    LOG.info(u'Search Terms: "%s"', ' '.join(term_list))

    # Add some terms that exclude uncute things
    term_list.extend(EXCLUDE)

    # Setup a requests session and retrieve the search url
    s = requests.Session()

    # Add a fake header
    s.headers.update({
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
        )
    })

    # Retrieve search results
    r = s.get('https://www.google.com/search', params={
        'q': u' '.join(term_list),
        'sa': 'X',
        'biw': '600',
        'bih': '800',
        'tbm': 'isch',
        'ijn': 1 / 1,
        'start': 1,
        'tbs': 'isz:lt,islt:svga',
        'ei': uuid.uuid4().hex,  # Unique id (avoid google ban hammer)
    })
    SEARCH_URL = r.history[0].url if r.history else r.url

    # Display search url:
    LOG.debug(u'Search URL: %s', SEARCH_URL)

    link_map = {}
    for item in JSON_RE.findall(r.text):
        try:
            d = json.loads(item)
        except Exception:
            continue  # Skip unparsable
        else:
            source_url = d.get('ru')
            dest_url = d.get('ou')
            if source_url and dest_url:
                if not _good(source_url):
                    continue
                link_map[dest_url] = source_url

    # Copy the link keys
    links = link_map.keys()[:]
    LOG.debug(u'Links: %s', '\n'.join(link_map.values()))

    # Randomly select some links and test them in parallel
    good_links = []  # Global link list (appending to lists is threadsafe)
    while True:
        thread_pool = []  # Track all running threads to join to later
        for item in range(THREADS):
            if not links:
                break
            link_idx = random.randint(0, len(links) - 1)
            try:
                url = links.pop(link_idx)
            except IndexError:
                continue

            t = TestUrl(url, good_links)
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

    if not good_links:
        LOG.info(u'Ran out of links to try')
        sys.exit(1)
    else:
        link_url = good_links[random.randint(0, len(good_links) - 1)]
        if IMAGE_ONLY:
            LOG.info('Image Source: "%s"', link_map[link_url])
            LOG.debug(u'Opening {0}'.format(link_url))
            webbrowser.open(link_url)
        else:
            LOG.info('Image Only Link: "%s"', link_url)
            LOG.debug(u'Opening {0}'.format(link_url))
            webbrowser.open(link_map[link_url])


if __name__ == "__main__":
    logger = logging.getLogger("__main__")
    handler = logging.StreamHandler()
    handler.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(
        "%(levelname)8s - %(asctime)15s %(message)s %(name)s:%(lineno)s",
        "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)

    run()
    sys.exit(0)
