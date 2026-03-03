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

# Name of the class can be changed in that case the name in the instance in line 74 must be changed too
# suggested graphic symbols that can be used
# ┏ ┓ ┗ ┛ ┻ ┳ ▂ ▁ ┃ ╹ ╻ ◎ ▣ ▩ ▒ ▓ └ ┘ ┌ ┐ ┬ ┴ ┼ ├ ┤ ─ │ ✅ ⛔ ⚠️
# ➜ ▸ ▴ ▾ ◂ ← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ← ↑ → ↓ ↰ ↱ ↲ ↳ ↴ ↵ ↩ ↪ 
# ┏━━━━━┓ 
# ┫ USB ┣
# ┗━━━━━┛
class picopins(showpins):
#   PWM   | UART    |   I2C  |  SPI   | GPIO |pin#|   DIAGRAM   |pin#| GPIO     |  SPI   |   I2C  | UART    | PWM
    PINOUT = [line.split("|") for line in """
          |         |        |        |      |  |       Rear view      |  |          |        |        |         |
          |         |        |        |      |  |┏━━━━━━━━━━━━━━━━━━━━┓|  |          |        |        |         |
          |         |        |        |      |  |┃                    ┃|  |          |        |        |         |
          |         |        |        |3.3V  |1 |┃◎                  ▣┃|24|GND       |        |        |         |
PWM✅     |UART✅   |I2C✅   |SPI✅   |GP1   |2 |┃◎                  ▣┃|23|GND       |        |        |         |
PWM✅     |UART✅   |I2C✅   |SPI✅   |GP2   |3 |┃◎                  ◎┃|22|GP43      |SPI✅   |I2C✅   |UART✅   |PWM✅
PWM✅     |UART✅   |I2C✅   |SPI✅   |GP3   |4 |┃◎        ▓▓▓▓▓▓    ◎┃|21|GP44      |SPI✅   |I2C✅   |UART✅   |PWM✅
PWM✅     |UART✅   |I2C✅   |SPI CS  |GP10  |5 |┃◎        ▓▓▓▓▓▓    ◎┃|20|GP18      |SPI✅   |I2C✅   |U1_TXD   |PWM✅
PWM✅     |UART✅   |I2C✅   |SPI RX  |GP11  |6 |┃◎        ▓▓▓▓▓▓    ◎┃|19|GP17      |SPI✅   |I2C✅   |U1_RXD   |PWM✅
PWM✅     |UART✅   |I2C✅   |SPI CLK |GP12  |7 |┃◎                  ◎┃|18|GP21      |SPI✅   |I2C✅   |UART✅   |PWM✅
PWM✅     |UART✅   |I2C✅   |SPI TX  |GP13  |8 |┃◎                  ◎┃|17|GP16      |SPI✅   |I2C✅   |UART✅   |PWM✅
          |         |        |        |NC    |9 |┃◎                  ◎┃|16|NC        |        |        |         |
          |         |        |        |NC    |10|┃◎        ▒▒▒       ▣┃|15|GND       |        |        |         |
          |         |        |        |GND   |11|┃▣        ▒▒▒       ▣┃|14|GND       |        |        |         |
          |         |        |        |5V    |12|┃◎                  ◎┃|13|3.3V      |        |        |         |
          |         |        |        |      |  |┃                    ┃|  |          |        |        |         |
          |         |        |        |      |  |┃                    ┃|  |          |        |        |         |
          |         |        |        |      |  |┃                    ┃|  |          |        |        |         |
          |         |        |        |      |  |┃                    ┃|  |          |        |        |         |
          |         |        |        |      |  |┃           ▣ ◎ ◎ ◎  ┃|  |          |        |        |         |
          |         |        |        |      |  |┗━━━━━━━━━━━│━│━│━│━━┛|  |          |        |        |         |
          |         |        |        |GND   |25|────────────┘ │ │ └───|28|GP44      |        |        |         |
          |         |        |        |3.3V  |26|──────────────┘ └─────|27|GP43      |        |        |         |
          |         |        |        |      |  |                      |  |          |        |        |         |
          |         |        |        |      |  |✅ ==> can be on any pin|  |          |        |        |         |
""".splitlines()[1:]]

# This list contains the ground pins
    GROUND = (11, 14, 15, 23, 24,25)
# This list contains the power pins
    POWER = (1, 12, 13, 26)
# This list contains the ADC pins
    ADC = (1, 2, 3, 4, 5, 6, 7, 17, 19, 20)
# This list contains the RUN/RESET pins
    RUN = (30,)
# This string contains the name of the board must end with a space
    BOARD = 'Lilygo T-DISPLAY S3 ' + __version__
# This list of list contains the LED(s)
# 1st item line of the LED
# 2nd item line of the GPIO that drives the LED, one LED can be associated with multiple GPIO
# 3rd item the name of the GPIO
# 4th item the name of the color used to blink the GPIO name one of (highlight_r, highlight_g, highlight_b)
    LED = ()
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)

# instance of the class
board = picopins()

def main():
    rich.print(board.display(Options(sys.argv)))

if __name__ == "__main__":
    main()
