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

Caveats
=======

 * Since django-localdevstorage extends a Django storage backend
   (``FileSystemStorage`` to be precise), only code that uses Django's
   file storage abstraction works with django-localdevstorage. Code that
   bypasses Django and accesses files directly will not benefit.
 * Currently, only one backend is provided. A second one using SSH is
   planned.




