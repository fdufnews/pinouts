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

class teensylcpins(showpins):

    PINOUT = [line.split("|") for line in """
        |         |       |        |        |  |      ┏━━━━━┓      |  |         |         |        |        |
        |         |       |        |        |  |┏━━━━━┫ USB ┣━━━━━┓|  |         |         |        |        |
        |         |       |        |Ground  | 1|┃▣    ┗━━━━━┛    ◎┃|28|VIN      |         |        |        |
        |UART1 RX |       |SPI1 TX |D0      | 2|┃◎               ▣┃|27|Ground   |         |        |        |
        |UART1 TX |       |SPI1 RX |D1      | 3|┃◎               ◎┃|26|3V3      |         |        |        |
        |         |       |        |D2      | 4|┃◎               ◎┃|25|D23 / A9 |         |I2C1 SDA|        |PWM
    PWM |UART1 RX |       |        |D3      | 5|┃◎               ◎┃|24|D22 / A8 |         |I2C1 SCL|        |PWM
    PWM |UART1 TX |       |        |D4      | 6|┃◎               ◎┃|23|D21 / A7 |SPI1 TX  |        |UART1 RX|
        |UART1 TX |       |SPI1 RX |D5      | 7|┃◎               ◎┃|22|D20 / A6 |SPI1 CLK |        |UART3 TX|PWM
    PWM |UART3 RX |       |SPI1 SS |D6      | 8|┃◎     ▓▓▓▓▓     ◎┃|21|D19 / A5 |         |I2C0 SCL|        |    
        |UART3 RX |       |SPI0 TX |D7      | 9|┃◎   ▓▓▓▓▓▓▓▓▓   ◎┃|20|D18 / A4 |         |I2C0 SDA|        |
        |UART3 TX |       |SPI0 RX |D8      |10|┃◎ ▓▓▓▓▓▓▓▓▓▓▓▓▓ ◎┃|19|D17 / A3 |         |I2C0 SDA|        |PWM
    PWM |UART2 RX |       |        |D9      |11|┃◎   ▓▓▓▓▓▓▓▓▓   ◎┃|18|D16 / A2 |         |I2C0 SCL|        |PWM
    PWM |UART2 TX |       |SPI0 SS |D10     |12|┃◎     ▓▓▓▓▓     ◎┃|17|D15 / A1 |         |        |        |
        |         |       |SPI0 TX |D11     |13|┃◎       D13━━▩  ◎┃|16|D14 / A0 |SPI0 CLK |        |        |
        |         |       |SPI0 RX |D12     |14|┃◎   ◎ ◎ ▣ ◎ ◎   ◎┃|15|D13      |SPI0 CLK |        |        |
        |         |       |        |        |  |┗━━━━╋━╋━╋━╋━╋━━━━┛|  |         |         |        |        |
        |         |       |        |        |  |     ┃ ┃ ┃ ┃ ┃     |  |         |         |        |        |
        |         |       |        |D17 @VIN|30|━━━━━┛ ┃ ┃ ┃ ┃     |  |         |         |        |        |
        |         |       |        |3V3     |31|━━━━━━━┛ ┃ ┃ ┗━━━━━|34|D26 / A12 / DAC|   |        |        |
        |         |       |        |Ground  |32|━━━━━━━━━┛ ┗━━━━━━━|33|Program  |         |        |        |
""".splitlines()[1:]]

    GROUND = (1, 27, 32)
    POWER = (26, 28, 31)
    ADC = (16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 34)
    RUN = ()
    BOARD = 'Teensy LC ' + __version__

    LED = ((14, 14, "D13","highlight_r"),)
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)


board = teensylcpins()

def main():
    rich.print(board.display(Options(sys.argv)))

if __name__ == "__main__":
    main()
