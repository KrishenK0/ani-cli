# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# Maintainer: KrishenK <Contact with GitHub issue>
pkgname='ani-cli-vostfr-git'
_pkgname='ani-cli'
pkgver=0.1.7.r11.66f0fb9
pkgrel=1
pkgdesc="A cli to browse and watch anime in VOSTFR (inspired by pystardust)"
arch=('any')
url="https://github.com/KrishenK0/ani-cli.git"
license=('MIT')
depends=('python' 'geckodriver' 'mpv')
makedepends=('git')
checkdepends=()
optdepends=()
provides=('ani-cli')
conflicts=('ani-cli')
source=("git+$url")
noextract=()
md5sums=('SKIP')

pkgver() {
    cd "$srcdir/${_pkgname}"
    printf "0.1.7.r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build() {
    cd "$srcdir/${_pkgname}"
	make
}

package() {
	cd "$srcdir/${_pkgname}"
	make DESTDIR="$pkgdir/" install
    install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${_pkgname}/LICENSE"
    install -Dm644 README.md "${pkgdir}/usr/share/doc/${_pkgname}/README.md"
}
