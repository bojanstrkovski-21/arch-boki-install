#!/bin/bash

set -e

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo." >&2
    exit 1
fi

if [ -d /tmp/archlive ]; then
	sudo rm -rfv /tmp/archlive
fi

# Check if the folder still exists
if [ -d /tmp/archlive ]; then
    echo "Error: The folder /tmp/archlive still exists. Exiting..."
    exit 1
else
	tput setaf 3
	echo "############################################################"
    echo "Folder /tmp/archlive successfully removed or not present."
	echo "############################################################"
	sleep 3
	tput sgr0
fi

echo "########################################################"
echo "########################################################"
echo "########################################################"
echo "########################################################"

packages_file="/tmp/archlive/packages.x86_64"

# Packages to add to the archiso profile packages
packages=(
	gcc
	git
	pkgconfig
	python
	python-pip
	python-build
	python-wheel
	python-simple-term-menu
	python-uv
	python-setuptools
	python-pyparted
	python-pydantic
)

mkdir -p /tmp/archlive/airootfs/root/archinstall-git
cp -r . /tmp/archlive/airootfs/root/archinstall-git

cat <<- _EOF_ | tee /tmp/archlive/airootfs/root/.zprofile
	cd archinstall-git
	rm -rf dist

	uv build --no-build-isolation --wheel
	uv pip install dist/*.whl --break-system-packages --system --no-build --no-deps

	echo
	alias sy="pacman -Syy"
	alias pinit="systemctl status pacman-initi.service"
	alias pc="vim /etc/pacman.conf"
	alias reflect="cp /etc/pacman.d/mirrorlist mirror-bak && reflector --verbose -a 6 -l 20 -f 20 -p https --sort rate --save /etc/pacman.d/mirrorlist"
	alias arch="archinstall --advanced"
	echo "This is an unofficial ISO for development and testing of archinstall. No support will be provided."
	echo "This ISO was built from Git SHA $GITHUB_SHA"
	echo "Type archinstall to launch the installer."
_EOF_

pacman --noconfirm -S archiso

cp -r /usr/share/archiso/configs/releng/* /tmp/archlive

sed -i 's/iso_name="archlinux"/iso_name="ArchBoki-archinstall"/; s/iso_label="ARCH_/iso_label="ArchBoki-archinstall_/' /tmp/archlive/profiledef.sh

sed -i /archinstall/d "$packages_file"

# Add packages to the archiso profile packages
for package in "${packages[@]}"; do
	echo "$package" >> "$packages_file"
done

cp pacman.conf /tmp/archlive
mkdir -p /tmp/archlive/work/x86_64/airootfs/etc/
cp pacman.conf /tmp/archlive/work/x86_64/airootfs/etc/



find /tmp/archlive
cd /tmp/archlive

mkarchiso -v -w work/ -o out/ ./

date=$(date +%Y.%m.%d)

cp /tmp/archlive/work/iso/arch/pkglist.x86_64.txt  /tmp/archlive/out/archlinux-$date-x86_64.iso.pkglist.txt
