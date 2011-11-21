from django.core.files.storage import FileSystemStorage

class BaseStorage(FileSystemStorage):
    def _open(self, name, mode='rb'):
        try:
            return super(BaseStorage, self)._open(name, mode)
        except IOError:
            try:
                self._get(name)
                return super(BaseStorage, self)._open(name, mode)
            except Exception:
                pass
            raise

    def exists(self, name):
        if super(BaseStorage, self).exists(name):
            return True
        return self._exists(name)
