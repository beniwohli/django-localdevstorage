Changelog
=========

0.1
---

First release with HTTP backend

0.2
---

 * SFTP backend, code mostly lifted from the SFTP backend from django-storages
 * fixed a bug that made it impossible to upload new files when using the dev storage

0.3
---
 * use the right way (tm) to calculate the URL of the remote file. This includes
   a switch from ``LOCALDEVSTORAGE_HTTP_FALLBACK_URL`` to
   ``LOCALDEVSTORAGE_HTTP_FALLBACK_DOMAIN``. The former will be removed in a
   future version, probably 0.4.

