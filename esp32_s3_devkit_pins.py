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
# ADC  | FSPI    |TOUCH   |RTC | GPIO |pin#|   DIAGRAM    |pin#| GPIO     |  RTC   |  TOUCH | FSPI    | ADC
    PINOUT = [line.split("|") for line in """
       |         |       |    |      |  |  ┏━━━━━━━━━━━━━┓  |  |          |        |        |         |
       |         |       |    |      |  |┏━┫             ┣━┓|  |          |        |        |         |
       |         |       |    |3V3   |1 |┃◎┣━━━━━━━━━━━━━┫▣┃|44|GND       |        |        |         |
       |         |       |    |3V3   |2 |┃◎┃             ┃◎┃|43|GP43      |UART0_TX|        |         |
       |         |       |    |RST   |3 |┃◎┃             ┃◎┃|42|GP44      |UART0_RX|        |         |
 ADC1_3|         |TOUCH4 |RTC |GP4   |4 |┃◎┃             ┃◎┃|41|GP1       |        |        |         |
 ADC1_4|         |TOUCH5 |RTC |GP5   |5 |┃◎┃             ┃◎┃|40|GP2       |RTC     |TOUCH1  |         |ADC1_0
 ADC1_5|         |TOUCH6 |RTC |GP6   |6 |┃◎┃             ┃◎┃|39|GP42      |RTC     |TOUCH2  |         |ADC1_1
 ADC1_6|         |TOUCH7 |RTC |GP7   |7 |┃◎┃             ┃◎┃|38|GP41      |        |        |         |
 ADC2_4|         |       |RTC |GP15  |8 |┃◎┗━━━━━━━━━━━━━┛◎┃|37|GP40      |        |        |         |
 ADC2_5|         |       |RTC |GP16  |9 |┃◎           RST ◎┃|36|GP39      |        |        |         |
 ADC2_6|         |       |RTC |GP17  |10|┃◎           \[o] ◎┃|35|GP38      |        |        |         |
 ADC2_7|         |       |RTC |GP18  |11|┃◎          BOOT ◎┃|34|GP37 ⚠️   |        |        |FSPIWP   |
 ADC1_7|         |TOUCH8 |RTC |GP8   |12|┃◎           \[o] ◎┃|33|GP36 ⚠️   |        |        |FSPIQ    |
 ADC1_2|         |TOUCH3 |RTC |GP3   |13|┃◎               ◎┃|32|GP35 ⚠️   |        |        |FSPICLK  |
       |         |       |    |GP46  |14|┃◎       PWR  RX ◎┃|31|GP0       |        |        |FSPID    |
 ADC1_8|FSPIHD   |TOUCH9 |RTC |GP9   |15|┃◎ ▩       ▒ ▓ ▓ ◎┃|30|GP45      |        |        |         |
 ADC1_9|FSPICS0  |TOUCH10|RTC |GP10  |16|┃◎ └─GP48   TX   ◎┃|29|GP48      |        |        |         |
 ADC2_0|FSPID    |TOUCH11|RTC |GP11  |17|┃◎               ◎┃|28|GP47      |        |        |         |
 ADC2_1|FSPICLK  |TOUCH12|RTC |GP12  |18|┃◎               ◎┃|27|GP21      |RTC     |        |         |
 ADC2_2|FSPIQ    |TOUCH13|RTC |GP13  |19|┃◎               ◎┃|26|USB_D+    |RTC     |        |         |ADC2_9
 ADC2_3|FSPIWP   |TOUCH14|RTC |GP14  |20|┃◎               ◎┃|25|USB_D-    |RTC     |        |         |ADC2_8
       |         |       |    |5V0   |21|┃◎┏━━━━━┓ ┏━━━━━┓▣┃|24|GND       |        |        |         |
       |         |       |    |GND   |22|┃▣┃     ┃ ┃     ┃▣┃|23|GND       |        |        |         |
       |         |       |    |      |  |┗━┫     ┣━┫     ┣━┛|  |          |        |        |         |
       |         |       |    |      |  |  ┗━━━━━┛ ┗━━━━━┛  |  |          |        |        |         |
No ADC2|         |       |    |      |  |⚠️  used by Octal SPIRAM  |  |          |        |        |         |
when WiFi|         |       |    |      |  |   SPI on any pin  |  |          |        |        |         |
is active|         |       |    |      |  |   PWM on any pin  |  |          |        |        |         |
       |         |       |    |      |  |   I2C on any pin  |  |          |        |        |         |
""".splitlines()[1:]]

# This list contains the ground pins
    GROUND = (22, 23, 24, 44)
# This list contains the power pins
    POWER = (1, 2, 21)
# This list contains the ADC pins
    ADC = (4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,20,25,26,39,40)
# This list contains the RUN/RESET pins
    RUN = (3,)
# This string contains the name of the board must end with a space
    BOARD = 'ESP32-S3 devkitC-1 ' + __version__
# This list of list contains the LED(s)
# 1st item line of the LED
# 2nd item line of the GPIO that drives the LED, one LED can be associated with multiple GPIO
# 3rd item the name of the GPIO
# 4th item the name of the color used to blink the GPIO name one of (highlight_r, highlight_g, highlight_b)
    LED = ((16, 17, "GP48","highlight_r"),)
            
    def __init__(self):
        showpins.__init__(self, self.BOARD, self.PINOUT, self.GROUND, self.POWER, self.ADC, self.RUN, self.LED)

# instance of the class
board = picopins()

def main():
    rich.print(board.display(Options(sys.argv)))

if __name__ == "__main__":
    main()
