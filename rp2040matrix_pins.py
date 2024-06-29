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

__version__ = '1.0'
# suggested graphic symbols that can be used
# ┏ ┓ ┗ ┛ ▂ ▁ ┃ ╹ ╻ ◎ ▣ ▩ ▒ ▓ └ ┘ ┌ ┐ ┬ ┴ ┼ ├ ┤ ─ │ ✅ ⛔
# ┏━━━━━┓ 
# ┫ USB ┣
# ┗━━━━━┛

class rp2040matrix(showpins):
    

    PINOUT = [line.split("|") for line in """
          |         |        |        |         |  |     ┏━━━━━┓     |  |       |        |        |         |
          |         |        |        |         |  |┏━━━━┫     ┣━━━━━┓|  |       |        |        |         |
          |         |        |        |5V       |1 |┃◎   ┗━━━━━┛   ◎ ┃ |18|GP0    |SPI0 RX |I2C0 SDA|UART0 TX|PWM0 A
          |         |        |        |GND      |2 |┃▣  GP16┐      ◎ ┃ |17|GGP1   |SPI0 CSn|I2C0 SCL|UART0 RX|PWM0 B
          |         |        |        |3V3      |3 |┃◎      │      ◎ ┃ |16|GP2    |SPI0 SCK|I2C1 SDA|UART0 CTS|PWM1 A
    PWM6 B|UART0 RX |I2C0 SCL|SPI1 CSn|GP29 / A3|4 |┃◎  ▩ ▩ ▩ ▩ ▩  ◎ ┃|15|GP3    |SPI0 TX |I2C1 SCL|UART0 RTS|PWM1 B
    PWM6 A|UART0 TX |I2C0 SDA|SPI1 RX |GP28 / A2|5 |┃◎  ▩ ▩ ▩ ▩ ▩  ◎ ┃|14|GP4    |SPI0 RX |I2C0 SDA|UART1 TX |PWM2 A
    PWM5 B|UART1 RTS|I2C1 SCL|SPI1 TX |GP27 / A1|6 |┃◎  ▩ ▩ ▩ ▩ ▩  ◎ ┃|13 |GP5    |SPI0 CSn|I2C0 SCLA|UART1 RX |PWM2 B
    PWM5 A|UART1 CTS|I2C1 SDA|SPI1 SCK|GP26 / A0|7 |┃◎  ▩ ▩ ▩ ▩ ▩  ◎ ┃|12|GP6    |SPI0 SCK|I2C1 SDA|UART1 CTS|PWM3 A
    PWM7 B|UART1 RTS|I2C1 SCL|SPI1 TX |GP15     |8 |┃◎  ▩ ▩ ▩ ▩ ▩  ◎ ┃|11|GP7    |SPI0 TX |I2C1 SCL|UART1 RTS|PWM3 B
    PWM7 A|UART0 CTS|I2C1 SDA|SPI1 SCK |GP14     |9 |┃◎             ◎ ┃|10|GP8    |SPI1 RX |I2C0 SDA|UART1 TX |PWM4 A
         |           |       |         |         |  |┗━━━╋━╋━╋━╋━╋━━━━┛|  |      |       | |        |
         |           |       |         |         |  |    ┃ ┃ ┃ ┃ ┃      |  |      |       | |        |
   PWM6 B|UART0 RX |I2C0 SCL|SPI1 CSn|GP13   |19|━━━━┛ ┃ ┃ ┃ ┃      | |  |       | |        |
   PWM6 A|UART0 TX |I2C0 SDA|SPI1 RX |GP12   |20|━━━━━━┛ ┃ ┃ ┗━━━━━━|23| GP9 |SPI1 CSn|I2C0 SCL |UART1 RX |PWM4 B
   PWM5 B|UART1 RTS|I2C1 SCL|SPI1 TX |GP11       |21|━━━━━━━━┛ ┗━━━━━━━━|22| GP10  |SPI1 SCK|I2C1 SDA |UART1 CTS|PWM5 A
          |         |        |        |         |  |   Matrix of 25    |  |       |        |        |         |
          |         |        |        |         |  | WS2812B RGB LEDs |  |       |        |        |         |
""".splitlines()[1:]]


    GROUND = (2,)
    POWER = (1, 3)
    ADC = (4,5,6,7)
    RUN = ()
    BOARD = 'RP2040 MATRIX ' + __version__

    LED = ((5,3,"GP16","highlight_r"),
            (6,3,"GP16","highlight_r"),
            (7,3,"GP16","highlight_r"),
            (8,3,"GP16","highlight_r"),
            (9,3,"GP16","highlight_r"))
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)


board = rp2040matrix()

def main():
    rich.print(board.display(Options(sys.argv)))

if __name__ == "__main__":
    main()
