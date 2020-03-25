from __future__ import unicode_literals, absolute_import

# Standard
import logging
import uuid

# Project
from dopameme.backends.base import BaseSearchBackend
from dopameme.constants import GOOGLE_IMG_RE

LOG = logging.getLogger(__name__)


class GoogleBackend(BaseSearchBackend):

    def get_links(self):
        # Retrieve search results
        r = self.session.get('https://www.google.com/search', params={
            'q': self.search_obj.default_str,
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

        return [x for x in GOOGLE_IMG_RE.findall(r.text) if self.is_good(x)]
