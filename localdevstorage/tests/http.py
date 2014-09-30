from django.conf import settings
from unittest import TestCase

from localdevstorage.http import HttpStorage

settings.configure(
    LOCALDEVSTORAGE_HTTP_FALLBACK_DOMAIN='https://github.com/piquadrat/django-localdevstorage/blob/master/localdevstorage/'
)

class HttpStorageTest(TestCase):
        def setUp(self):
            self.storage = HttpStorage(base_url=settings.LOCALDEVSTORAGE_HTTP_FALLBACK_DOMAIN, location='./localdevstorage/')

        def test_http_fallback(self):
            self.f = self.storage.open('base.py')
            self.assertIn('BaseStorage', self.f.read())

        def tearDown(self):
            self.storage.delete('base.py')