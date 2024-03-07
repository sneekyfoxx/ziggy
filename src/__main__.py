""" This file is the entry point into the program.
    Handles commandline arguments, importing all
    of the appropriate modules, and invoking all
    of the appropriate functions, classes, and methods.
"""
from ziggy import STDERR, ARGV, EXIT
from ziggy.ziggyOptions import ziggy_options
from ziggy.ziggyConfirm import ziggy_confirm

def main(args: list[str]) -> int:
    """ Entry point into program.
    """
    if ziggy_confirm() is False:
        STDERR(f"{RED}Platform Not Supported{RESET}\n")
        return 1
    else: 
        return ziggy_options(len(args), *args)

if __name__ == "__main__":
    returncode = main(ARGV[1:])
    EXIT(returncode)
