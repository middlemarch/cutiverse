# Standard
import logging
import threading

LOG = logging.getLogger(__name__)


class TestUrl(threading.Thread):
    def __init__(self, session, url, url_list, *args, **kwargs):
        """
        Test a url.

        This works by being given a URL and a list to add the URL to if the url
        checks out as a good one. This class is executed as a thread but
        appending to a list is thread safe; all TestUrl threads are given the
        same list instance to append to.
        """
        self.url = url
        self.url_list = url_list
        self.session = session
        super().__init__(*args, **kwargs)

    def run(self):
        """Execute the thread."""
        LOG.debug("Testing #y<%s>", self.url)
        try:
            r = self.session.head(self.url, timeout=0.5)
        except Exception:
            pass  # Probably a bad url yo
        else:
            if r.status_code == 200:
                if r.url == self.url:
                    self.url_list.append(r.url)
                else:
                    redirect_url = r.url
                    LOG.debug("#y<%s> redirects to #y<%s>", self.url, redirect_url)
                    try:
                        r = self.session.head(redirect_url)
                    except Exception:
                        pass  # A bad url
                    else:
                        if r.status_code == 200:
                            self.url_list.append(redirect_url)
