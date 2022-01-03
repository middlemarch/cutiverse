# Standard
import logging
import random
import sys
import webbrowser

# Project
from dopameme.search import SearchObj
from dopameme.backends.yandex import YandexBackend

LOG = logging.getLogger(__name__)
LOG_LEVEL = "INFO"  # Log output level


def run(**kwargs):
    """Find and open a cute link."""
    noun = kwargs.get("noun", None)
    search_obj = SearchObj(noun=noun)

    LOG.info("Search Terms: #y<%s>", search_obj.display_str)

    search_backend = YandexBackend(search_obj)
    good_links = search_backend.good_urls

    if not good_links:
        LOG.error("#r<Ran out of links to try>")
        sys.exit(1)
    else:
        link_url = good_links[random.randint(0, len(good_links) - 1)]
        LOG.debug("Opening #g<%s>", link_url)
        webbrowser.open_new_tab(link_url)
