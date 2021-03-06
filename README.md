# pacmods

Arch Linux tool to show changes to the system configuration files.

Example run:

```
# ./pacmods.py
M /etc/fstab (filesystem)
M /etc/passwd (filesystem)
M /etc/systemd/logind.conf (systemd)
D /etc/foo.conf (foo)
A /etc/systemd/system/default.target
A /etc/profile.d/vim.sh
```

* Modified config files are indicated with `M`; the package that the file
  belongs to is appended in parentheses.
* Deleted config files are indicated with `D`; the owning package is appended in
  parentheses.
* Added config files are shown with `A`.

## How it works

* "`M`"odified and "`D`"eleted config files are detected by looking at the
  config files (or "backup files") of each installed package (these are
  [treated specially](https://www.archlinux.org/pacman/pacman.8.html#_handling_config_files_a_id_hcf_a)
  by `pacman`). Modifications are detected by comparing the MD5 checksum of the
  file against the package database.
* "`A`"dded files are all files in `/etc` and `/usr/local/etc` that are not
  owned by a package. Files in `/etc/ssl/certs` and
  `/etc/ca-certificates/extracted` are also excluded, as those directories
  appear to only contain generated files.

## Installation

* Either [get it from the AUR](https://aur.archlinux.org/packages/pacmods/)
  ([what's the AUR?](https://wiki.archlinux.org/index.php/Arch_User_Repository)).
* Or just
  [download `pacmods.py` from here](https://raw.githubusercontent.com/c4rlo/pacmods/master/pacmods.py)
  and run it. Note that you must have the
  [`python`](https://www.archlinux.org/packages/staging/x86_64/python/) and
  [`pyalpm`](https://www.archlinux.org/packages/extra/x86_64/pyalpm/) packages
  installed.

## TODO

* Make the list of config directories (currently `/etc` and `/usr/local/etc`)
  configurable.
* Make the list of excluded files (currently everything in `/etc/ssl/certs` and
  `/etc/ca-certificates/extracted`) configurable; and possibly tweak the
  defaults, if required.
* Make the output format configurable.
