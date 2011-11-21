from django.test import TestCase

from localdevstorage.http import HttpStorage


class HttpStorageTest(TestCase):
        def setUp(self):
            self.storage = HttpStorage(fallback_url='https://github.com/piquadrat/django-localdevstorage/blob/master/localdevstorage/')

        def test_http_fallback(self):
            self.f = self.storage.open('base.py')
            self.assertIn('BaseStorage', self.f.read())

        def tearDown(self):
            self.storage.delete('base.py')