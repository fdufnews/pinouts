#!/bin/env python3
import re
import sys

import rich
from rich.panel import Panel
from rich.table import Table
from showpins import showpins, Options

"""
nanopins, by fdufnews based on @gadgetoid work

Support him:
https://ko-fi.com/gadgetoid
https://github.com/sponsors/Gadgetoid
https://www.patreon.com/gadgetoid

Shout-out to Raspberry Pi Spy for having almost this exact idea first:
https://www.raspberrypi-spy.co.uk/2022/12/pi-pico-pinout-display-on-the-command-line/
"""

__version__ = '1.0.0'

class nanopins(showpins):

    PINOUT = [line.split("|") for line in """
     | |       |        |        |  |      ┏━━━━━┓      |  |      |       | |        |
     | |       |        |        |  |┏━━━━━┫ USB ┣━━━━━┓|  |      |       | |        |
     | |       |SPI SCK |D13     |16|┃◎    ┗━━━━━┛    ◎┃|15|D12   |SPI RX | |        |
     | |       |        |3V3     |17|┃◎               ◎┃|14|D11   |SPI TX | |        |PWM
     | |       |        |AREF    |18|┃◎               ◎┃|13|D10   |SPI SS | |        |PWM
     | |       |        |D21 / A7|19|┃◎    ▓▓▓▓▓▓▓    ◎┃|12|D9    |       | |        |PWM
     | |       |        |D20 / A6|20|┃◎    ▓▓▓▓▓▓▓    ◎┃|11|D8    |       | |        |
     | |I2C SCL|        |D19 / A5|21|┃◎    ▓▓▓▓▓▓▓    ◎┃|10|D7    |       | |        |
     | |I2C SDA|        |D18 / A4|22|┃◎               ◎┃| 9|D6    |       | |        |PWM
     | |       |        |D17 / A3|23|┃◎               ◎┃| 8|D5    |       | |        |PWM
     | |       |        |D16 / A2|24|┃◎               ◎┃| 7|D4    |       | |        |
     | |       |        |D15 / A1|25|┃◎  ▩            ◎┃| 6|D3    |       | |        |PWM
     | |       |        |D14 / A0|26|┃◎  ┗━D13        ◎┃| 5|D2    |       | |        |
     | |       |        |5V      |27|┃◎               ▣┃| 4|Ground|       | |        |
     | |       |        |Reset   |28|┃◎               ◎┃| 3|Reset |       | |        |
     | |       |        |Ground  |29|┃▣     ┏◎ ◎┓▣┓   ◎┃| 2|D0    |       | |UART RX |
     | |       |        |Vin     |30|┃◎     ┃◎ ◎┃◎┃   ◎┃| 1|D1    |       | |UART TX |
     | |       |        |        |  |┗━━━━━━╋╋━╋╋╋╋━━━━┛|  |      |       | |        |
     | |       |        |        |  |       ┃┃ ┃┃┃┃     |  |      |       | |        |
     | |       |        |5V      |31|━━━━━━━┛┃ ┃┃┃┗━━━━━|36|Ground|       | |        |
     | |       |SPI RX  |        |32|━━━━━━━━┛ ┃┃┗━━━━━━|35|Reset |       | |        |
     | |       |SPI SCK |        |33|━━━━━━━━━━┛┗━━━━━━━|34|      |SPI TX | |        |
""".splitlines()[1:]]


    GROUND = (4, 29, 36)
    POWER = (17, 27, 30, 31)
    ADC = (19, 20, 21, 22, 23, 24, 25, 26)
    RUN = (3, 28)
    BOARD = 'Arduino Nano ' + __version__

    LED = ((11, 12, "D13","highlight_r"),)
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)


board = nanopins()

def main():
    rich.print(board.display(Options(sys.argv)))

if __name__ == "__main__":
    main()
