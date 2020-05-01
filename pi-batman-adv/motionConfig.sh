#!/bin/bash
# init script for motioneye daemon
# a WIP for the D&M Makerspace @ github/jesssullivan

echo preforming initial update / upgrade...

apt-get install -y ffmpeg libmariadb3 libpq5 libmicrohttpd12

wget https://github.com/Motion-Project/motion/releases/download/release-4.2.2/pi_buster_motion_4.2.2-1_armhf.deb
dpkg -i pi_buster_motion_4.2.2-1_armhf.deb

apt-get install -y python-pip python-dev libssl-dev libcurl4-openssl-dev libjpeg-dev libz-dev
pip install motioneye

mkdir -p /etc/motioneye
cp /usr/local/share/motioneye/extra/motioneye.conf.sample /etc/motioneye/motioneye.conf
mkdir -p /var/lib/motioneye

cp /usr/local/share/motioneye/extra/motioneye.systemd-unit-local /etc/systemd/system/motioneye.service

# check systemd:
systemctl daemon-reload
systemctl enable motioneye
systemctl start motioneye
