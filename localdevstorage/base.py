import os
from django.core.files.storage import FileSystemStorage

try:
    FileNotFoundError
except:
    FileNotFoundError = IOError


class BaseStorage(FileSystemStorage):
    def _open(self, name, mode='rb'):
        try:
            return super(BaseStorage, self)._open(name, mode)
        except FileNotFoundError:
            if 'w' in mode: # if writing, make sure the parent structure exists
                self._ensure_directory(name)

            try:
                try:
                    f = self._get(name)
                except IOError:
                    # if the underlying file doesn't exist, no matter.
                    pass
                else:
                    # if it does, write the contents locally
                    self._write(f, name)

            except Exception:
                pass
        return super(BaseStorage, self)._open(name, mode)

    def _exists_locally(self, name):
        return super(BaseStorage, self).exists(name)

    def exists(self, name):
        if self._exists_locally(name):
            return True
        return self._exists_upstream(name)

    def _ensure_directory(self, name):
        dirname = os.path.dirname(self.path(name))
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def _write(self, filelike, name):
        self._ensure_directory(name)
        f = open(self.path(name), mode='wb')
        f.write(filelike.read())

    def _fetch_local(self, name, force=False):
        if self._exists_locally(name) and not force:
            return

        return self._write(self._get(name), name)
