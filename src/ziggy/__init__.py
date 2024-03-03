""" This file will expose all of the necessary
    modules to `__main__.py` when importing
    the `ziggy` package.
"""

import os
import sys
from pathlib import Path
import platform
import subprocess
from re import findall

RED = "\x1b[1;31m"
GREEN = "\x1b[1;32m"
BLUE = "\x1b[1;34m"
PURPLE = "\x1b[1;35m"
WHITE = "\x1b[1;37m"
RESET = "\x1b[0m"

EXISTS = os.path.exists
EXPANDUSER = os.path.expanduser

ARGV = sys.argv
STDOUT = sys.stdout.write
STDERR = sys.stderr.write
EXIT = sys.exit

PATH = Path
SCANDIR = os.scandir

SYSTEM = platform.system
MACHINE = platform.machine

RUN = subprocess.run

FIND = findall

try:
    from requests import request
    from requests.exceptions import ConnectionError
    from bs4 import BeautifulSoup
except (ImportError, ModuleNotFoundError):
    STDERR(f"'{WHITE}requests{RESET}' and '{WHITE}BeautifulSoup4{RESET}' {RED}are required packages{RESET}\n")
    EXIT(1)

REQUEST = request
REQ_ERROR = ConnectionError
SCRAPER = BeautifulSoup
