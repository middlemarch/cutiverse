# Standard
import logging
import re
import sys
import uuid
from typing import List

# Project
from dopameme.backends.base import BaseSearchBackend

LOG = logging.getLogger(__name__)
URL_RE = re.compile(r"{\"url\"\:\"https?://[^\"]+[.](?:jpg|jpeg|png|webp|gif|tiff)\"")


class DuckDuckGo(BaseSearchBackend):
    def get_links(self) -> List[str]:
        # Retrieve search results
        LOG.info("Obtaining search token...")
        res = self.session.get(
            "https://duckduckgo.com/",
            params={
                "q": self.search_obj.default_str,
            },
        )
        match = re.search(r"vqd=([\d-]+)\&", res.text, re.M | re.I)
        try:
            token = match.groups(1)
        except Exception:
            LOG.error("Unable to obtain search token from DuckDuckGo.com")
            sys.exit(1)
        LOG.debug("Search Token: #c<%s>", token[0])

        search_endpoint = "https://duckduckgo.com/i.js"
        params = {
            "l": "us-en",
            "o": "json",
            "q": self.search_obj.default_str,
            "vqd": token[0],
            "p": "1",
        }
        search_results = self.session.get(search_endpoint, params=params)
        LOG.debug("Search URL: #y<%s>", search_results.request.url)
        try:
            response_data = search_results.json()
        except Exception:
            LOG.error("Error getting search results: #r<%s>", search_results.text)
            sys.exit(1)

        is_good = self.is_good  # Stash to avoid repeated attibute lookups

        # Test all the search results
        url_list = []
        for result in search_results.json().get("results", []):
            image_url = result.get("image", None)
            height = result.get("height", None)
            width = result.get("width", None)

            # Image has valid URL
            if not image_url:
                LOG.debug("Result #y<%s> has no 'image' key", result)
                continue
            if not is_good(image_url):
                LOG.debug("Skipping #y<%s> because it has values we want to exclude", image_url)

            if height and height < 512:
                LOG.debug("Skipping small image: #y<%s (%s x %s)>", image_url, width, height)
                continue
            if width and width < 512:
                LOG.debug("Skipping small image: #y<%s (%s x %s)>", image_url, width, height)
                continue

            try:
                url_list.append(result["image"])
            except KeyError:
                LOG.debug("Result %s has no 'image' key", result)

        return url_list
