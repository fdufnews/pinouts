#!/bin/env python3
import re
import sys

import rich
from rich.panel import Panel
from rich.table import Table

"""
xiaopins, by fdufnews based on @gadgetoid work

Support him:
https://ko-fi.com/gadgetoid
https://github.com/sponsors/Gadgetoid
https://www.patreon.com/gadgetoid

Shout-out to Raspberry Pi Spy for having almost this exact idea first:
https://www.raspberrypi-spy.co.uk/2022/12/pi-pico-pinout-display-on-the-command-line/
"""

__version__ = '1.0.0'

PINOUT = [line.split("|") for line in """
      |         |        |        |         |  |     ┏━━━━━┓     |  |       |        |        |         |
      |         |        |        |         |  |┏━━━━┫     ┣━━━━┓|  |       |        |        |         |
PWM5 A|UART1 CTS|I2C1 SDA|SPI1 SCK|GP26 / A0|1 |┃◎   ┗━━━━━┛   ◎┃|14|VBUS   |        |        |         |
PWM5 B|UART1 RTS|I2C1 SCL|SPI1 TX |GP27 / A1|2 |┃◎  GP16┬─┬──▩ ▣┃|13|Ground |        |        |         |
PWM6 A|UART0 TX |I2C0 SDA|SPI1 RX |GP28 / A2|3 |┃◎  GP17┘GP25  ◎┃|12|3v3 Out|        |        |         |
PWM6 B|UART0 RX |I2C0 SCL|SPI0 CSn|GP29 / A3|4 |┃◎ ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|11|GP3    |SPI0 TX |I2C1 SCL|UART0 RTS|PWM1 B
PWM3 A|UART1 CTS|I2C1 SDA|SPI0 SCK|GP6      |5 |┃◎ ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|10|GP4    |SPI0 RX |I2C0 SDA|UART1 TX |PWM2 A
PWM3 B|UART1 RTS|I2C1 SCL|SPI0 TX |GP7      |6 |┃◎ ▓▓▓▓▓▓▓▓▓▓▓ ◎┃|9 |GP2    |SPI0 SCK|I2C1 SDA|UART0 CTS|PWM1 A
PWM0 A|UART0 TX |I2C0 SDA|SPI0 RX |GP0      |7 |┃◎ (R)  ▩  (B) ◎┃|8 |GP1    |SPI0 CSn|I2C0 SCL|UART0 RX |PWM0 B
      |         |        |        |         |  |┃ GP11☀─┴─GP12  ┃|  |       |        |        |         |
      |         |        |        |         |  |┗━━━━━━━━━━━━━━━┛|  |       |        |        |         |
""".splitlines()[1:]]

LEFT_PINS = [[col.strip() for col in reversed(row[0:6])] for row in PINOUT]
RIGHT_PINS = [[col.strip() for col in row[7:]] for row in PINOUT]
DIAGRAM = [row[6] for row in PINOUT]

ROWS = len(LEFT_PINS)
COLS = ["pins", "gpio", "spi", "i2c", "uart", "pwm"]
COL_PIN_NUMS = 0
COL_GPIO = 1

LED_ROW = 3
LED2812_ROW = 8

THEME = {
    "gpio": "#859900",
    "pins": "#434343",
    "spi": "#d33682",
    "i2c": "#268bd2",
    "uart": "#6c71c4",
    "pwm": "#666666",
    "panel": "#ffffff on #000000",
    "panel_light": "#000000 on #fdf6e3",
    "diagram": "#555555",
    "adc": "#2aa198",
    "power": "#dc322f",
    "ground": "#005b66",
    "run": "#df8f8e",
    "highlight": "bold #dc322f on white",
    "highlight_r": "bold #dc322f on white",
    "highlight_v": "bold #20c020 on white",
    "highlight_b": "bold #3030dc on white",
    "highlight_row": "bold {fg} on #444444"
}


def usage(error=None):
    error = f"\n[red]Error: {error}[/]\n" if error else ""
    rich.print(f"""
[#859900]xiaopins[/] [#2aa198]v{__version__}[/] - a beautiful GPIO pinout and pin function guide for the XIAO RP2040
{error}
usage: xiaopins [--...] [--all] or {{{",".join(COLS[2:])}}} [--find <text>]
       --pins          - show physical pin numbers
       --all or {{{",".join(COLS[2:])}}} - pick list of interfaces to show
       --hide-gpio     - hide GPIO pins
       --light         - melt your eyeballs
       --find "<text>" - highlight pins matching <text>
                         supports regex if you're feeling sassy!

eg:    xiaopins i2c                    - show GPIO and I2C labels
       xiaopins                        - basic GPIO pinout
       xiaopins --all --find "PWM3 A"  - highlight any "PWM3 A" labels
       xiaopins --all --find "PWM.* A" - highlight any PWM A channels

web:   https://pico.pinout.xyz
bugs:  https://github.com/pinout-xyz/picopins
""")
    sys.exit(1 if error else 0)


def gpio_style(pin):
    if pin == 13: return "ground"
    if pin in (12, 14): return "power"
    if pin in (1, 2, 3, 4): return "adc"
    #if pin == 30: return "run"
    return "gpio"


def styled(label, style, fg=None):
    style = THEME[style]
    style = style.format(fg=fg)
    return f'[{style}]{label}[/]'


def search(pin, highlight):
    if not highlight:
        return False
    # Hack to make "--find adc" also find A0, A1, etc
    if highlight.lower() == "adc":
        highlight += "|a[0-9]"
    highlight = re.compile(highlight, re.I)
    # Match search term against pin label
    return re.search(highlight, pin) is not None


