# Packaging Guide

This document describes how to build native packages for different Linux distributions.

## Supported Distributions

- **Debian/Ubuntu**: `.deb` packages
- **Alt Linux and other RPM-based**: `.rpm` packages
- **Arch Linux**: AUR packages using `PKGBUILD`

## Prerequisites

### For Debian/Ubuntu (.deb)
```bash
sudo apt-get install build-essential debhelper dh-python python3-all python3-setuptools python3-wheel python3-build python3-installer
```

### For RPM (Alt Linux, Fedora, CentOS, etc.)
```bash
# On Alt Linux
sudo apt-get install rpm-build python3-devel python3-setuptools python3-wheel python3-pip

# On Fedora/CentOS
sudo dnf install rpm-build python3-devel python3-setuptools python3-wheel python3-pip
```

### For Arch Linux
```bash
sudo pacman -S base-devel python python-setuptools python-wheel python-build python-installer
```

## Building Packages

### Using Makefile (Recommended)

Build all package formats:
```bash
make packages
```

Build individual package formats:
```bash
make build-deb    # Build Debian package
make build-rpm    # Build RPM package
make build-arch   # Build Arch Linux package
```

### Manual Build Instructions

#### Debian/Ubuntu (.deb)

1. Ensure you have the source distribution:
   ```bash
   make dist
   ```

2. Build the Debian package:
   ```bash
   dpkg-buildpackage -b -us -uc
   ```

   The `.deb` file will be created in the parent directory.

3. To build a source package as well:
   ```bash
   dpkg-buildpackage -S -us -uc
   ```

#### RPM (Alt Linux, Fedora, CentOS)

1. Set up RPM build directories (if not already done):
   ```bash
   mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
   ```

2. Copy source tarball and spec file:
   ```bash
   cp dist/topalias-*.tar.gz ~/rpmbuild/SOURCES/
   cp topalias.spec ~/rpmbuild/SPECS/
   ```

3. Build the RPM:
   ```bash
   rpmbuild -ba ~/rpmbuild/SPECS/topalias.spec
   ```

   The RPM files will be in `~/rpmbuild/RPMS/noarch/` and source RPM in `~/rpmbuild/SRPMS/`.

#### Arch Linux (PKGBUILD)

1. Build the package:
   ```bash
   makepkg -s
   ```

2. Install the built package:
   ```bash
   sudo pacman -U topalias-*.pkg.tar.xz
   ```

3. To build without installing dependencies (if already installed):
   ```bash
   makepkg -s --skipinteg
   ```

## Package Installation

### Debian/Ubuntu
```bash
sudo dpkg -i topalias_*.deb
sudo apt-get install -f  # Install dependencies if needed
```

### RPM-based (Alt Linux, Fedora, CentOS)
```bash
# On Alt Linux
sudo apt-get install topalias-*.rpm

# On Fedora/CentOS
sudo dnf install topalias-*.rpm
```

### Arch Linux
```bash
sudo pacman -U topalias-*.pkg.tar.xz
```

Or if published to AUR:
```bash
yay -S topalias
# or
paru -S topalias
```

## Updating Package Versions

When releasing a new version, update the version in:
- `setup.py` (version field)
- `pyproject.toml` (version field)
- `topalias/__init__.py` (`__version__` variable)
- `PKGBUILD` (`pkgver` field)
- `topalias.spec` (`Version` field)
- `debian/changelog` (add new entry)

## Notes

- The PKGBUILD uses `SKIP` for sha256sums initially. After the first successful build, update it with the actual checksum.
- For RPM packages, you may need to adjust the `%{?dist}` macro based on your distribution.
- Debian packages use `debian/compat` version 13, which requires debhelper >= 13.

