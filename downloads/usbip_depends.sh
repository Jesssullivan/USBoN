# remote device setup script to recive serial commands.
# run on startup as an administrator.
# written by Jess Sullivan @ The D&M Makerspace

dpkg -s linux-tools-generic &> /dev/null

    if [ $? -ne 0 ]

        then
            echo "usbip not found, installing..."

            apt-get install linux-tools-generic -y  # usbip was added to mainline 'universe' ppa here

            mkdir /usr/share/hwdata/  # usb.ids quick fix
            cp /var/lib/usbutils/usb.ids /usr/share/hwdata//usb.ids # usb.ids quick fix
            modprobe usbip_host  # configure to recive serial via usbip
            sleep .25 && echo 'attempted install....'

            echo 'install done, please restart pi.'

        else

            echo 'usbip found, continuing...'

            usbipd &  # start usbip daemon in backround
            sleep .25
            usbip bind -b 1-1  #  pi only really has bus 1-1, unlikely to be different

            echo 'completed setup!'

    fi



