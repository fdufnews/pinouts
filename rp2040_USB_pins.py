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
# ┏ ┓ ┗ ┛ ┻ ┳ ▂ ▁ ┃ ╹ ╻ ◎ ▣ ▩ ▒ ▓ └ ┘ ┌ ┐ ┬ ┴ ┼ ├ ┤ ─ │ ✅ ⛔
# ➜ ▸ ▴ ▾ ◂ ← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ← ↑ → ↓ ↰ ↱ ↲ ↳ ↴ ↵ ↩ ↪ 
# ┏━━━━━┓ 
# ┫ USB ┣
# ┗━━━━━┛
class rp2040usbpins(showpins):
#   PWM   | UART    |   I2C  |  SPI   | GPIO |pin#|   DIAGRAM   |pin#| GPIO     |  SPI   |   I2C  | UART    | PWM
    PINOUT = [line.split("|") for line in """
          |         |        |        |      |  |   ┏━━━━━━━━━┓   |  |          |        |        |         |
          |         |        |        |      |  |   ┃ ▓ ▓ ▓ ▓ ┃   |  |          |        |        |         |
          |         |        |        |      |  |   ┃ ▓ ▓ ▓ ▓ ┃   |  |          |        |        |         |
          |         |        |        |      |  |   ┃ ▓ ▓ ▓ ▓ ┃   |  |          |        |        |         |
          |         |        |        |      |  |┏━━┛    GP22 ┗━━┓|  |          |        |        |         |
    PWM0 A|UART0 TX |I2C0 SDA|SPI0 RX |GP0   |1 |┃◎  ▒▒▒  │     ◎┃|18|VBUS      |        |        |         |
    PWM0 B|UART0 RX |I2C0 SCL|SPI0 CSn|GP1   |2 |┃◎  ▒▒▒  ▩     ▣┃|17|Ground    |        |        |         |
    PWM1 A|UART0 CTS|I2C1 SDA|SPI0 SCK|GP2   |3 |┃◎             ◎┃|16|3v3 Out   |        |        |         |
    PWM1 B|UART0 RTS|I2C1 SCL|SPI0 TX |GP3   |4 |┃◎   ▓▓▓▓▓▓▓   ◎┃|15|GP29 / A3 |SPI1 CSn|I2C0 SCL|UART0 RX |PWM6 B
    PWM2 A|UART1 TX |I2C0 SDA|SPI0 RX |GP4   |5 |┃◎   ▓▓▓▓▓▓▓   ◎┃|14|GP28 / A2 |SPI1 RX |I2C0 SDA|UART0 TX |PWM6 A
    PWM2 B|UART1 RX |I2C0 SCL|SPI0 CSn|GP5   |6 |┃◎   ▓▓▓▓▓▓▓   ◎┃|13|GP27 / A1 |SPI1 TX |I2C1 SCL|UART1 RTS|PWM5 B
    PWM3 A|UART1 CTS|I2C1 SDA|SPI0 SCK|GP6   |7 |┃◎             ◎┃|12|GP26 / A0 |SPI1 SCK|I2C1 SDA|UART1 CTS|PWM5 A
    PWM3 B|UART1 RTS|I2C1 SCL|SPI0 TX |GP7   |8 |┃◎  ┏━━━━━━━┓  ◎┃|11|GPIO15    |SPI1 TX |I2C1 SCL|UART0 RTS|PWM7 B
    PWM4 A|UART1 TX |I2C0 SDA|SPI1 RX |GP8   |9 |┃◎  ┃▣ ◎ ◎ ◎┃  ◎┃|10|GPIO14    |SPI1 SCK|I2C1 SDA|UART0 CTS|PWM7 A
          |         |        |        |      |  |┗━━━┻━━━━━━━┻━━━┛|  |          |        |        |         |
          |         |        |        |      |  |     │ │ │ │     |  |          |        |        |         |
          |         |        |        |Ground|32|─────┘ │ │ └─────|35|GPIO17    |SPI0 CSn|I2C0 SCL|UART0 RX |PWM0 B
          |         |        |        |3v3   |33|───────┘ └───────|34|GPIO16    |SPI0 RX |I2C0 SDA|UART0 TX |PWM0 A
          |         |        |        |      |  |                 |  |          |        |        |         |
          |         |        |        |      |  |    underside    |  |          |        |        |         |
    PWM4 B|UART1 RX |I2C0 SCL|SPI1 CSn|GP9   |19|┃   ◎       ◎   ┃|  |          |        |        |         |
    PWM5 A|UART1 CTS|I2C1 SDA|SPI1 SCK|GP10  |20|┃   ◎       ◎   ┃|31|GP25      |SPI1 CSn|I2C0 SCL|UART1 RX |PWM4 B
    PWM5 B|UART1 RTS|I2C1 SCL|SPI1 TX |GP11  |21|┃   ◎       ◎   ┃|30|GP24      |SPI1 RX |I2C0 SDA|UART1 TX |PWM4 A
    PWM6 A|UART0 TX |I2C0 SDA|SPI1 RX |GP12  |22|┃   ◎       ◎   ┃|29|GP23      |SPI0 TX |I2C1 SCL|UART1 RTS|PWM3 B
    PWM6 B|UART0 RX |I2C0 SCL|SPI1 CSn|GP13  |23|┃   ◎       ◎   ┃|28|GP22      |SPI0 SCK|I2C1 SDA|UART1 CTS|PWM3 A
    PWM1 A|UART0 CTS|I2C1 SDA|SPI0 SCK|GP18  |24|┃   ◎       ◎   ┃|27|GP21      |SPI0 CSn|I2C0 SCL|UART1 RX |PWM2 B
    PWM1 B|UART0 RTS|I2C1 SCL|SPI0 TX |GP19  |25|┃   ◎       ◎   ┃|26|GP20      |SPI0 RX |I2C0 SDA|UART1 TX |PWM2 A
          |         |        |        |      |  |                 |  |          |        |        |         |
""".splitlines()[1:]]

# This list contains the ground pins
    GROUND = (17,)
# This list contains the power pins
    POWER = (18, 16)
# This list contains the ADC pins
    ADC = (12, 13, 14, 15)
# This list contains the RUN/RESET pins
    RUN = ()
# This string contains the name of the board must end with a space
    BOARD = 'RP2040 USB ' + __version__
# This list of list contains the LED(s)
# 1st item line of the LED
# 2nd item line of the GPIO that drives the LED
# 3rd item the name of the GPIO
# 4th item the name of the color used to blink the GPIO name one of (highlight_r, highlight_g, highlight_b)
    LED = ((6, 4, "GP22","highlight_g"),)
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)

# instance of the class
board = rp2040usbpins()

def main():
    rich.print(board.display(Options(sys.argv)))

if __name__ == "__main__":
    main()
