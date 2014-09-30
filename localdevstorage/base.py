import os

from django.core.files.storage import FileSystemStorage


class BaseStorage(FileSystemStorage):
    def _open(self, name, mode='rb'):
        try:
            return super(BaseStorage, self)._open(name, mode)
        except IOError:
            try:
                f = self._get(name)
                self._write(f, name)
                return super(BaseStorage, self)._open(name, mode)
            except Exception:
                pass
            raise

    def _exists_locally(self, name):
        return super(BaseStorage, self).exists(name)

    def exists(self, name):
        if self._exists_locally(self):
            return True
        return self._exists_upstream(name)

    def _write(self, filelike, name):
        dirname = os.path.dirname(self.path(name))
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        f = open(self.path(name), mode='wb')
        f.write(filelike.read())

    def _fetch_local(self, name, force=False):
        if self._exists_locally(name) and not force:
            return

        return self._write(self._get(name), name)
