import urllib2
import urlparse
import warnings

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from localdevstorage.base import BaseStorage


class HttpStorage(BaseStorage):
    def __init__(self, location=None, base_url=None, fallback_url=None, fallback_domain=None):
        self.fallback_url = fallback_url or getattr(settings, 'LOCALDEVSTORAGE_HTTP_FALLBACK_URL', None)
        if self.fallback_url:
            warnings.warn('fallback_url and LOCALDEVSTORAGE_HTTP_FALLBACK_URL have been replaced by fallback_domain and LOCALDEVSTORAGE_HTTP_FALLBACK_DOMAIN, respectively, and will be removed in a future release.')
        self.fallback_domain = fallback_domain or getattr(settings, 'LOCALDEVSTORAGE_HTTP_FALLBACK_DOMAIN', None)
        if not (self.fallback_url or self.fallback_domain):
            raise ImproperlyConfigured('please define LOCALDEVSTORAGE_HTTP_FALLBACK_DOMAIN in your settings')
        super(BaseStorage, self).__init__(location, base_url)

    def _exists(self, name):
        request = HeadRequest(self._path(name))
        try:
            response = urllib2.urlopen(request)
            return response.code == 200
        except Exception:
            return False

    def _path(self, name):
        if self.fallback_domain:
            return urlparse.urljoin(self.fallback_domain, self.url(name))
        return self.fallback_url + name

    def _get(self, name):
        request = urllib2.Request(self._path(name))
        response = urllib2.urlopen(request)
        if response.code != 200:
            raise IOError()
        return response


class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"
