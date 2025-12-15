# Maintainer: Sergey Chudakov <csredrat@gmail.com>
pkgname=topalias
pkgver=4.1.0
pkgrel=1
pkgdesc="Linux bash aliases generator from bash/zsh command history with statistics"
arch=('any')
url="https://github.com/CSRedRat/topalias"
license=('GPL3')
depends=('python' 'python-click>=8.0.1')
makedepends=('python-setuptools' 'python-wheel' 'python-build' 'python-installer' 'python-pytest')
source=("https://github.com/CSRedRat/$pkgname/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')  # Update with actual checksum after first build: sha256sum v$pkgver.tar.gz

build() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}

check() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m pytest || true
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
}

