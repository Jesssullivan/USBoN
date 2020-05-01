#!/bin/bash
# example systemctl wan config for batman
# a WIP for the D&M Makerspace @ github/jesssullivan

# individual IPv4 IDs:
IPV1=0
IPV2=1
addr=172.27.$IPV1.$IPV2

# TODO: automated check to make sure all nodes receive unique IDs
echo BATSpace network: starting B.A.T.M.A.N.:

modprobe batman-adv
ip link set wlan1 down

# ifconfig wlan1 mtu 1532 # unusual, cited as 1532 though
ifconfig wlan1 mtu 1500 # much more usual, perhaps wrong...?
iwconfig wlan1 mode ad-hoc
iwconfig wlan1 essid BATSpace
iwconfig wlan1 channel 8

echo BATSpace: configuring wlan1...

sleep 1 && echo ...

ip link set wlan1 up

sleep 1 && echo ...

batctl if add wlan1

echo BATSpace: enabling bat0...

sleep 2 && echo ...

ifconfig bat0 up

echo BATSpace: configuring IPv4 on $addr

sleep 5 && echo ...

# individual IPv4:
ifconfig bat0 $addr/16

echo BATSpace: startup tasks complete
