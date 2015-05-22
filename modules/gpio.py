#!/usr/bin/env python

"""
Control the Digital I/Os the WRTNode using SYSFS
"""
import sys

# Available pins on the WRTNode:
# Check datasheet!! Many pins are just Output only
GPIO0 = 0       # Output Only
GPIO1 = 1       # GPIO1 = I2C_SD (I2C Data)
GPIO2 = 2       # GPIO2 = I2C_SCL (I2C Clock)
GPIO4 = 4       # GPIO4 = SPI_CLK (SPI Clock)
GPIO5 = 5       # GPIO5 = SPI_MOSI (SPI Master Input/Slave Output ***regarding datasheet!)
GPIO6 = 6       # GPIO6 = SPI_MISO (SPI Master Ouptup/Slave Input *)
GPIO15 = 15     # GPIO15 = TXD2 (UART Lite TXD)
GPIO16 = 16     # GPIO16 = RXD2 (UART Lite RXD)
GPIO17 = 17     # GPIO17 = WDT_RST_N (Watchdog Reset)
GPIO18 = 18     # GPIO18 = ANT_TRNB ((-) sig. for anntenna T/R swich)
GPIO19 = 19     # GPIO19 = ANT_TRN ((+)) sig. for anntenna T/R swich)
GPIO20 = 20     # GPIO20 = PA_PG_G0 (Control for external PA0)
GPIO21 = 21     # GPIO21 = PA_PG_G1 (Control for external PA1)
GPIO37 = 37     # GPIO37 = SPI_CS1 (SPI chip select 1)
GPIO38 = 38     # GPIO38 = SPI_HOLD (GPO Output)
GPIO39 = 39     # GPIO39 = SPI_WP (GPO Output)
GPIO40 = 40     # GPIO40 = EPHY_LED0_N_JTDO
GPIO41 = 41     # GPIO41 = EPHY_LED1_N_JTDI
GPIO42 = 42     # GPIO42 = EPHY_LED2_N_JTMS
GPIO43 = 43     # GPIO43 = EPHY_LED3_N_JTCLK
GPIO44 = 44     # GPIO44 = EPHY_LED4_N_JTRST_N


class Pin:

    pinId = None
    pinDir = ""

    def __init__(self, pinId):
        self.pinId = pinId
        self.export()

    def __del__(self):
        self.unexport()

    def state(self):
        f = file(self.pinDir + "value", "r")
        s = f.read()
        f.close()

        if s == "1\n":
            return 1

        return 0

    def export(self):
        f = file("/sys/class/gpio/export", "w")
        f.write("%d" % self.pinId)
        f.close()
        self.pinDir = "/sys/class/gpio/gpio%d/" % self.pinId

    def unexport(self):
        f = file("/sys/class/gpio/unexport", "w")
        f.write("%d" % self.pinId)
        f.close()

    def __str__(self):
        return ("P_%d" % self.pinId)


class PinIn(Pin):

    def __init__(self, pinId):
        Pin.__init__(self, pinId)
        f = file(self.pinDir + "direction", "w")
        f.write("in")
        f.close()


class PinOut(Pin):

    def __init__(self, pinId):
        Pin.__init__(self, pinId)
        f = file(self.pinDir + "direction", "w")
        f.write("out")
        f.close()

    def set(self):
        f = file(self.pinDir + "value", "w")
        f.write("1")
        f.close()

    def clear(self):
        f = file(self.pinDir + "value", "w")
        f.write("0")
        f.close()

    def toggle(self):
        if self.state() == 1:
            self.clear()
        else:
            self.set()


class DigitalIO:

    def __init__(self):
        pass

    @staticmethod
    def get_input(self, pinId):
        return PinIn(pinId)

    @staticmethod
    def get_output(pinId):
        return PinOut(pinId)

    @staticmethod
    def release(self, pin):
        del pin


""" Example use:

    pin = DigitalIO.get_output(GPIO23)
    pin.clear()
    pin.toggle()
    release(pin)
"""
if __name__ == "__main__":
    try:
        print "GPIO Module: exporting gpio20..."
        ping = DigitalIO.get_output(GPIO20)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
