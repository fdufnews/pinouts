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
#   ADC   | SPI     |  TOUCH |  RTC   | GPIO |pin#|     DIAGRAM      |pin#| GPIO |  RTC   |  TOUCH |  SPI    | ADC
    PINOUT = [line.split("|") for line in """
          |         |        |        |      |  |    ┏━━━━━━━━━━━━┓    |  |      |        |        |         |
          |         |        |        |      |  |┏━━━┫            ┣━━━┓|  |      |        |        |         |
          |         |        |        |GND   |20|┃▣ ◎┣━━━━━━━━━━━━┫◎ ▣┃|39|GND   |        |        |         |
          |         |        |        |NC    |18|┃◎ ◎┃            ┃◎ ◎┃|37|GP17  |RTC     |TOUCH   |         |ADC2_7
    ADC1_3|         |        |RTC     |GP39  |16|┃◎ ◎┃            ┃◎ ◎┃|35|GP25  |RTC     |        |         |ADC2_8
    ADC1_7|         |        |RTC     |GP35  |14|┃◎ ◎┃            ┃◎ ◎┃|33|GP32  |RTC     |TOUCH   |         |ADC1_4
    ADC1_5|         |TOUCH   |RTC     |GP33  |12|┃◎ ◎┃            ┃◎ ◎┃|31|GP12  |RTC     |TOUCH   |HSPIQ    |ADC2_5
    ADC1_6|         |        |RTC     |GP34  |10|┃◎ ◎┃            ┃◎ ◎┃|29|GP4   |RTC     |TOUCH   |HSPIHD   |ADC2_0
    ADC2_6|HSPICLK  |TOUCH   |RTC     |GP14  |8 |┃◎ ◎┃            ┃▣ ◎┃|27|GP0   |RTC     |TOUCH   |         |ADC2_1
          |         |        |        |NC    |6 |┃◎ ▣┗━━━━━━━━━━━━┛◎ ◎┃|25|GP2   |RTC     |TOUCH   |HSPIWP   |ADC2_2
          |SPIHD    |        |        |GP9   |4 |┃◎ ◎              ◎ ◎┃|23|GP8   |        |        |SPID     |
          |SPICS0   |        |        |GP11  |2 |┃◎ ◎              ◎ ◎┃|21|GP6   |        |        |SPICLK   |
          |         |        |        |      |  |┃  ┃        GP2━━━ ▩ ┃|  |      |        |        |         |
          |         |        |        |      |  |┃  ┃    ┏━━━━━┓   ┃  ┃|  |      |        |        |         |
          |         |        |        |      |  |┗━━┃━━━━┫ USB ┣━━━┃━━┛|  |      |        |        |         |
          |         |        |        |      |  |   ┃    ┗━━━━━┛   ┃   |  |      |        |        |         |
          |         |        |        |      |  |   ▾              ▾  ┃|  |      |        |        |         |
          |         |        |        |RST   |19|┃  ◎              ◎  ┃|40|GP1   |UART0_RX|        |         |
    ADC1_0|         |        |RTC     |GP36  |17|┃  ◎              ◎  ┃|38|GP3   |UART0_TX|        |         |
    ADC2_9|         |        |RTC     |GP26  |15|┃  ◎              ◎  ┃|36|GP22  |        |        |VSPIWP   |
          |VSPICLK  |        |        |GP18  |13|┃  ◎              ◎  ┃|34|GP21  |        |        |VSPIHD   |
          |VSPIQ    |        |        |GP19  |11|┃  ◎              ◎  ┃|32|GP17  |        |        |         |
          |VSPID    |        |        |GP23  |9 |┃  ◎              ◎  ┃|30|GP16  |        |        |         |
          |VSPICS0  |        |        |GP5   |7 |┃  ◎              ▣  ┃|28|GND   |        |        |         |
          |         |        |        |3V3   |5 |┃  ▣              ▣  ┃|26|VCC   |        |        |         |
    ADC2_4|HSPID    |TOUCH   |RTC     |GP13  |3 |┃  ◎              ◎  ┃|24|GP15  |HSPICS0 |TOUCH   |         |ADC2_3
          |SPIWP    |        |        |GP10  |1 |┃  ◎              ◎  ┃|22|GP7   |        |        |SPIQ     |
          |         |        |        |      |  |                      |  |      |        |        |         |
No ADC2   |         |        |        |      |  |    I2C on any PIN    |  |      |        |        |         |
when WiFi |         |        |        |      |  |    PWM on any PIN    |  |      |        |        |         |
is active |         |        |        |      |  |    SPI on any PIN    |  |      |        |        |         |
          |         |        |        |      |  |                      |  |      |        |        |         |
""".splitlines()[1:]]

# This list contains the ground pins
    GROUND = (20, 28, 39)
# This list contains the power pins
    POWER = (5, 26)
# This list contains the ADC pins
    ADC = (3,8,10,12,14,15,16,17,24,25,27,29,31,33,35,37)
# This list contains the RUN/RESET pins
    RUN = (19,)
# This string contains the name of the board must end with a space
    BOARD = 'ESP32 MH-ET live D1 mini ' + __version__
# This list of list contains the LED(s)
# 1st item line of the LED
# 2nd item line of the GPIO that drives the LED, one LED can be associated with multiple GPIO
# 3rd item the name of the GPIO
# 4th item the name of the color used to blink the GPIO name one of (highlight_r, highlight_g, highlight_b)
    LED = ((12, 12, "GP2","highlight_r"),)
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)

# instance of the class
board = picopins()

def main():
    rich.print(board.display(Options(sys.argv)))

if __name__ == "__main__":
    main()
