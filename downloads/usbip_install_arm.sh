# arm / pi version-
# remote device install script to recive serial commands.
# -Jess Sullivan @ The D&M Makerspace

dpkg -s usbip &> /dev/null

    if [ $? -ne 0 ]

        then
            echo "usbip not found, installing..."

            # linux-tools-generic is not available for arm- usbip must be optained seperately here
            apt-get install usbip -y

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

