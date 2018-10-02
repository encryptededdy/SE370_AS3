#!/usr/bin/env python
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import with_statement

import filecmp
import logging

import os
import shutil
import sys
import errno
import logging

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

# Modified by: Edward Zhang, ezha210

class VersionFS(LoggingMixIn, Operations):
    def __init__(self):
        # get current working directory as place for versions tree
        self.root = os.path.join(os.getcwd(), '.versiondir')
        # check to see if the versions directory already exists
        if os.path.exists(self.root):
            print('Version directory already exists.')
        else:
            print('Creating version directory.')
            os.mkdir(self.root)

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        print ("access:", path, mode)
        full_path = self._full_path(path)
        if not os.access(full_path, mode) or ".previousversions" in full_path:
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        # print "chmod:", path, mode
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        # print "chown:", path, uid, gid
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        # print "getattr:", path
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                                                        'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size',
                                                        'st_uid'))

    def readdir(self, path, fh):
        # print "readdir:", path
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            if ".previousversions" not in r:
                yield r

    def readlink(self, path):
        # print "readlink:", path
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        # print "mknod:", path, mode, dev
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        # print "rmdir:", path
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        print ("mkdir:", path, mode)
        if (str(path).endswith(".previousversions")):
            # Prevent the user from creating a .previousversions
            raise Exception("Invalid directory name")
        else:
            return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        # print "statfs:", path
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
                                                         'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files',
                                                         'f_flag',
                                                         'f_frsize', 'f_namemax'))

    def unlink(self, path):
        # print "unlink:", path
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        # print "symlink:", name, target
        return os.symlink(target, self._full_path(name))

    def rename(self, old, new):
        # print "rename:", old, new
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        # print "link:", target, name
        return os.link(self._full_path(name), self._full_path(target))

    def utimens(self, path, times=None):
        # print "utimens:", path, times
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        print('** open:', path, '**')
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        print('** create:', path, '**')
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        print('** read:', path, '**')
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        print('** write:', path, '**')
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        print('** truncate:', path, '**')
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        print('** flush', path, '**')
        return os.fsync(fh)

    # Store version when something's released
    def release(self, path, fh):
        logging.basicConfig()
        print('** release', path, '**')

        # split up the path
        (path_dir, path_file) = os.path.split(path)
        # print("Found path_dir: ", path_dir, " path_file: ", path_file)
        if path_dir.startswith("/"):
            path_dir = path_dir[1:] # remove leading slash as it breaks os.path.join

        # make directory if it doesn't exist...
        if not os.path.exists(os.path.join(os.getcwd(), '.versiondir', path_dir, '.previousversions', path_file)):
            # print("Making dir ", os.path.join(os.getcwd(), '.versiondir', path_dir, '.previousversions', path_file))
            os.makedirs(os.path.join(os.getcwd(), '.versiondir', path_dir, '.previousversions', path_file))
        # else:
            # print("Detected ", os.path.join(os.getcwd(), '.versiondir', path_dir, '.previousversions', path_file))

        versions = []

        # find the greatest version that already exists
        existing_version_count = 0
        for version_file in os.listdir(os.path.join(os.getcwd(), '.versiondir', path_dir, '.previousversions', path_file)):
            if version_file.isdigit():
                versions.append(int(version_file))
                if int(version_file) > existing_version_count:
                    existing_version_count = int(version_file)

        # make a copy and store it, with version+1
        original_file_path = os.path.join(os.getcwd(), '.versiondir', path_dir, path_file)
        existing_version_file_path = os.path.join(os.getcwd(), '.versiondir', path_dir, '.previousversions', path_file, str(existing_version_count))
        new_version_file_path = os.path.join(os.getcwd(), '.versiondir', path_dir, '.previousversions', path_file, str(existing_version_count+1))

        if existing_version_count == 0 or not filecmp.cmp(original_file_path, existing_version_file_path):
            print("Copying from ", original_file_path, " to ", new_version_file_path)
            shutil.copyfile(original_file_path, new_version_file_path)
            versions.append(existing_version_count+1)
        else:
            print("No changed detected, not copying")

        # sort versions
        versions.sort()

        # loop through deleting old versions until we have only 6 left
        while len(versions) > 6:
            to_delete = versions.pop(0)
            version_to_delete_path = os.path.join(os.getcwd(), '.versiondir', path_dir, '.previousversions', path_file,
                                                  str(to_delete))
            os.remove(version_to_delete_path)

        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        print('** fsync:', path, '**')
        return self.flush(path, fh)


def main(mountpoint):
    FUSE(VersionFS(), mountpoint, nothreads=True, foreground=True)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1])
