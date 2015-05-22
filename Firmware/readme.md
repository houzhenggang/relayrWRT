'Somabar' Controller
=======
relayrWRT Firmware
===================================
Features
------
1. Flexible wifi configuration(internet access) via Luci
2. I2C integration
3. SPI integration
4. Linux 3.18.7 Kernel
5. mosquitto bridge integration
6. Linux-NFC(neard) tools and test scripts in python
7. PCF875x GPIO expander support
8. TRF7970A driver support
9. gpio-led support

Flash the firmware
------


1.After flashing the firmware, there will be a Wifi network "relayrWRTxxxx", xxxx are the last 4 digits of the board's MAC addr.

2. There is no password for the Wifi, you can set a new password for wifi via log in 192.168.7.1

3. The default IP of relayr Firmware is set to 192.168.7.1

First time connect
------
If you connect first time to this firmware or you didn't set password for root user of OpenWrt, use telnet to connect:

telnet 192.168.7.1


Set the password for root:

root@OpenWrt:~# passwd

The WRTnode will set up a default connection to relayr wifi

Get access to internet
------

1. log in Luci : 192.168.7.1
2. go to Network--Wifi
3. Click "Scan"
4. Find correct network, type in the correct password and click "Submit"


Packages needed:
--------

update the package feeds:

```
opkg update

```

Install Paho client for Python:

```
cd /tmp
wget http://git.eclipse.org/c/paho/org.eclipse.paho.mqtt.python.git/snapshot/org.eclipse.paho.mqtt.python-1.1.tar.gz
tar xzf org.eclipse.paho.mqtt.python-1.1.tar.gz
cd org.eclipse.paho.mqtt.python-1.1
python setup.py install
```
Integrated mosquitto bridge config file to allow the broker run as a deamon at startup:
```
/etc/mosquitto/relayr.conf

/etc/mosquitto/relayr.crt
```
mosquitto deamon is auto enabled

default port is 1888 (no SSL needed, we are in the local network).

Function tests:
--------

Make sure that the WRTnode is connected to internet.

##mosquitto bridge test
The /etc/mosquitto/relayr.conf set up a bridge connection to Relayr cloud(SSL connection from relayr to WRTnode, no SSL from WRTnode to its wifi device)
```
mosquitto_sub -h 192.168.7.1 -t /temp/#

```

##TRF7970A NFC test
Each time a tag is presented, step 2 must precede the list or dump commands. Otherwise, the transmitter will not be on to power the passive tag.

```
1. test/test-adapter powered nfc0 on
2. test/test-adapter poll nfc0 on Initiator
3. test/test-tag list
4. test/test-tag dump
5. test/test-tag write /org/neard/nfc0/tagnumberinthelist Text UTF-8 en-US hello,relayr!

```
##PCF875x GPIO expander test


1 Calculate the pin number

GPIO expander pin number = 112 + offset of control pin register

2 /sys/class/gpio/export write the number

for example gpio112 ,after the success of the command to generate/sys/class/gpio/gpio112 directory, if there are no corresponding directory, means the pin cannot be derived

```
echo 0 > /sys/class/gpio/export
```

3 The direction file in /sys/class/gpio/gpio0

direction: define input and output

defined as the output：
```
echo out > direction
```
defined as the input：

```
echo in > direction
```
4 The value file in /sys/class/gpio/gpio0

Value: level of gpio pin, 0 (low level) 1 (high level), if the gpio is configured as output, the value is writable, remember any nonzero value will output a high level

```
echo 1 > value
```

##Write Green Red LED test
The Leds are registed in the kernel and we can manupulate these leds though shell commands.

```
GPIOs 40-71, platform/10000660.gpio, 10000660.gpio:
 gpio-40  (somabar:white:ld1   ) out hi    
 gpio-42  (somabar:red:ld2     ) out hi    
 gpio-44  (somabar:green:ld3   ) out hi 

```
```
root@OpenWrt:/# echo 1 > /sys/class/leds/somabar\:green\:ld3/brightness
root@OpenWrt:/# echo 0 > /sys/class/leds/somabar\:green\:ld3/brightness
```
