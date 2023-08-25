#!/bin/env python3
import re
import sys

import rich
from rich.panel import Panel
from rich.table import Table

"""
showpins, by fdufnews based on @gadgetoid work

Support him:
https://ko-fi.com/gadgetoid
https://github.com/sponsors/Gadgetoid
https://www.patreon.com/gadgetoid

Shout-out to Raspberry Pi Spy for having almost this exact idea first:
https://www.raspberrypi-spy.co.uk/2022/12/pi-pico-pinout-display-on-the-command-line/
"""
__version__ = '1.0.0'


COLS = ["pins", "gpio", "spi", "i2c", "uart", "pwm"]


class showpins(object):


    COL_PIN_NUMS = 0
    COL_GPIO = 1

            
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



    def usage(self, appname, error=None):
        error = f"\n[red]Error: {error}[/]\n" if error else ""
        rich.print(f"""
    [#859900]{appname}[/] [#2aa198]v{__version__}[/] - a beautiful GPIO pinout and pin function guide
    {error}
    usage: {appname} [--...] [--all] or {{{",".join(COLS[2:])}}} [--find <text>]
           --pins          - show physical pin numbers
           --all or {{{",".join(COLS[2:])}}} - pick list of interfaces to show
           --hide-gpio     - hide GPIO pins
           --light         - melt your eyeballs
           --find "<text>" - highlight pins matching <text>
                             supports regex if you're feeling sassy!

    eg:    {appname} i2c                    - show GPIO and I2C labels
           {appname}                        - basic GPIO pinout
           {appname} --all --find "PWM3 A"  - highlight any "PWM3 A" labels
           {appname} --all --find "PWM.* A" - highlight any PWM A channels

    web:   https://pico.pinout.xyz
    bugs:  https://github.com/pinout-xyz/picopins
    """)
        sys.exit(1 if error else 0)


    def gpio_style(self, pin):
        if pin in self.GROUND: return "ground"
        if pin in self.POWER: return "power"
        if pin in self.ADC: return "adc"
        if pin in self.RUN: return "run"
        return "gpio"


    def styled(self, label, style, fg=None):
        style = self.THEME[style]
        style = style.format(fg=fg)
        return f'[{style}]{label}[/]'


    def search(self, pin, highlight):
        if not highlight:
            return False
        # Hack to make "--find adc" also find A0, A1, etc
        if highlight.lower() == "adc":
            highlight += "|a[0-9]"
        highlight = re.compile(highlight, re.I)
        # Match search term against pin label
        return re.search(highlight, pin) is not None


    def build_pins(self, pins, show_indexes, highlight=None):
        # Find all labels including the highlight word
        search_highlight = [self.search(pin, highlight) for pin in pins]
        # See if any non-visble labels match
        has_hidden_results = True in [index not in show_indexes and value
                                      for index, value in enumerate(search_highlight)]
        # Get the phyical pin for special case GPIO highlighting
        physical_pin_number = int(pins[self.COL_PIN_NUMS]) if pins[self.COL_PIN_NUMS] != "" else None
        # Iterate through the visible labels
        for i in show_indexes:
            label = pins[i]
            if search_highlight[i]:
                yield self.styled(label, "highlight")
            elif i == self.COL_GPIO:  # GPn / VSYS etc
                # Special case for styling power, ground, GPn, run, etc
                style = self.gpio_style(physical_pin_number)
                # Highlight for a non-visible search result
                if has_hidden_results:
                    yield self.styled(label, "highlight_row", fg=self.THEME[style])
                else:
                    yield self.styled(label, style)
            else:
                # Table column styles will catch the rest
                yield label


    def build_row(self, row, show_indexes, highlight=None):
        for pin in self.build_pins(self.LEFT_PINS[row], show_indexes, highlight):
            yield pin + " "
        yield " " + self.DIAGRAM[row]
        # We can't reverse a generator
        for pin in reversed(list(self.build_pins(self.RIGHT_PINS[row], show_indexes, highlight))):
            yield " " + pin

    def __init__(self, board, pinout, ground, power, adc, run, led):
        self.BOARD  = board 
        self.PINOUT = pinout
        self.GROUND = ground
        self.POWER  = power
        self.ADC    = adc
        self.RUN    = run
        self.LED    = led
        self.LEFT_PINS = [[col.strip() for col in reversed(row[0:6])] for row in self.PINOUT]           
        self.RIGHT_PINS = [[col.strip() for col in row[7:]] for row in self.PINOUT]
        
        self.DIAGRAM = [row[6] for row in self.PINOUT]
        self.ROWS = len(self.LEFT_PINS)
        
    def display(self, opts):
        show_indexes = []
        grid = Table.grid(expand=True)

        for label in reversed(opts.show):
            grid.add_column(justify="left", style=self.THEME[label], no_wrap=True)
            show_indexes.append(COLS.index(label))

        if opts.show_gpio:
            grid.add_column(justify="right", style=self.THEME["gpio"], no_wrap=True)
            show_indexes.append(self.COL_GPIO)

        if opts.show_pins:
            grid.add_column(justify="right", style=self.THEME["pins"], no_wrap=True)
            show_indexes.append(self.COL_PIN_NUMS)

        grid.add_column(no_wrap=True, style=self.THEME["diagram"])

        if opts.show_pins:
            grid.add_column(justify="left", style=self.THEME["pins"], no_wrap=True)

        if opts.show_gpio:
            grid.add_column(justify="left", style=self.THEME["gpio"], no_wrap=True)

        for label in opts.show:
            grid.add_column(justify="left", style=self.THEME[label], no_wrap=True)

        for listLED in self.LED:
            if self.search(listLED[2] + ' LED', opts.find):
                self.DIAGRAM[listLED[0]] = self.DIAGRAM[listLED[0]].replace("▩", "[blink red]▩[/]")
                self.DIAGRAM[listLED[1]] = self.DIAGRAM[listLED[1]].replace(listLED[2], self.styled(listLED[2], listLED[3]))

        for i in range(self.ROWS):
            grid.add_row(*self.build_row(i, show_indexes, highlight=opts.find))

        layout = Table.grid(expand=True)
        layout.add_row(grid)
        layout.add_row("fdufnews based on @gadgetoid work\nhttps://pico.pinout.xyz")

        return Panel(
            layout,
            title= self.BOARD + " Pinout",
            expand=False,
            style=self.THEME["panel_light"] if opts.light_mode else self.THEME["panel"])


class Options():
    def __init__(self, argv):
        self.appname = argv[0]
        argv.pop(0)
        if "--help" in argv:
            showpins.usage(None, self.appname )

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
                showpins.usage(None, self.appname, "--find needs something to find.")
            self.find = argv.pop(index)

        # Assume any non -- args are labels
        self.show = [self.valid_label(arg) for arg in argv if not arg.startswith("--")]

        if self.show == [] and self.all:
            self.show = COLS[2:]
        elif self.all:
            showpins.usage(None, self.appname, "Please use either --all or a list of interfaces.")

    def valid_label(self, label):
        if label not in COLS[2:]:
            showpins.usage(None, self.appname, f"Invalid interface \"{label}\".")
        return label

if __name__ == "__main__":
    print("""\n\nThis code is not supposed to be executed alone.
It is part of files displaying development boards pinout.
The program you should execute are picopins.py, xiaopins.py and so on.\n""")
