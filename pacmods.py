#!/usr/bin/python3

import contextlib
import hashlib
import os
import os.path
import sys

import pyalpm

DIRS = "/etc", "/usr/local/etc"

SKIP_DIRS = {
    "/etc/ssl": ("certs",),
    "/etc/ca-certificates": ("extracted",)
}

BUFSIZE = 65536


def errprint(s):
    print(s, file=sys.stderr)


def main():
    allpaths = set()

    for pkg in pyalpm.Handle("/", "/var/lib/pacman").get_localdb().pkgcache:
        for path, db_md5 in pkg.backup:
            md5 = hashlib.md5()
            try:
                f = open(f"/{path}", "rb", BUFSIZE)
            except FileNotFoundError:
                if path in (p for p, _, _ in pkg.files):
                    print(f"D /{path} ({pkg.name})")
            except PermissionError as e:
                errprint(f"{e} ({pkg.name})")
            else:
                for chunk in iter(lambda: f.read(BUFSIZE), b""):
                    md5.update(chunk)
                f.close()
                if md5.hexdigest() != db_md5:
                    print(f"M /{path} ({pkg.name})")
        allpaths.update(f"/{path}" for path, _, _ in pkg.files)

    for top in DIRS:
        for dirpath, dirnames, filenames in os.walk(top, onerror=errprint):
            for d in SKIP_DIRS.get(dirpath, ()):
                with contextlib.suppress(ValueError):
                    dirnames.remove(d)
            for fn in filenames:
                path = os.path.join(dirpath, fn)
                if path not in allpaths:
                    print(f"A {path}")


if __name__ == "__main__":
    main()
