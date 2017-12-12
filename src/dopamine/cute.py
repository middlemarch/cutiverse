# Standard Library
import json
import logging
import random
import sys
import threading
import uuid
import webbrowser

# Request Library
import requests

# Project
from dopamine.constants import (
    THREADS,
    ADJECTIVES,
    NOUNS,
    MODIFIERS,
    EXCLUDE,
    BAD_URL_RE,
    JSON_RE,
)

LOG = logging.getLogger(__name__)
LOG_LEVEL = 'INFO'  # Log output level


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


def run(image_only=False):
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
        if image_only:
            LOG.info('Image Source: "%s"', link_map[link_url])
            LOG.debug(u'Opening {0}'.format(link_url))
            webbrowser.open(link_url)
        else:
            LOG.info('Image Only Link: "%s"', link_url)
            LOG.debug(u'Opening {0}'.format(link_url))
            webbrowser.open(link_map[link_url])
