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

__version__ = '0.2'

# Name of the class can be changed in that case the name in the instance in line 74 must be changed too
# suggested graphic symbols that can be used
# ┏ ┓ ┗ ┛ ▂ ▁ ┃ ╹ ╻ ◎ ▣ ▩ ▒ ▓ └ ┘ ┌ ┐ ┬ ┴ ┼ ├ ┤ ─ │ ✅ ⛔
# ┏━━━━━┓ 
# ┫ USB ┣
# ┗━━━━━┛
class picopins(showpins):
#   PWM   | UART    |   I2C  |  SPI   | GPIO |pin#|   DIAGRAM   |pin#| GPIO     |  SPI   |   I2C  | UART    | PWM
    PINOUT = [line.split("|") for line in """
          |         |        |        |      |  |     ┏━━━━━┓     |  |          |        |        |         |
          |         |        |        |      |  |┏━━━━┫     ┣━━━━┓|  |          |        |        |         |
    PWM0 A|UART0 TX |I2C0 SDA|SPI0 RX |GP0   |1 |┃◎   ┗━━━━━┛   ◎┃|40|VBUS      |        |        |         |
    PWM0 B|UART0 RX |I2C0 SCL|SPI0 CSn|GP1   |2 |┃◎ ▩           ◎┃|39|VSYS      |        |        |         |
          |         |        |        |Ground|3 |┃▣ └─GP25      ▣┃|38|Ground    |        |        |         |
    PWM1 A|UART0 CTS|I2C1 SDA|SPI0 SCK|GP2   |4 |┃◎  ▒▒▒        ◎┃|37|3v3 En    |        |        |         |
    PWM1 B|UART0 RTS|I2C1 SCL|SPI0 TX |GP3   |5 |┃◎  ▒▒▒        ◎┃|36|3v3 Out   |        |        |         |
    PWM2 A|UART1 TX |I2C0 SDA|SPI0 RX |GP4   |6 |┃◎             ◎┃|35|ADC VRef  |        |        |         |
    PWM2 B|UART1 RX |I2C0 SCL|SPI0 CSn|GP5   |7 |┃◎             ◎┃|34|GP28 / A2 |SPI1 RX |I2C0 SDA|UART0 TX |PWM6 A
          |         |        |        |Ground|8 |┃▣             ▣┃|33|ADC Ground|        |        |         |
    PWM3 A|UART1 CTS|I2C1 SDA|SPI0 SCK|GP6   |9 |┃◎   ▓▓▓▓▓▓▓   ◎┃|32|GP27 / A1 |SPI1 TX |I2C1 SCL|UART1 RTS|PWM5 B
    PWM3 B|UART1 RTS|I2C1 SCL|SPI0 TX |GP7   |10|┃◎   ▓▓▓▓▓▓▓   ◎┃|31|GP26 / A0 |SPI1 SCK|I2C1 SDA|UART1 CTS|PWM5 A
    PWM4 A|UART1 TX |I2C0 SDA|SPI1 RX |GP8   |11|┃◎   ▓▓▓▓▓▓▓   ◎┃|30|run       |        |        |         |
    PWM4 B|UART1 RX |I2C0 SCL|SPI1 CSn|GP9   |12|┃◎   ▓▓▓▓▓▓▓   ◎┃|29|GP22      |SPI0 SCK|I2C1 SDA|UART1 CTS|PWM3 A
          |         |        |        |Ground|13|┃▣             ▣┃|28|Ground    |        |        |         |
    PWM5 A|UART1 CTS|I2C1 SDA|SPI1 SCK|GP10  |14|┃◎             ◎┃|27|GP21      |SPI0 CSn|I2C0 SCL|UART1 RX |PWM2 B
    PWM5 B|UART1 RTS|I2C1 SCL|SPI1 TX |GP11  |15|┃◎             ◎┃|26|GP20      |SPI0 RX |I2C0 SDA|UART1 TX |PWM2 A
    PWM6 A|UART0 TX |I2C0 SDA|SPI1 RX |GP12  |16|┃◎             ◎┃|25|GP19      |SPI0 TX |I2C1 SCL|UART0 RTS|PWM1 B
    PWM6 B|UART0 RX |I2C0 SCL|SPI1 CSn|GP13  |17|┃◎             ◎┃|24|GP18      |SPI0 SCK|I2C1 SDA|UART0 CTS|PWM1 A
          |         |        |        |Ground|18|┃▣             ▣┃|23|Ground    |        |        |         |
    PWM7 A|UART0 CTS|I2C1 SDA|SPI1 SCK|GP14  |19|┃◎             ◎┃|22|GP17      |SPI0 CSn|I2C0 SCL|UART0 RX |PWM0 B
    PWM7 B|UART0 RTS|I2C1 SCL|SPI1 TX |GP15  |20|┃◎    ◎ ▣ ◎    ◎┃|21|GP16      |SPI0 RX |I2C0 SDA|UART0 TX |PWM0 A
          |         |        |        |      |  |┗━━━━━━━━━━━━━━━┛|  |          |        |        |         |
""".splitlines()[1:]]

# This list contains the ground pins
    GROUND = (3, 8, 13, 18, 23, 28, 38)
# This list contains the power pins
    POWER = (40, 39, 37, 36)
# This list contains the ADC pins
    ADC = (35, 34, 33, 32, 31)
# This list contains the RUN/RESET pins
    RUN = (30,)
# This string contains the name of the board must end with a space
    BOARD = 'Raspberry Pi Pico ' + __version__
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
