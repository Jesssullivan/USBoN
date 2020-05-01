#!/bin/bash
# check open-mesh depends
# a WIP for the D&M Makerspace @ github/jesssullivan

apt-get update -y
apt-get upgrade -y

echo installing B.A.T.M.A.N. depends...
apt install -y libnl-3-dev libnl-genl-3-dev batctl

git clone https://git.open-mesh.org/batctl.git
cd batctl

echo please 'make install' manually
echo please 'echo 'batman-adv' | sudo tee --append /etc/modules' manually
echo please 'echo "$(pwd)/batmanRC.sh" >> ~/.bashrc' manually
