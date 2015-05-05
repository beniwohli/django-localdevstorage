======================
django-localdevstorage
======================

.. image:: https://travis-ci.org/piquadrat/django-localdevstorage.svg?branch=master
    :target: http://travis-ci.org/piquadrat/django-localdevstorage

.. image:: https://coveralls.io/repos/piquadrat/django-localdevstorage/badge.svg?branch=master
    :target: https://coveralls.io/r/piquadrat/django-localdevstorage?branch=master

.. image:: https://img.shields.io/pypi/v/django-localdevstorage.svg
    :target: https://pypi.python.org/pypi/django-localdevstorage/

django-localdevstorage is a set of storage backends that helps during
development. Instead of having to copy all user generated media from
the live site for local development, the storage backends provided by
django-localdevstorage will download media files that are not available
locally "on demand".

Installation
============

Set one of the provided storage backends in your ``settings.py``. These
are:

    * HTTP: ``DEFAULT_FILE_STORAGE = 'localdevstorage.http.HttpStorage'``
    * (more will follow)

.. note::
    If you use `django-filer`_ 0.9 or higher, you have to make sure that
    ``localdevstorage`` is *not* used as the thumbnail storage, e.g. by
    adding this to your settings::

        FILER_STORAGES = {
            'public': {
                'thumbnails': {
                    'ENGINE': 'django.core.files.storage.FileSystemStorage',
                    'OPTIONS': {},
                    'THUMBNAIL_OPTIONS': {
                        'base_dir': 'filer_public_thumbnails',
                    },
                },
            },
        }


HTTP
----

Set the fallback domain that should be used to fetch missing files. This
is usually the protocol (http or https) and the domain your live site::

    LOCALDEVSTORAGE_HTTP_FALLBACK_DOMAIN = 'http://www.example.com/'

.. note::
    Earlier versions of this library used ``LOCALDEVSTORAGE_HTTP_FALLBACK_URL``.
    While this still works, it is recommended to update your settings to the
    new name. ``LOCALDEVSTORAGE_HTTP_FALLBACK_URL`` will be removed in a future
    version.

If your server is secured with HTTP basic auth, you can provide a username and
password::

    LOCALDEVSTORAGE_HTTP_USERNAME = 'foo'
    LOCALDEVSTORAGE_HTTP_PASSWORD = 'bar'

SFTP
----

There are three settings that need to be configured for the SFTP backend:

 * ``LOCALDEVSTORAGE_SFTP_USER``
 * ``LOCALDEVSTORAGE_SFTP_HOST``
 * ``LOCALDEVSTORAGE_SFTP_ROOT_PATH``: this should be the ``MEDIA_ROOT``
   on the remote machine in most cases.

.. note::
    * The SFTP backend is much slower than the HTTP backend, which you should
      use in most cases. The SFTP backend is only really useful if your
      media files are not directly accessible through unauthenticated HTTP.
    * because the SFTP backend can't prompt for a password, make sure that
      a connection can be established through public key exchange.

.. warning::
    Although we took special care not to do anything destructive on the
    remote machine, bugs in our code or in upstream libraries can always
    happen. This alone should be reason enough to use the HTTP backend in
    almost all cases, since it is, by definition, read only.

Caveats
=======

 * Since django-localdevstorage extends a Django storage backend
   (``FileSystemStorage`` to be precise), only code that uses Django's
   file storage abstraction works with django-localdevstorage. Code that
   bypasses Django and accesses files directly will not benefit.


.. _django-filer: https://github.com/stefanfoulis/django-filer
