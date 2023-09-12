import os
import random

import pyfiglet
from colorama import Fore

lg = Fore.LIGHTGREEN_EX
rs = Fore.RESET
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN

info = lg + "(" + w + "i" + lg + ")" + rs
error = lg + "(" + r + "!" + lg + ")" + rs
success = w + "(" + lg + "+" + w + ")" + rs
INPUT = lg + "(" + cy + "~" + lg + ")" + rs
colors = [lg, w, r, cy]


def banner():
    f = pyfiglet.Figlet(font="slant")
    logo = f.renderText("Tele Adder")
    print(random.choice(colors) + logo + rs)


def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
