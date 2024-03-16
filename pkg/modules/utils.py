""" Utility functions for simplifying 'ziggy' operations. """

import sys
import platform
import asyncio
import subprocess
from os.path import exists, expanduser
from pathlib import Path

try:
    import requests
except ModuleNotFoundError:
    raise SystemExit(f"[{__FILE__}] failed to import 'requests'")

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise SystemExit(f"[{__FILE__}] failed to import 'BeautifulSoup'")

constants = dict({
    'versions': list(),
    'version': '',
    'dirname': '',
    'ziggy': '',
    'symlink': '',
    'separator': '', 
    'extension': '',
    'redirect': '',
    'extract': '',
    'link': '',
    'unlink': '',
    'move': '',
    'remove': ''
})

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

def carve_url(string: str, /) -> str:
    """ Carve out the platform and architecture specific url
        from the request response.
    """
    if not isinstance(string, str):
        raise SystemExit(f"[<function carve_url>] expected 'string: str' got 'string: {type(string).__name__}'")
    
    current_platform = platform.system().lower()
    current_processor = platform.machine().lower()
    
    match (current_platform, current_processor):
        # Windows
        case ('windows', 'x86'):
            if ('windows' in string and string.endswith('.zip')) and ('x86-' in string or 'i386-' in string):
                return string
        case ('windows', 'amd64'):
            if ('windows' in string and string.endswith('.zip')) and ('win64-' in string or 'x86_64-' in string):
                return string
        case ('windows', 'aarch64'):
            if ('windows' in string and string.endswith('.zip')) and 'aarch64-' in string: 
                return string
        # Mac OS
        case ('darwin', 'x86_64'):
            if ('macos' in string and string.endswith('.tar.xz')) and 'x86_64-' in string:
                return string
        case ('darwin', 'aarch64'):
            if ('macos' in string and string.endswith('.tar.xz')) and 'aarch64' in string:
                return string
        # Linux
        case ('linux', 'x86'):
            if ('linux' in string and string.endswith('.tar.xz')) and ('x86-' in string or 'i386' in string):
                return string
        case ('linux', 'x86_64'):
            if ('linux' in string and string.endswith('.tar.xz')) and 'x86_64-' in string:
                return string
        case ('linux', 'aarch64'):
            if ('linux' in string and string.endswith('.tar.xz')) and 'aarch64-' in string:
                return string
        case ('linux', 'armv6kz'):
            if ('linux' in string and string.endswith('.tar.xz')) and 'armv6kz-' in string:
                return string
        case ('linux', 'armv7a'):
            if ('linux' in string and string.endswith('.tar.xz')) and 'armv7a-' in string:
                return string
        case ('linux', 'riscv64'):
            if ('linux' in string and string.endswith('.tar.xz')) and 'riscv64-' in string:
                return string
        case ('linux', 'powerpc64le'):
            if ('linux' in string and string.endswith('.tar.xz')) and 'powerpc64le-' in string:
                return string
        case ('linux', 'powerpc'):
            if ('linux' in string and string.endswith('.tar.xz')) and 'powerpc-' in string:
                return string
        # FreeBSD
        case ('freebsd', 'x86_64'):
            if ('linux' in string and string.endswith('.tar.xz')) and 'x86_64-' in string:
                return string
        case _:
            return ''

def fetch_versions(current_platform: str, current_processor: str, /) -> bool:
    """ Fetch all supporting versions for the current platform
        and architecture.
    """
    response = requests.get('https://ziglang.org/download')
    if response.status_code != 200:
        raise SystemExit(f"{response.status_code} [<function fetch_versions>] request failed!")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        response.close()

        strings = [string.get('href') for string in soup.find_all('a')]
        links = list(filter(None, map(carve_url, [string for string in strings])))
        if len(links) > 0:
            for link in links:
                constants['versions'].append(link)
            return True
        else:
            return False

def set_constants() -> bool:
    """ Set the values for each key in the constants dict.
        Values are based on the current platform and architecture.
    """
    current_platform = platform.system().lower()
    current_processor = platform.machine().lower()
    status = fetch_versions(current_platform, current_processor)

    if status:
        match current_platform:
            case 'windows':
                constants.update({
                    'ziggy': f'{expanduser("~")}\\\\.ziggy',
                    'symlink': f'{expanduser("~")}\\\\zig',
                    'separator': '\\\\',
                    'extension': '.zip',
                    'redirect': '2 > null',
                    'extract': 'unzip',
                    'link': 'mklink',
                    'unlink': 'del',
                    'move': 'move',
                    'remove': 'rmdir'
                })
                return True
            case ('darwin' | 'freebsd' | 'linux'):
                constants.update({
                    'ziggy': f'{expanduser("~")}/.ziggy',
                    'symlink': '/usr/bin/zig',
                    'separator': '/',
                    'extension': '.tar.xz',
                    'redirect': '2 > /dev/null',
                    'extract': 'tar xJf',
                    'link': 'sudo ln -s',
                    'unlink': 'sudo unlink',
                    'move': 'mv',
                    'remove': 'rm -r --interactive=never'
                })
                return True
            case _:
                raise systemExit(f"Unsupported Platform: '{current_platform}'")
        return True
    else:
        return False

def match_version(version: str, /) -> bool:
    """ Match the given version and return the
        url from the versions list.
    """
    if not isinstance(version, str):
        raise SystemExit(f"[<function match_version>] expected 'version: str' got 'version: {type(version).__name__}'")
    else:
        zig_versions = {
            '0.1.0', '0.2.0', '0.3.0', '0.4.0', '0.5.0', '0.6.0', '0.7.0', '0.7.1', '0.8.0',
            '0.8.1', '0.9.0', '0.9.1', '0.10.0', '0.10.1', '0.11.0', '0.12.0'
        }
        if version not in zig_versions:
            output(f"'{version}' isn't a valid Zig compiler version number.\n", mode='warn', exitcode=2)
            raise SystemExit(2)
        else:
            for ver in constants['versions']:
                if version in ver:
                    constants.update({'version': ver})
                    return True
    return False

def extract_name(url: str, /) -> bool:
    """ Extract the name from the url to use as
        the directory name.
    """
    if not isinstance(url, str):
        raise SystemExit(f"[<function extract_name>] expected 'url: str' got 'url: {type(url).__name__}'")
    else:
        name = url.split('/')[-1]
        name = name.replace('.zip', '') if name.endswith('.zip') else name.replace('.tar.xz', '')
        constants.update({'dirname': name})
        if constants['dirname'] != '':
            return True
        else:
            return False