def build_pins(pins, show_indexes, highlight=None):
    # Find all labels including the highlight word
    search_highlight = [search(pin, highlight) for pin in pins]
    # See if any non-visble labels match
    has_hidden_results = True in [index not in show_indexes and value
                                  for index, value in enumerate(search_highlight)]
    # Get the phyical pin for special case GPIO highlighting
    physical_pin_number = int(pins[COL_PIN_NUMS]) if pins[COL_PIN_NUMS] != "" else None
    # Iterate through the visible labels
    for i in show_indexes:
        label = pins[i]
        if search_highlight[i]:
            yield styled(label, "highlight")
        elif i == COL_GPIO:  # GPn / VSYS etc
            # Special case for styling power, ground, GPn, run, etc
            style = gpio_style(physical_pin_number)
            # Highlight for a non-visible search result
            if has_hidden_results:
                yield styled(label, "highlight_row", fg=THEME[style])
            else:
                yield styled(label, style)
        else:
            # Table column styles will catch the rest
            yield label


def build_row(row, show_indexes, highlight=None):
    for pin in build_pins(LEFT_PINS[row], show_indexes, highlight):
        yield pin + " "
    yield " " + DIAGRAM[row]
    # We can't reverse a generator
    for pin in reversed(list(build_pins(RIGHT_PINS[row], show_indexes, highlight))):
        yield " " + pin


def xiaopins(opts):
    show_indexes = []
    grid = Table.grid(expand=True)

    for label in reversed(opts.show):
        grid.add_column(justify="left", style=THEME[label], no_wrap=True)
        show_indexes.append(COLS.index(label))

    if opts.show_gpio:
        grid.add_column(justify="right", style=THEME["gpio"], no_wrap=True)
        show_indexes.append(COL_GPIO)

    if opts.show_pins:
        grid.add_column(justify="right", style=THEME["pins"], no_wrap=True)
        show_indexes.append(COL_PIN_NUMS)

    grid.add_column(no_wrap=True, style=THEME["diagram"])

    if opts.show_pins:
        grid.add_column(justify="left", style=THEME["pins"], no_wrap=True)

    if opts.show_gpio:
        grid.add_column(justify="left", style=THEME["gpio"], no_wrap=True)

    for label in opts.show:
        grid.add_column(justify="left", style=THEME[label], no_wrap=True)

    if search("GP16 LED", opts.find):
        DIAGRAM[LED_ROW] = DIAGRAM[LED_ROW].replace("▩", "[blink red]▩[/]")
        DIAGRAM[LED_ROW ] = DIAGRAM[LED_ROW].replace("GP16", styled("GP16", "highlight_v"))
    if search("GP17 LED", opts.find):
        DIAGRAM[LED_ROW] = DIAGRAM[LED_ROW].replace("▩", "[blink red]▩[/]")
        DIAGRAM[LED_ROW + 1] = DIAGRAM[LED_ROW + 1].replace("GP17", styled("GP17", "highlight_r"))
    if search("GP25 LED", opts.find):
        DIAGRAM[LED_ROW] = DIAGRAM[LED_ROW].replace("▩", "[blink red]▩[/]")
        DIAGRAM[LED_ROW + 1] = DIAGRAM[LED_ROW + 1].replace("GP25", styled("GP25", "highlight_b"))
    if search("GP11 GP12 LED", opts.find):
        DIAGRAM[LED2812_ROW] = DIAGRAM[LED2812_ROW].replace("▩", "[blink red]▩[/]")
        DIAGRAM[LED2812_ROW + 1] = DIAGRAM[LED2812_ROW + 1].replace("GP11☀", styled("GP11☀", "highlight"))
    if search("GP12 LED", opts.find):
        DIAGRAM[LED2812_ROW] = DIAGRAM[LED2812_ROW].replace("▩", "[blink red]▩[/]")
        DIAGRAM[LED2812_ROW + 1] = DIAGRAM[LED2812_ROW + 1].replace("GP12", styled("GP12", "highlight"))

    for i in range(ROWS):
        grid.add_row(*build_row(i, show_indexes, highlight=opts.find))

    layout = Table.grid(expand=True)
    layout.add_row(grid)
    layout.add_row("fdufnews based on @gadgetoid work\nhttps://pico.pinout.xyz")

    return Panel(
        layout,
        title="XIAO RP2040 Pinout",
        expand=False,
        style=THEME["panel_light"] if opts.light_mode else THEME["panel"])


class Options():
    def __init__(self, argv):
        argv.pop(0)

        if "--help" in argv:
            usage()

        if "--version" in argv:
            print(f"{__version__}")
            sys.exit(0)

        self.all = "--all" in argv
        self.show_pins = "--pins" in argv
        self.show_gpio = "--hide-gpio" not in argv
        self.light_mode = "--light" in argv
        self.find = None

        if "--find" in argv:
            index = argv.index("--find") + 1
            if index >= len(argv) or argv[index].startswith("--"):
                usage("--find needs something to find.")
            self.find = argv.pop(index)

        # Assume any non -- args are labels
        self.show = [self.valid_label(arg) for arg in argv if not arg.startswith("--")]

        if self.show == [] and self.all:
            self.show = COLS[2:]
        elif self.all:
            usage("Please use either --all or a list of interfaces.")

    def valid_label(self, label):
        if label not in COLS[2:]:
            usage(f"Invalid interface \"{label}\".")
        return label


def main():
    rich.print(xiaopins(Options(sys.argv)))


if __name__ == "__main__":
    main()
