# x86 version-
# remote device install script to recive serial commands.
# -Jess Sullivan @ The D&M Makerspace

dpkg -s linux-tools-generic &> /dev/null

    if [ $? -ne 0 ]

        then
            echo "usbip not found, installing..."

            apt-get install linux-tools-generic -y  # usbip was added to mainline 'universe' ppa here

            touch usbip_install.log

            mkdir /usr/share/hwdata/ >> usbip_install.log  # usb.ids quick fix

            cp /var/lib/usbutils/usb.ids /usr/share/hwdata//usb.ids >> usbip_install.log  # usb.ids quick fix

            modprobe usbip_host  # configure to recive serial via usbip

            sleep .25

            echo 'attempted install....'

            # sysytemctl enable client.service  >> usbip_install.log

            echo 'install done, restarting ... '

            reboot now

        else

            echo 'usbip found, continuing...'

            usbipd &  # start usbip daemon in backround

            sleep .25

            usbip bind -b 1-1.2

    fi

