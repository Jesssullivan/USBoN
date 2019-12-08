# USBoN
_ _ _
***README yet to be updated with Makerspace-specific formatting*** 
_ _ _
     
     
***Status***        

Intended for remote Pi Zeros (raspian + motioneye) installed around our facility.     
A central server manages motioneye streams, OctoPrint, job slicing, etc.    

Serial device (e.g. 3d printer) connected to a remote client is mounted on the server using the Debian usbip package.       


***prerequisite- usb.ids recently broke:***
```bash
sudo mkdir /usr/share/hwdata/
sudo cp /var/lib/usbutils/usb.ids /usr/share/hwdata//usb.ids
``` 

***send:***
```bash
# receiving: "client" 
sudo modprobe vhci-hcd
```

***bind:***
```bash
# sending: "server"
sudo modprobe usbip_host
sudo usbipd &
sudo usbip bind -b 1-1
```
    
