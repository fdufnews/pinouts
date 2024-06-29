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

__version__ = '1.0'

class picopins(showpins):

    PINOUT = [line.split("|") for line in """
          |         |        |        |      |  |     ┏━━━━━┓     |  |          |        |        |         |
          |         |        |        |      |  |┏━━━━┫     ┣━━━━┓|  |          |        |        |         |
    PWM0 A|UART0 TX |I2C0 SDA|SPI0 RX |GP0   |1 |┃◎   ┗━━━━━┛   ◎┃|40|VBUS      |        |        |         |
          |         |        |BOTRIGHT|GP1   |2 |┃◎ ▩           ◎┃|39|VSYS      |        |        |         |
          |         |        |        |Ground|3 |┃▣ └─GP25      ▣┃|38|Ground    |        |        |         |
          |         |        |       X|GP2   |4 |┃◎  ▒▒▒        ◎┃|37|3v3 En    |        |        |         |
          |         |        |       A|GP3   |5 |┃◎  ▒▒▒        ◎┃|36|3v3 Out   |        |        |         |
          |         |        |       Y|GP4   |6 |┃◎             ◎┃|35|ADC VRef  |        |        |         |
    PWM2 B|UART1 RX |I2C0 SCL|SPI0 CSn|GP5   |7 |┃◎             ◎┃|34|GP28 / A2 |SPI1 RX |I2C0 SDA|UART0 TX |PWM6 A
          |         |        |        |Ground|8 |┃▣             ▣┃|33|ADC Ground|        |        |         |
          |         |        |       B|GP6   |9 |┃◎   ▓▓▓▓▓▓▓   ◎┃|32|GP27 / A1 |START   |        |         |      
          |         |        | TFT_PWM|GP7   |10|┃◎   ▓▓▓▓▓▓▓   ◎┃|31|GP26 / A0 |SELECT  |        |         |      
          |         |        | TFT_DC |GP8   |11|┃◎   ▓▓▓▓▓▓▓   ◎┃|30|run       |        |        |         |
          |         |        | TFT_CSn|GP9   |12|┃◎   ▓▓▓▓▓▓▓   ◎┃|29|GP22      |SPI0 SCK|I2C1 SDA|UART1 CTS|PWM3 A
          |         |        |        |Ground|13|┃▣             ▣┃|28|Ground    |        |        |         |
          |         |        | TFT_SCK|GP10  |14|┃◎             ◎┃|27|GP21      |SPI0 CSn|I2C0 SCL|UART1 RX |PWM2 B
          |         |        | TFT_TX |GP11  |15|┃◎             ◎┃|26|GP20      |SPI0 RX |I2C0 SDA|UART1 TX |PWM2 A
          |         |        | TFT_RST|GP12  |16|┃◎             ◎┃|25|GP19      |SPI0 TX |I2C1 SCL|UART0 RTS|PWM1 B
          |         |        |    LEFT|GP13  |17|┃◎             ◎┃|24|GP18      |BOTLEFT |        |         |      
          |         |        |        |Ground|18|┃▣             ▣┃|23|Ground    |        |        |         |
          |         |        |    DOWN|GP14  |19|┃◎             ◎┃|22|GP17      |RIGHT   |        |         |      
    PWM7 B|UART0 RTS|I2C1 SCL|SPI1 TX |GP15  |20|┃◎    ◎ ▣ ◎    ◎┃|21|GP16      |UP      |        |         |      
          |         |        |        |      |  |┗━━━━━━━━━━━━━━━┛|  |          |        |        |         |
""".splitlines()[1:]]


    GROUND = (3, 8, 13, 18, 23, 28, 38)
    POWER = (40, 39, 37, 36)
    ADC = (35, 34, 33, 32, 31)
    RUN = (30,)
    BOARD = 'Raspberry Pi Pico + GamePad Module ' + __version__

    LED = ((3, 4, "GP25","highlight_r"),)
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)


board = picopins()

def main():
    rich.print(board.display(Options(sys.argv)))
    rich.print("GamePad from : https://fr.aliexpress.com/item/1005002542268650.html")

if __name__ == "__main__":
    main()
