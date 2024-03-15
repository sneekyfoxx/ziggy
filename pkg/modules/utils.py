""" Utility functions for simplifying 'ziggy' operations. """

import sys
import platform
from os.path import exists, expanduser

def output(message: str, /, mode: str = 'normal', exitcode: int = 0) -> int:
    """ Output a specified message based on a given mode.
        Return an exit code if specified otherwise return 0.
        The exit code must be a value in the range 0-2 (inclusive).
        
        Modes:
            normal  - prints to standard output (cyan)
            success - prints to standard output (green)
            error   - prints to standard error  (red)
            warn    - prints to standard output (yellow)
    """
    if not isinstance(message, str):
        raise SystemExit(f"[<function output>] expected 'message: str' recieved 'message: {type(message).__name__}'")
    
    if not isinstance(mode, str):
        raise SystemExit(f"[<function output>] expected 'mode: str' recieved 'mode: {type(mode).__name__}'")
    
    if not isinstance(exitcode, int):
        raise SystemExit(f"[<function output>] expected 'exitcode: int' recieved exitcode: {type(exitcode).__name__}'")
    
    if not (0 <= exitcode <= 2):
        raise SystemExit(f"[<function output>] expected 'exitcode=(0 <= n <= 2)' recieved 'exitcode={exitcode}'")
    
    red = "\x1b[1;31m"
    green = "\x1b[1;32m"
    yellow = "\x1b[1;33m"
    cyan = "\x1b[1;36m"
    reset = "\x1b[0m"
    
    match mode:
        case 'normal':
            sys.stdout.write(f"{cyan}{message}{reset}\n")
        case 'success':
            sys.stdout.write(f"{green}{message}{reset}\n")
        case 'error':
            sys.stderr.write(f"{red}{message}{reset}\n")
        case 'warn':
            sys.stdout.write(f"{yellow}{message}{reset}\n")
        case _:
            raise SystemExit(f"[<function output>] expected 'mode=normal|success|error|warn' recieved 'mode={mode}'")
    
    return exitcode

def set_attributes(function: callable, /) -> callable:
    """ Set the attributes on the 'constants' function.
    """
    if not callable(function):
        raise SystemExit(f"[<function set_attributes>] expected 'function: callable'")
    elif not type(function).__name__ == 'function':
        raise SystemExit(f"[<function set_attributes>] expected 'function: <class function>' got 'function: {type(function)}'")
    elif not function.__name__ == 'constants':
        raise SystemExit(f"[<function set_attributes>] expected 'function.__name__=callable' got 'function.__name__={function.__name__}'")
    else:
        current_platform = platform.system().lower()
        function.base_url = 'https://ziglang.org/download'
        function.dev_url = 'https://ziglnag.org/builds'
        function.versions = list()

        if current_platform == 'windows':
            function.ziggy = f'{expanduser("~")}\\\\.ziggy'
            function.symlink = f'{expanduser("~")}\\\\zig'
            function.separator = '\\\\'
            function.extension = '.zip'
            function.redirect = '2 > null'
            function.extract = 'unzip'
            function.link = 'mklink'
            function.unlink = 'del'
            function.move = 'move'
            function.remove = 'rmdir'
        elif current_platform in {'darwin', 'freebsd', 'linux'}:
            function.ziggy = f'{expanduser("~")}/.ziggy'
            function.symlink = '/usr/bin/zig'
            function.separator = '/'
            function.extension = '.tar.xz'
            function.redirect = '2 > /dev/null'
            function.extract = 'tar xJf'
            function.link = 'sudo ln -s'
            function.unlink = 'sudo unlink'
            function.move = 'mv'
            function.remove = 'rm -r --interactive=never'
        else:
            raise systemExit(f"Unsupported Platform: '{current_platform}'")
    
    return function

@set_attributes
def constants() -> callable:
    """ Contain all platform specific constants for operations
        pertaining to the current platform.
    """    
    return constants