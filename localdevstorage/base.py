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
            try:
                f = self._get(name)
                self._write(f, name)
                return super(BaseStorage, self)._open(name, mode)
            except FileNotFoundError:
                pass
            raise

    def exists(self, name):
        if super(BaseStorage, self).exists(name):
            return True
        return self._exists(name)

    def _write(self, filelike, name):
        dirname = os.path.dirname(self.path(name))
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        f = open(self.path(name), mode='wb')
        f.write(filelike.read())
