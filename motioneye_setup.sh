#!/bin/bash
# setup pi zero motioneyeos cameras
# by Jess Sullivan @ the D&M Makerspace
#
# permiss & run:
# sudo chmod u+x motioneye_setup.sh
# ./motioneye_setup.sh

# make sure we are root:
if [[ $EUID -ne 0 ]]; then
   echo "sudo is required to install, aborting."
   exit 1
fi

# Target default is sdc:
if ! [[ $1 == *sd** ]]; then
  echo -e "Using default disk target sdc \nyou may append a different target like so: \n"
  echo -e "sudo ./motioneye_setup.sh sdc"
  DISK="sdc"
else
  echo -e "Using specified target $1"
  DISK=$1
fi

# fully qualified image url:
ADDR=https://github.com/ccrisan/motioneyeos/releases/download/20190911/motioneyeos-raspberrypi-20190911.img.xz

# the "don't remove image" arg:
KEEP="keep"

# .xz filename:
XZIMG="${ADDR##*/}"

# .img filename:
IMG=$(echo $XZIMG | sed -e 's/\(.xz\)*$//g')


# check wget- OSX does not have it installed by default:
command -v wget >/dev/null || {
  echo >&2 -e "wget is not installed! \n  " \
    " - on OSX w/ homebrew, run 'brew install wget' to continue.";
  exit 1
  }

# otherwise, get image:
wget $ADDR

# make sure we can unzip xz with unxz:
command -v unxz >/dev/null || {
  echo >&2 -e "unxz is not installed! \n  " \
    "please make sure unxz is available before continuing.";
  exit 1
  }

# expand image:
echo "expanding image...."
unxz -T 0 -c $IMG > ${IMG%???}
DISK_IMG=${IMG%???}

#install:
echo "installing at $DISK...."
umount /dev/$DISK 2>/dev/null || true
dd if=$DISK_IMG of=/dev/$DISK bs=1048576
sync

# disallow further r/w until reinserted:
eject /dev/$1

# remove zipped image? 
if ! [ "$1" = $KEEP ] || [ "$2" = $KEEP ]; then
  rm $XZIMG
  rm $IMG
fi

echo -e "\n\nall done!"

echo -e "\nreinsert the card if you'd like to add a wpa_supplicant.conf to the /boot partition. \n" \
  "\nto search for local camera addresses, you could use the following command: \n"

# literal (escaped $ for echo):
# sudo nmap -sP 10.206.1.1/24 | awk '/^Nmap/{ip=$NF}/B8:27:EB/{print ip}'

echo -e "sudo nmap -sP 10.206.1.1/24 | awk '/^Nmap/{"'ip=$NF'"}/B8:27:EB/{print ip}' \n"

	
