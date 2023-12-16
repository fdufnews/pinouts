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
# ┏ ┓ ┗ ┛ ▂ ▁ ┃ ╹ ╻ ◎ ▣ ▩ ▒ ▓ └ ┘ ┌ ┐ ┬ ┴ ┼ ├ ┤ ─ │ ✅ ⛔
# ┏━━━━━┓ 
# ┫ USB ┣
# ┗━━━━━┛
class picopins(showpins):
#   PWM   | UART    |   I2C  |  SPI   | GPIO            |pin#|   DIAGRAM     |pin#| GPIO      |  SPI      |   I2C    | UART    | PWM
    PINOUT = [line.split("|") for line in """
          |         |        |        |                 |  |      ┏━━━━━┓      |  |           |           |          |         |
          |         |        |        |                 |  |┏━━━━━┫ USB ┣━━━━━┓|  |           |           |          |         |
          |         |        |        |Ground           |1 |┃▣    ┗━━━━━┛    ▣┃|36|Ground     |           |          |         |
          |         |        |        |5V               |2 |┃◎               ◎┃|35|5V         |           |          |         |
          |         |        |        |3V3              |3 |┃◎               ◎┃|33|3V3        |           |          |         |
          |         |        |        |RST              |4 |┃◎       GP25    ▣┃|33|Ground     |           |          |         |
  PWM ✅  |UART1 ✅ |I2C0/1 ✅|SPI ✅ |GP13/ADC2_4      |5 |┃◎         └──▩  ◎┃|32|GP1        |SPI ✅    |I2C0/1 ✅ |UART0 TX |PWM ✅
  PWM ✅  |UART1 ✅ |I2C0/1 ✅|SPI ✅ |GP12/ADC2_5      |6 |┃◎               ◎┃|31|GP3        |SPI ✅    |I2C0/1 ✅ |UART0 RX |PWM ✅
  PWM ✅  |UART1 ✅ |I2C0/1 ✅|SPI ✅ |GP14/ADC2_6      |7 |┃◎   ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|30|GP15/ADC2_3|SPI ✅    |OLED_SCL  |UART1 ✅ |PWM ✅
  PWM ✅  |UART1 ✅ |I2C0/1 ✅|SPI ✅ |GP27/ADC2_7      |8 |┃◎   ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|29|GP2/ADC2_2 |SPI ✅    |I2C0/1 ✅ |UART1 ✅ |PWM ✅
  PWM ✅  |UART1 ✅ |I2C0/1 ✅|SPI ✅ |GP26/ADC2_9/DAC2 |9 |┃◎   ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|28|GP0/ADC2_1 |SPI ✅    |I2C0/1 ✅ |UART1 ✅ |PWM ✅
  PWM ✅  |UART1 ✅ |I2C0/1 ✅|SPI ✅ |GP25/ADC2_8/DAC1 |10|┃◎   ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|27|GP4/ADC2_0 |SPI ✅    |OLED_SDA  |UART1 ✅ |PWM ✅
          |         |        |        |GP33*            |11|┃◎   ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|26|GP16       |SPI ✅     |OLED_RST |UART1 ✅  |PWM ✅
          |         |        |        |GP32*            |12|┃◎   ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|25|GP17       |SPI ✅     |I2C0/1 ✅|UART1 ✅  |PWM ✅
          |         |        |        |GP35*/ADC1_7     |13|┃◎   ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|24|GP5        |SPI ✅     |I2C0/1 ✅|UART1 ✅  |PWM ✅
          |         |        |        |GP34*/ADC1_6     |14|┃◎   ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|23|GP18       |SPI ✅     |I2C0/1 ✅|UART1 ✅  |PWM ✅
          |         |        |        |GP39*            |15|┃◎   ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|22|GP23       |SPI ✅     |I2C0/1 ✅|UART1 ✅  |PWM ✅
          |         |        |        |GP38*            |16|┃◎   ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|21|GP19       |SPI ✅     |I2C0/1 ✅|UART1 ✅  |PWM ✅
          |         |        |        |GP37*            |17|┃◎   ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|20|GP22       |SPI ✅     |I2C0/1 ✅|UART1 ✅  |PWM ✅
          |         |        |        |GP36*            |18|┃◎               ◎┃|19|GP21       |SPI ✅     |I2C0/1 ✅|UART1 ✅  |PWM ✅
          |         |        |        |                 |  |┗━━━┓▂▂▂▂▂▂▂▂▂┏━━━┛|  |           |           |        |           |
          |         |        |        |                 |  |   *input only     |  |           |           |        |           |
          |         |        |        |                 |  |   UART0 ==> USB   |  |           |           |        |           |
          |         |        |        |                 |  |✅ ==> can be any pin|  |           |           |        |           |
""".splitlines()[1:]]

# This list contains the ground pins
    GROUND = (1, 33, 36)
# This list contains the power pins
    POWER = (2, 3, 33, 35)
# This list contains the ADC pins
    ADC = (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 27, 28, 29, 30)
# This list contains the RUN/RESET pins
    RUN = (4,)
# This string contains the name of the board must end with a space
    BOARD = 'HELTEC WiFI_Kit_32 ' + __version__
# This list of list contains the LED(s)
# 1st item row of the LED
# 2nd item row of the GPIO that drives the LED
# 3rd item the name of the GPIO
# 4th item the name of the color used to blink the LED one of (highlight_r, highlight_g, highlight_b)
    LED = ((6, 5, "GP25","highlight_r"),)
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)

# instance of the class
board = picopins()

def main():
    rich.print(board.display(Options(sys.argv)))

if __name__ == "__main__":
    main()
