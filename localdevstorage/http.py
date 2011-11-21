from django.core.exceptions import ImproperlyConfigured
import os
import urllib2

from django.conf import settings

from localdevstorage.base import BaseStorage

class HttpStorage(BaseStorage):
    def __init__(self, location=None, base_url=None, fallback_url=None):
        self.fallback_url = fallback_url or getattr(settings, 'LOCALDEVSTORAGE_HTTP_FALLBACK_URL')
        if not self.fallback_url:
            raise ImproperlyConfigured('please define LOCALDEVSTORAGE_HTTP_FALLBACK_URL in your settings')
        super(BaseStorage, self).__init__(location, base_url)

    def _exists(self, name):
        request = urllib2.Request(self._path(name))
        request.get_method = lambda : 'HEAD'
        response = urllib2.urlopen(request)
        return response.code == 200

    def _path(self, name):
        return self.fallback_url + name

    def _get(self, name):
        request = urllib2.Request(self._path(name))
        response = urllib2.urlopen(request)
        if response.code != 200:
            raise IOError()
        dirname = os.path.dirname(self.path(name))
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        f = open(self.path(name), mode='wb')
        f.write(response.read())