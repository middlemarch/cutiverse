# Standard
import logging
import re
import uuid

# Project
from dopameme.backends.base import BaseSearchBackend

LOG = logging.getLogger(__name__)
URL_RE = re.compile(r"{\"url\"\:\"https?://[^\"]+[.](?:jpg|jpeg|png|webp|gif|tiff)\"")


class YandexBackend(BaseSearchBackend):
    def get_links(self):
        # Retrieve search results
        r = self.session.get(
            "https://yandex.com/images/search",
            params={
                "text": self.search_obj.default_str,
            },
        )
        SEARCH_URL = r.history[0].url if r.history else r.url

        # Display search url:
        LOG.debug("Search URL: #y<%s>", SEARCH_URL)

        url_vals = URL_RE.findall(r.text)

        # Cleanup by trimming {"url": from found values start and " from the values end
        url_list = [x[8:-1] for x in url_vals]

        # Remove bad url values from the found list
        return [x for x in url_list if self.is_good(x)]
