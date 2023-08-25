#!/bin/env python3
import re
import sys

import rich
from rich.panel import Panel
from rich.table import Table
from showpins import showpins, Options

"""
prominipins, by fdufnews based on @gadgetoid work

Support him:
https://ko-fi.com/gadgetoid
https://github.com/sponsors/Gadgetoid
https://www.patreon.com/gadgetoid

Shout-out to Raspberry Pi Spy for having almost this exact idea first:
https://www.raspberrypi-spy.co.uk/2022/12/pi-pico-pinout-display-on-the-command-line/
"""

__version__ = '1.0.0'

class prominipins(showpins):

    PINOUT = [line.split("|") for line in """
        | |       |        |        |  |                   |  |      |       | |        |
        | |       |        |        |  |┏━━━━━━━━━━━━━━━━━┓|  |      |       | |        |
    PWM | |       |SPI SS  |D10     |13|┃◎ ▩             ◎┃|12|D9    |       | |        |PWM
    PWM | |       |SPI TX  |D11     |14|┃◎ ┗━D13         ◎┃|11|D8    |       | |        |
        | |       |SPI RX  |D12     |15|┃◎     ▓▓▓▓▓     ◎┃|10|D7    |       | |        |
        | |       |SPI SCK |D13     |16|┃◎   ▓▓▓▓▓▓▓▓▓   ◎┃| 9|D6    |       | |        |PWM
        | |       |        |D14 / A0|17|┃◎ ▓▓▓▓▓▓▓▓▓▓▓▓▓ ◎┃| 8|D5    |       | |        |PWM
        | |       |        |D15 / A1|18|┃◎   ▓▓▓▓▓▓▓▓▓   ◎┃| 7|D4    |       | |        |
        | |       |        |D16 / A2|19|┃◎     ▓▓▓▓▓     ◎┃| 6|D3    |       | |        |PWM
        | |I2C SDA|        |D18 / A4|20|┃ ◎               ┃|  |      |       | |        |    
        | |       |        |D17 / A3|21|┃◎               ◎┃| 5|D2    |       | |        |
        | |I2C SCL|        |D19 / A5|22|┃ ◎               ┃|  |      |       | |        |    
        | |       |        |5V      |23|┃◎               ▣┃| 4|Ground|       | |        |
        | |       |        |Reset   |24|┃◎               ◎┃| 3|Reset |       | |        |
        | |       |        |Ground  |25|┃▣               ◎┃| 2|D0    |       | |UART RX |
        | |       |        |Vin     |26|┃◎  ▣ ▣ ◎ ◎ ◎ ◎  ◎┃| 1|D1    |       | |UART TX |
        | |       |        |        |  |┗━━━╋━╋━╋━╋━╋━╋━━━┛|  |      |       | |        |
        | |       |        |        |  |    ┃ ┃ ┃ ┃ ┃ ┃    |  |      |       | |        |
        | |       |        |Ground  |31|━━━━┛ ┃ ┃ ┃ ┃ ┗━━━━|36|Reset |       | |        |
        | |       |        |Ground  |32|━━━━━━┛ ┃ ┃ ┗━━━━━━|35|      |       | |UART TX |
        | |       |        |5V      |33|━━━━━━━━┛ ┗━━━━━━━━|34|      |       | |UART RX |
""".splitlines()[1:]]

    GROUND = (4, 25, 31, 32)
    POWER = (23, 26, 33)
    ADC = (17, 18, 19, 20, 21, 22)
    RUN = (3, 24, 36)
    BOARD = 'Arduino Pro Mini ' + __version__

    LED = ((2, 3, "D13","highlight_r"),)
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)


board = prominipins()

def main():
    rich.print(board.display(Options(sys.argv)))

if __name__ == "__main__":
    main()
