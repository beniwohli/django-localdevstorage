# This is mostly lifted from django-storages' sftp backend: Their license:
#
# SFTP storage backend for Django.
# Author: Brent Tubbs <brent.tubbs@gmail.com>
# License: MIT
#
# Modeled on the FTP storage by Rafal Jonca <jonca.rafal@gmail.com>
from __future__ import print_function
try:
    import ssh
except ImportError:
    import paramiko as ssh

import os
import posixpath
from django.conf import settings
from django.core.files.base import File
try:
    from io import StringIO
except ImportError:
    # Python 2 fallbacks
    from cStringIO import StringIO

from localdevstorage.base import BaseStorage


class SftpStorage(BaseStorage):
    def __init__(self, location=None, base_url=None, user=None, host=None, root_path=None):
        self._host = host or settings.LOCALDEVSTORAGE_SFTP_HOST
        self._root_path = root_path or settings.LOCALDEVSTORAGE_SFTP_ROOT_PATH

        # if present, settings.SFTP_STORAGE_PARAMS should be a dict with params
        # matching the keyword arguments to paramiko.SSHClient().connect().  So
        # you can put username/password there.  Or you can omit all that if
        # you're using keys.
        self._params = getattr(settings, 'SFTP_STORAGE_PARAMS', {})
        self._params['username'] = user or settings.LOCALDEVSTORAGE_SFTP_USER

        # for now it's all posix paths.  Maybe someday we'll support figuring
        # out if the remote host is windows.
        self._pathmod = posixpath
        super(SftpStorage, self).__init__(location, base_url)

    def _connect(self):
        self._ssh = ssh.SSHClient()

        # automatically add host keys from current user.
        self._ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))

        # and automatically add new host keys for hosts we haven't seen before.
        self._ssh.set_missing_host_key_policy(ssh.AutoAddPolicy())

        try:
            self._ssh.connect(self._host, **self._params)
        except ssh.AuthenticationException as e:
            raise
        except Exception as e:
            print(e)

        if not hasattr(self, '_sftp'):
            self._sftp = self._ssh.open_sftp()

    @property
    def sftp(self):
        """Lazy SFTP connection"""
        if not hasattr(self, '_sftp'):
            self._connect()
        return self._sftp

    def _get(self, name):
        try:
            return SFTPStorageFile(name, self, 'rb')
        except IOError:
            pass

    def _exists(self, name):
        try:
            f = SFTPStorageFile(name, self, 'rb')
            f.close()
            return True
        except Exception:
            return False

    def _read(self, name):
        remote_path = self._remote_path(name)
        return self.sftp.open(remote_path, 'rb')

    def _remote_path(self, name):
        return self._join(self._root_path, name)

    def _join(self, *args):
        # Use the path module for the remote host type to join a path together
        return self._pathmod.join(*args)


class SFTPStorageFile(File):
    def __init__(self, name, storage, mode):
        self._name = name
        self._storage = storage
        self._mode = mode
        self._is_dirty = False
        self.file = StringIO()
        self._is_read = False

    @property
    def size(self):
        if not hasattr(self, '_size'):
            self._size = self._storage.size(self._name)
        return self._size

    def read(self, num_bytes=None):
        if not self._is_read:
            self.file = self._storage._read(self._name)
            self._is_read = True

        return self.file.read(num_bytes)

    def write(self, content):
        raise NotImplementedError

    def close(self):
        if self._is_dirty:
            self._storage._save(self._name, self.file.getvalue())
        self.file.close()
