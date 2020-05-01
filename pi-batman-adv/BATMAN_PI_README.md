
*Using motioneye video clients on Raspbian & a BATMAN-adv Ad-Hoc network*

[link: motioneyeos](https://github.com/ccrisan/motioneyeos/wiki)   
[link: motioneye Daemon](https://github.com/ccrisan/motioneye/wiki)   
[link: Pi Zero W Tx/Rx data sheet:](https://www.cypress.com/file/298756/download#page=28&zoom=100,0,184)   
[link: BATMAN Open Mesh](https://www.open-mesh.org/projects/open-mesh/wiki)   

The Pi Zero uses an onboard BCM43143 wifi module.  See above for the data sheet.
We can expect around a ~19 dBm Tx signal from a BCM43143 if we are optimistic.  Unfortunately, "usable" Rx gain is unclear in the context of the Pi.

This implementation of motioneye is running on Raspbian Buster (opposed to motioneyeos).  

**Calculating Mesh Effectiveness w/ Python:**

Please take a look at dBmLoss.py- the idea here is one should be able to estimate the maximum plausible distance between mesh nodes before setting anything up.  It can be run with no arguments-  

```
python3 dBmLoss.py
```  

...with no arguments, it should use default values (Tx = 20 dBm, Rx = |-40| dBm) to print this:   

```
you can add (default) Rx Tx arguments using the following syntax:
                 python3 dBmLoss.py 20 40
                 python3 dBmLoss.py <Rx> <Tx>                 


 57.74559999999994 ft = max. mesh node spacing, @
 Rx = 40
 Tx = 20
```   

Try a few values from a shell or take a look in the file for more info.  

**Order of Operations:**

All shell scripts should be privileged to match ```chmod u+x``` and assume a Raspbian Buster environment.

See ./motionConfig.sh to configure motioneye.   
See ./batmanConfig.sh to install & configure BATMAN-adv.   
See ./batmanRC.sh to initialize the network   
See batmanBATSpace.service for a systemd service framework
