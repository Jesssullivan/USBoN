# depends:
apt-get install python3-pip -y
apt-get install python-pillow -y
apt-get install python-pip python-dev libssl-dev libcurl4-openssl-dev libjpeg-dev libz-dev -y
apt-get install ffmpeg libmariadb3 libpq5 libmicrohttpd12 -y
apt-get install linux-tools-generic -y
pip install requests
pip3 install requests
apt-get install usbip -y
modprobe usbip_host

# motioneye setup:
pip install motioneye
mkdir -p /etc/motioneye
cp /usr/local/share/motioneye/extra/motioneye.conf.sample /etc/motioneye/motioneye.conf
mkdir -p /var/lib/motioneye
cp /usr/local/share/motioneye/extra/motioneye.systemd-unit-local /etc/systemd/system/motioneye.service
systemctl daemon-reload
systemctl enable motioneye
systemctl start motioneye

cp client.py ~
echo '\n\n python3 /home/pi/client.py' >> ../../.bashrc

systemctl daemon-reload

reboot now
