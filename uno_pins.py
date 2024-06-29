#!/bin/env python3
import re
import sys

import rich
from rich.panel import Panel
from rich.table import Table
from showpins import showpins, Options

"""
unopins, by fdufnews based on @gadgetoid work

Support him:
https://ko-fi.com/gadgetoid
https://github.com/sponsors/Gadgetoid
https://www.patreon.com/gadgetoid

Shout-out to Raspberry Pi Spy for having almost this exact idea first:
https://www.raspberrypi-spy.co.uk/2022/12/pi-pico-pinout-display-on-the-command-line/
"""

__version__ = '1.0'

class unopins(showpins):

    PINOUT = [line.split("|") for line in """
     | |       |        |        |  |  ┏━━━━━┓     ┏━━━━━┓ |  |      |        | |        |
     | |       |        |        |  |┏━┫ PWR ┣━━━━━┫ USB ┣┓|  |      |        | |        |
     | |       |        |        |  |┃ ┗━━━━━┛     ┗━━━━━┛┃|  |      |        | |        |
     | |       |        |        |  |┃                    ┃|  |      |        | |        |
     | |       |        |        |  |┃                   ◎┃|28|AREF  |        | |        |
     | |       |        |        |  |┃                 ▩ ▣┃|27|Ground|        | |        |
     | |       |        |        |  |┃              D13┘ ◎┃|26|D13   |SPI SCK | |        |
     | |       |        |        |  |┃                   ◎┃|25|D12   |SPI RX  | |        |
     | |       |        |Reset   |1 |┃◎                  ◎┃|24|D11   |SPI TX  | |        |PWM
     | |       |        |3V3     |2 |┃◎                  ◎┃|23|D10   |SPI SS  | |        |PWM
     | |       |        |5V      |3 |┃◎                  ◎┃|22|D9    |        | |        |PWM
     | |       |        |Ground  |4 |┃▣   ▓▓▓▓▓          ◎┃|21|D8    |        | |        |
     | |       |        |Ground  |5 |┃▣   ▓▓▓▓▓           ┃|  |      |        | |        |
     | |       |        |Vin     |6 |┃◎   ▓▓▓▓▓          ◎┃|20|D7    |        | |        |
     | |       |        |        |  |┃    ▓▓▓▓▓          ◎┃|19|D6    |        | |        |PWM
     | |       |        |D14 / A0|7 |┃◎   ▓▓▓▓▓          ◎┃|18|D5    |        | |        |PWM
     | |       |        |D15 / A1|8 |┃◎   ▓▓▓▓▓          ◎┃|17|D4    |        | |        |
     | |       |        |D16 / A2|9 |┃◎   ▓▓▓▓▓          ◎┃|16|D3    |        | |        |PWM
     | |       |        |D17 / A3|10|┃◎   ▓▓▓▓▓          ◎┃|15|D2    |        | |        |
     | |I2C SDA|        |D18 / A4|11|┃◎      ┏◎ ◎┓◎┓     ◎┃|14|D1    |        | |UART TX |
     | |I2C SCL|        |D19 / A5|12|┃◎      ┃▣ ◎┃◎┃     ◎┃|13|D0    |        | |UART RX |
     | |       |        |        |  |┗━━━━━━━╋╋━╋╋╋╋━━━━━━┛|  |      |        | |        |
     | |       |        |        |  |        ┃┃ ┃┃┃┃       |  |      |        | |        |
     | |       |        |Reset   |30|━━━━━━━━┛┃ ┃┃┃┗━━━━━━━|35|      |SPI RX  | |        |
     | |       |        |Ground  |31|━━━━━━━━━┛ ┃┃┗━━━━━━━━|34|5V    |        | |        |
     | |       |SPI TX  |        |32|━━━━━━━━━━━┛┗━━━━━━━━━|33|      |SPI SCK | |        |
""".splitlines()[1:]]


    GROUND = (4, 5, 27, 31)
    POWER = (2, 3, 6, 34)
    ADC = (7, 8, 9, 10, 11, 12)
    RUN = (1,)
    BOARD = 'Arduino UNO ' + __version__

    LED = ((5, 6, "D13","highlight_r"),)
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)


board = unopins()

def main():
    rich.print(board.display(Options(sys.argv)))

if __name__ == "__main__":
    main()
