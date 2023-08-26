#!/bin/env python3
import re
import sys

import rich
from rich.panel import Panel
from rich.table import Table
from showpins import showpins, Options

"""
xiaopins, by fdufnews based on @gadgetoid work

Support him:
https://ko-fi.com/gadgetoid
https://github.com/sponsors/Gadgetoid
https://www.patreon.com/gadgetoid

Shout-out to Raspberry Pi Spy for having almost this exact idea first:
https://www.raspberrypi-spy.co.uk/2022/12/pi-pico-pinout-display-on-the-command-line/
"""

__version__ = '2.0.0'

class xiaopins(showpins):
    

    PINOUT = [line.split("|") for line in """
          |         |        |        |         |  |     ┏━━━━━┓     |  |       |        |        |         |
          |         |        |        |         |  |┏━━━━┫     ┣━━━━┓|  |       |        |        |         |
    PWM5 A|UART1 CTS|I2C1 SDA|SPI1 SCK|GP26 / A0|1 |┃◎   ┗━━━━━┛   ◎┃|14|VBUS   |        |        |         |
    PWM5 B|UART1 RTS|I2C1 SCL|SPI1 TX |GP27 / A1|2 |┃◎  GP16┬─┬──▩ ▣┃|13|Ground |        |        |         |
    PWM6 A|UART0 TX |I2C0 SDA|SPI1 RX |GP28 / A2|3 |┃◎  GP17┘GP25  ◎┃|12|3v3 Out|        |        |         |
    PWM6 B|UART0 RX |I2C0 SCL|SPI0 CSn|GP29 / A3|4 |┃◎ ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|11|GP3    |SPI0 TX |I2C1 SCL|UART0 RTS|PWM1 B
    PWM3 A|UART1 CTS|I2C1 SDA|SPI0 SCK|GP6      |5 |┃◎ ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|10|GP4    |SPI0 RX |I2C0 SDA|UART1 TX |PWM2 A
    PWM3 B|UART1 RTS|I2C1 SCL|SPI0 TX |GP7      |6 |┃◎ ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|9 |GP2    |SPI0 SCK|I2C1 SDA|UART0 CTS|PWM1 A
    PWM0 A|UART0 TX |I2C0 SDA|SPI0 RX |GP0      |7 |┃◎ (R)  ▩  (B) ◎┃|8 |GP1    |SPI0 CSn|I2C0 SCL|UART0 RX |PWM0 B
          |         |        |        |         |  |┃ GP11☀─┴─GP12  ┃|  |       |        |        |         |
          |         |        |        |         |  |┗━━━━━━━━━━━━━━━┛|  |       |        |        |         |
""".splitlines()[1:]]


    GROUND = (13,)
    POWER = (12, 14)
    ADC = (1, 2, 3, 4)
    RUN = ()
    BOARD = 'XIAO RP2040 ' + __version__

    LED = ((3, 3, "GP16","highlight_g"),
            (3, 4, "GP17","highlight_r"),
            (3, 4, "GP25","highlight_b"),
            (8, 9, "GP11","highlight_r"),
            (8, 9, "GP12","highlight_r"))
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)


board = xiaopins()

def main():
    rich.print(board.display(Options(sys.argv)))

if __name__ == "__main__":
    main()
