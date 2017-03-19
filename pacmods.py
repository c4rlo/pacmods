#!/usr/bin/python3

import hashlib
import os
import os.path
import pyalpm
import sys
from contextlib import suppress

DIRS = ('/etc', '/usr/local/etc')

SKIP_DIRS = {
    '/etc/ssl': ('certs',),
    '/etc/ca-certificates': ('extracted',)
}

BUFSIZE = 65536


def errprint(s):
    print(s, file=sys.stderr)


def main():
    allpaths = set()

    for pkg in pyalpm.Handle('/', '/var/lib/pacman').get_localdb().pkgcache:
        for path, db_md5 in pkg.backup:
            md5 = hashlib.md5()
            try:
                f = open('/' + path, 'rb', BUFSIZE)
            except FileNotFoundError:
                if path in (p for p, _, _ in pkg.files):
                    print('D /{} ({})'.format(path, pkg.name))
            except PermissionError as e:
                errprint('{} ({})'.format(e, pkg.name))
            else:
                for chunk in iter(lambda: f.read(BUFSIZE), b''):
                    md5.update(chunk)
                f.close()
                if md5.hexdigest() != db_md5:
                    print('M /{} ({})'.format(path, pkg.name))
        allpaths.update('/' + path for path, _, _ in pkg.files)

    for top in DIRS:
        for dirpath, dirnames, filenames in os.walk(top, onerror=errprint):
            for d in SKIP_DIRS.get(dirpath, ()):
                with suppress(ValueError):
                    dirnames.remove(d)
            for fn in filenames:
                path = os.path.join(dirpath, fn)
                if path not in allpaths:
                    print('A ' + path)


if __name__ == '__main__':
    main()
