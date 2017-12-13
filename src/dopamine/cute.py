from __future__ import unicode_literals

# Standard Library
import json
import logging
import random
import sys
import uuid
import webbrowser

# Third Party
import requests

# Project
from dopamine.constants import (
    ADJECTIVES,
    NOUNS,
    MODIFIERS,
    EXCLUDE,
    BAD_URL_RE,
    JSON_RE,
)
from dopamine.testlib import TestUrl

LOG = logging.getLogger(__name__)
LOG_LEVEL = 'INFO'  # Log output level


def _good(url):
    """Ensure given URL doesn't contain uncute language."""
    if BAD_URL_RE.match(url):
        return False
    return True

def run(**kwargs):
    """Find and open a cute link."""
    image_only = kwargs.get('image_only', False)
    threads = kwargs.get('threads', 8)
    noun = kwargs.get('noun', None)

    # Randomly select an index for each type
    adjective_idx = random.randint(0, len(ADJECTIVES) - 1)
    noun_idx = random.randint(0, len(NOUNS) - 1)
    modifier_idx = random.randint(0, len(MODIFIERS) - 1)

    # Initial search terms
    term_list = ADJECTIVES[adjective_idx].split(' ')

    # Add in noun or randomly select one from list
    if noun:
        term_list.extend(noun.split(' '))
    else:
        term_list.extend(NOUNS[noun_idx].split(' '))

    # Add a modifier (sometimes)
    add_modifier = bool(random.randint(0, 1))
    if add_modifier:
        term_list.extend(MODIFIERS[modifier_idx].split(' '))

    LOG.info('Search Terms: #y<%s>', ' '.join(term_list))

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
        'q': ' '.join(term_list),
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
    LOG.debug('Search URL: #y<%s>', SEARCH_URL)

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
    LOG.debug('Links: %s', '\n'.join(link_map.values()))

    # Randomly select some links and test them in parallel
    good_links = []  # Global link list (appending to lists is threadsafe)
    while True:
        thread_pool = []  # Track all running threads to join to later
        for item in range(threads):
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
        LOG.error('#r<Ran out of links to try>')
        sys.exit(1)
    else:
        link_url = good_links[random.randint(0, len(good_links) - 1)]
        if image_only:
            LOG.info('Image Source: #g<%s>', link_map[link_url])
            LOG.debug('Opening #g<%s>', link_url)
            webbrowser.open(link_url)
        else:
            LOG.info('Image Only Link: #g<%s>', link_url)
            LOG.debug('Opening #g<%s>', link_url)
            webbrowser.open_new_tab(link_map[link_url])
