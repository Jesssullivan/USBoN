*archived:*     

    
*remote setup:*
```bash
# install depends:
pip3 install Requests
sudo apt-get install usbip
# nohup usbipd &  # starts daemon, this is run from the python script 

# move files to destinations:
cp Py3_client.py ~
sudo cp client.service /etc/systemd/client.service

# start systemd service:
sudo systemctl daemon-reload
sudo systemctl enable client.service

# reboot for changes to take effect:
sudo reboot
``` 

*server setup:*  
```bash
# install depends:
sudo apt-get install linux-tools-generic
sudo modprobe vhci-hcd
python3 Py3_server.py
```