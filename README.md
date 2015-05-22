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
echo 112 > /sys/class/gpio/export
```

3 The direction file in /sys/class/gpio/gpio112

direction: define input and output

defined as the output：
```
echo out > direction
```
defined as the input：

```
echo in > direction
```
4 The value file in /sys/class/gpio/gpio112

Value: level of gpio pin, 0 (low level) 1 (high level), if the gpio is configured as output, the value is writable, remember any nonzero value will output a high level

```
echo 1 > value
```

##White Green Red LED test
The Leds are registed in the kernel and we can manupulate these leds though shell commands.

```
GPIOs 40-71, platform/10000660.gpio, 10000660.gpio:
 gpio-40  (somabar:white   ) out hi    
 gpio-42  (somabar:blue     ) out hi    
 gpio-44  (somabar:green   ) out hi 

```
```
root@OpenWrt:/# echo 1 > /sys/class/leds/somabar\:green/brightness
root@OpenWrt:/# echo 0 > /sys/class/leds/somabar\:green/brightness
```

To make the white LED blink 1s
```
root@OpenWrt:/sys/devices/gpio-leds/leds/somabar:white# echo timer > trigger 
root@OpenWrt:/sys/devices/gpio-leds/leds/somabar:white# echo 1000 > delay_off
root@OpenWrt:/sys/devices/gpio-leds/leds/somabar:white# echo 1000 > delay_on
```

To turn white LED off
```
root@OpenWrt:/sys/devices/gpio-leds/leds/somabar:white# echo none > trigger 
```
#I/O Mapping for the Somabar prototype:


Available I/Os on the WRTNode:

This is the current configuration for the I/Os in the machine.
------
Note: a LOW value (0) turns ON an Output, a HIGH (1) turn it OFF.

        To see which kernel module is registering which I/O:
        cat sys/kernel/debug/gpio
------


```
***********  WRTNode GPIOs: *************

GPIO_name, Direction, In/Out_Name:
----------------------------------
GPIO0,  Output ==> RFID_MUX_B1      //Antennas Multiplexer control
GPIO17, Input  ==> GLASS_DETECTOR
GPIO18, Output ==> RFID_MUX_B2
GPIO19, Output ==> RFID_MUX_B3
GPIO20, Output ==> TRF_ENABLE
GPIO21, Input  ==> TRF_IRQ
GPIO40, Output ==> WHITE_LED
GPIO41, Input  ==> CLEAN_WHATER_LOW
GPIO42, Output ==> RED_LED
GPIO43, Input  ==> WASTE_WATER_HIGH
GPIO44, Output ==> GREEN_LED
GPIO72, Output ==> RFID_MUX_B0


***********  Port Expander pins: *************

GPIO_name, Addresss, Output_Name, PCF875x IO:
---------------------------------------------
GPIO112 (BASE + 00) ==> POD6_PUMP        //P00
GPIO113 (BASE + 01) ==> POD5_PUMP        //P01
GPIO114 (BASE + 02) ==> POD4_PUMP        //P02
GPIO115 (BASE + 03) ==> POD3_PUMP        //P03
GPIO116 (BASE + 04) ==> POD2_PUMP        //P04
GPIO117 (BASE + 05) ==> POD1_PUMP        //P05
GPIO118 (BASE + 06) ==> NOT_USED         //P06
GPIO119 (BASE + 07) ==> BITTERS_PUMP     //P07
GPIO120 (BASE + 08) ==> WASH_SOLENOID    //P10
GPIO121 (BASE + 09) ==> CLEAN_WATER_PUMP //P11
GPIO122 (BASE + 10) ==> TRANSFER_PUMP    //P12
GPIO123 (BASE + 11) ==> NOT_USED         //P13
GPIO123 (BASE + 12) ==> NOT_USED         //P14
GPIO123 (BASE + 13) ==> NOT_USED         //P15
GPIO123 (BASE + 14) ==> NOT_USED         //P16
GPIO123 (BASE + 15) ==> NOT_USED         //P17

***********  Antenna Mux Truth Table: *************

Antenna, GPIOvalue(B0B1B2B3):
----------------------------------
A0,	1100
A1,	0000
A2,	1000
A3,	0111
A4,	0101
A5,	0100
```
Change different antenna:
```
echo 72 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio72/direction
echo 1 > /sys/class/gpio/gpio72/value

echo 0 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio0/direction
echo 0 > /sys/class/gpio/gpio0/value

echo 18 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio18/direction
echo 0 > /sys/class/gpio/gpio18/value

echo 19 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio19/direction
echo 0 > /sys/class/gpio/gpio18/value



echo 0 > /sys/class/gpio/gpio72/value
echo 0 > /sys/class/gpio/gpio0/value
echo 0 > /sys/class/gpio/gpio18/value
echo 0 > /sys/class/gpio/gpio19/value
```


