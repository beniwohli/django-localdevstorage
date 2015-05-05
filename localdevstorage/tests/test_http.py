import os
import shutil

from django.conf import settings
from django.test import TestCase

from localdevstorage.http import HttpStorage

import responses

DOMAIN = 'https://example.com'


class HttpStorageTest(TestCase):
    def tearDown(self):
        test_dir = os.path.join(settings.TEST_DIR, 'foo')
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


    @responses.activate
    def test_http_fallback(self):
        responses.add(
            responses.GET,
            DOMAIN + '/foo/test_fallback',
            body='foo', status=200,
            content_type='text/plain'
        )
        storage = HttpStorage(fallback_domain=DOMAIN)
        f = storage.open('foo/test_fallback')
        self.assertIn('foo', str(f.read()))
        assert len(responses.calls) == 1

    @responses.activate
    def test_exists(self):
        responses.add(
            responses.HEAD,
            DOMAIN + '/foo/test_exists',
            body='foo', status=200,
            content_type='text/plain'
        )
        responses.add(
            responses.HEAD,
            DOMAIN + '/foo/test_does_not_exist',
            body='foo', status=404,
            content_type='text/plain'
        )
        storage = HttpStorage(fallback_domain=DOMAIN)
        self.assertTrue(storage.exists('foo/test_exists'))
        self.assertFalse(storage.exists('foo/test_does_not_exist'))

    @responses.activate
    def test_http_auth(self):
        responses.add(
            responses.GET,
            DOMAIN + '/foo/test_auth',
            body='foo', status=200,
            content_type='text/plain'
        )
        with self.settings(
                LOCALDEVSTORAGE_HTTP_PASSWORD='pw',
                LOCALDEVSTORAGE_HTTP_USERNAME='user'
        ):
            storage = HttpStorage(fallback_domain='https://example.com')
        f = storage.open('foo/test_auth')
        self.assertIn('Authorization', responses.calls[0].request.headers)
