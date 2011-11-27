======================
django-localdevstorage
======================

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

HTTP
----

Set the fallback URL that should be used to fetch missing files. This
is usually the domain and ``MEDIA_URL`` of your live site::

    LOCALDEVSTORAGE_HTTP_FALLBACK_URL = 'http://www.example.com/media/'

.. note::
    Make sure to include the trailing slash. No errors or warnings will
    be raised if your media files can't be found.

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

