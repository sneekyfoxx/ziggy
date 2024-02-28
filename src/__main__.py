""" This file is the entry point into the program.
    Handles commandline arguments, importing all
    of the appropriate modules, and invoking all
    of the appropriate functions, classes, and methods.
"""

from . import ziggy
from ziggyConfirm import ziggy_confirm

def main(args: list[str]) -> int:
    """ Entry point into program.
    """
    if ziggy_confirm() is False:
        sys.stderr.write("\x1b[1;31mPlatform Not Supported\x1b[0m\n")
        return 1
    pass

if __name__ == "__main__":
    returncode = main(sys.argv[1:])
    sys.exit(returncode)
