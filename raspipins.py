#!/bin/env python3
import re
import sys

import rich
from rich.panel import Panel
from rich.table import Table
from showpins import showpins, Options

"""
picopins, by @gadgetoid

Support me:
https://ko-fi.com/gadgetoid
https://github.com/sponsors/Gadgetoid
https://www.patreon.com/gadgetoid

Shout-out to Raspberry Pi Spy for having almost this exact idea first:
https://www.raspberrypi-spy.co.uk/2022/12/pi-pico-pinout-display-on-the-command-line/
"""

__version__ = '0.0.1'

# Name of the class can be changed in that case the name in the instance in line 74 must be changed too
class picopins(showpins):
#   PWM   | UART    |   I2C |  SPI    | GPIO |pin#|  DIAGRAM  |pin#| GPIO   |  SPI    |   I2C  | UART   | PWM
    PINOUT = [line.split("|") for line in """
          |        |        |         |        |  |━━━━━━━━━━━━━━━┓|  |          |         |        |        |
          |        |        |         |        |  |            (O)┃|  |          |         |        |        |
          |        |        |         |        |  |  ┏━━━━━━━━━┓  ┃|  |          |         |        |        |
          |        |        |         |3V3     |1 |  ┃◎       ◎┃  ┃|2 |5V        |         |        |        |
          |        |I2C1 SDA|         |GP2     |3 |  ┃◎       ◎┃  ┃|4 |5V        |         |        |        |
          |        |I2C1 SCL|         |GP3     |5 |  ┃◎       ▣┃  ┃|6 |Ground    |         |        |        |
          |        |        |         |GP4     |7 |  ┃◎       ◎┃  ┃|8 |GP14      |         |        |TXD     |
          |        |        |         |Ground  |9 |  ┃▣       ◎┃  ┃|10|GP15      |         |        |RXD     |
          |        |        |SPI1 CS1 |GP17    |11|  ┃◎       ◎┃  ┃|12|GP18      |SPI1 CS0 |        |        |PWM0
          |        |        |         |GP27    |13|  ┃◎       ▣┃  ┃|14|Ground    |         |        |        |
          |        |        |         |GP22    |15|  ┃◎       ◎┃  ┃|16|GP23      |         |        |        |
          |        |        |         |3V3     |17|  ┃◎       ◎┃  ┃|18|GP24      |         |        |        |
          |        |        |SPI0 MOSI|GP10    |19|  ┃◎       ▣┃  ┃|20|Ground    |         |        |        |
          |        |        |SPI0 MISO|GP9     |21|  ┃◎       ◎┃  ┃|22|GP25      |         |        |        |
          |        |        |SPI0 SCLK|GP11    |23|  ┃◎       ◎┃  ┃|24|GP8       |SPI0 CS0 |        |        |
          |        |        |         |Ground  |25|  ┃▣       ◎┃  ┃|26|GP7       |SPI0 CS1 |        |        |
          |        |ID_SD   |         |GP0(DNC)|27|  ┃◎       ◎┃  ┃|28|GP1(DNC)  |         |ID_SC   |        |
          |        |        |         |GP5     |29|  ┃◎       ▣┃  ┃|30|Ground    |         |        |        |
          |        |        |         |GP6     |31|  ┃◎       ◎┃  ┃|32|GP12      |         |        |        |PWM0
PWM1      |        |        |         |GP13    |33|  ┃◎       ▣┃  ┃|34|Ground    |         |        |        |
PWM1      |        |        |SPI1 MISO|GP19    |35|  ┃◎       ◎┃  ┃|36|GP16      |         |        |        |
          |        |        |         |GP26    |37|  ┃◎       ◎┃  ┃|38|GP20      |SPI1 MOSI|        |        |
          |        |        |         |Ground  |39|  ┃▣       ◎┃  ┃|40|GP21      |SPI1 SCLK|        |        |
          |        |        |         |        |  |  ┗━━━━━━━━━┛  ┃|  |          |         |        |        |
""".splitlines()[1:]]

# This list contains the ground pins
    GROUND = (6, 9, 14, 20, 25, 30, 34, 39)
# This list contains the power pins
    POWER = (1, 2, 4, 17)
# This list contains the ADC pins
    ADC = ()
# This list contains the RUN/RESET pins
    RUN = ()
# This string contains the name of the board must end with a space
    BOARD = 'Raspberry Pi ' + __version__
# This list of list contains the LED(s)
# 1st item row of the LED
# 2nd item row of the GPIO that drives the LED
# 3rd item the name of the GPIO
# 4th item the name of the color used to blink the LED one of (highlight_r, highlight_g, highlight_b)
    LED = ((3, 4, "GP25","highlight_r"),)
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)

# instance of the class
board = picopins()

def main():
    rich.print(board.display(Options(sys.argv)))

if __name__ == "__main__":
    main()
