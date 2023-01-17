# microbit
application to be exected by micro:bit and its extension cutebot (and others)



In order to let ubuntu to connect to micro:bit...
```
If Chromium has been installed from the snap store (the default in the Ubuntu Software Store) it will not be able to access WebUSB devices.
On some Linux distributions eg. Ubuntu,  you may need to declare a udev rule. To do this:

Close Chrome

On Fedora, ensure that the plugdev group exists
getent group plugdev >/dev/null || sudo groupadd -r plugdev


Create a file at
/etc/udev/rules.d/50-microbit.rules
 with the following content:
SUBSYSTEM=="usb", ATTR{idVendor}=="0d28", MODE="0664", GROUP="plugdev"

Add your user to the plugdev group (replace with your username): 
sudo usermod -a -G plugdev <your-username>

Restart the udev rules 
sudo udevadm control --reload-rules 

Log out and log back in
Open Chrome and try to pair again 
}
```
https://support.microbit.org/support/solutions/articles/19000105428-webusb-troubleshooting

Installing uflash to be able to use local python env to flash the app to microbit:
https://uflash.readthedocs.io/en/latest/
