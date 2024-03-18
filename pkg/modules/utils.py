""" Utility functions for simplifying 'ziggy' operations. """

import os
import sys
import platform
import shutil
import subprocess
from os.path import sep
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
    'supported': list(),
    'zig_url': '',
    'archive': '',
    'format': '',
    'dirname': '',
    'ziggy': '',
    'symlink': '',
    'link': '',
    'unlink': '',
    'extension': '',
    'redirect': '',
    'extract': '',
    'mkdir': '',
    'move': '',
    'remove': '',
    'rmdirs': ''
})

def output(message: str, /, mode: str = 'normal', exitcode: int = 0) -> int:
    """ Output a specified message based on a given mode.
        Return an exit code if specified otherwise return 0.
        The exit code must be a value in the range 0-2 (inclusive).
        
        Modes:
            normal - prints to standard output (green >> prefix and cyan text)
            warn   - prints to standard output (yellow >> prefix an cyan text)
            error  - prints to standard error  (red >> prefix and cyan text)
    """
    if not isinstance(message, str):
        raise SystemExit(f"[<function output>] expected 'message: str' got 'message: {type(message).__name__}'")
    
    if not isinstance(mode, str):
        raise SystemExit(f"[<function output>] expected 'mode: str' got 'mode: {type(mode).__name__}'")
    
    if not isinstance(exitcode, int):
        raise SystemExit(f"[<function output>] expected 'exitcode: int' got 'exitcode: {type(exitcode).__name__}'")
    
    if not (0 <= exitcode <= 2):
        raise SystemExit(f"[<function output>] expected 'exitcode=(0 <= n <= 2)' got 'exitcode={exitcode}'")
    
    red = "\x1b[1;38;2;255;50;50m"
    green = "\x1b[1;38;2;50;255;50m"
    yellow = "\x1b[1;38;2;255;255;50m"
    cyan = "\x1b[38;2;50;255;255m"
    reset = "\x1b[0m"
    
    match (mode, exitcode):
        case ('normal', 0):
            sys.stdout.write(f"{green}>>{reset} {cyan}{message}{reset}\n")
        case ('warn', 1):
            sys.stdout.write(f"{yellow}>>{reset} {cyan}{message}{reset}\n")
        case ('error', 2):
            sys.stderr.write(f"{red}>>{reset} {cyan}{message}{reset}\n")
        case _:
            errors = f"\n  'mode=normal, exitcode=0'\n  'mode=warn, exitcode=1'\n  'mode=error, errorcode=2'"
            raise SystemExit(f"[<function output>]\n expected one of:{errors}\n\n got 'mode={mode}, exitcode={exitcode}'")
    return exitcode

def carve_supported_urls(string: str, /) -> str:
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

def fetch_supported_versions(current_platform: str, current_processor: str, /) -> bool:
    """ Fetch all supporting versions for the current platform
        and architecture.
    """
    response = requests.get('https://ziglang.org/download')
    if response.status_code != 200:
        raise SystemExit(f"{response.status_code} [<function fetch_supported_versions>] request failed!")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        response.close()

        strings = [string.get('href') for string in soup.find_all('a')]
        links = list(filter(None, map(carve_supported_urls, [string for string in strings])))
        if len(links) > 0:
            for link in links:
                constants['supported'].append(link)
            return True
        else:
            return False

def set_constants() -> None:
    """ Set the values for each key in the constants dict.
        Values are based on the current platform and architecture.
    """
    current_platform = platform.system().lower()
    current_processor = platform.machine().lower()
    status = fetch_supported_versions(current_platform, current_processor)

    if status:
        match current_platform:
            case 'windows':
                constants.update({
                    'format': 'zip',
                    'ziggy': f'{Path.home()}{sep}.ziggy',
                    'symlink': f'{Path.home()}{sep}zig',
                    'link': 'mklink',
                    'unlink': 'del',
                    'extension': '.zip',
                    'redirect': '2>null',
                    'extract': 'unzip',
                    'mkdir': 'mkdir',
                    'move': 'move',
                    'remove': 'rmdir /q',
                    'rmdirs': 'rmdir /s /q'
                })
            case ('darwin' | 'freebsd' | 'linux'):
                constants.update({
                    'format': 'xztar',
                    'ziggy': f'{Path.home()}{sep}.ziggy',
                    'symlink': f'{sep}usr{sep}bin{sep}zig',
                    'link': 'sudo ln -s',
                    'unlink': 'sudo unlink',
                    'extension': '.tar.xz',
                    'redirect': f'2>{sep}dev{sep}null',
                    'extract': 'tar xJf',
                    'mkdir': 'mkdir',
                    'move': 'mv',
                    'remove': 'rm',
                    'rmdirs': 'rm -r --interactive=never'
                })
            case _:
                exitcode = output(f'Unsupported platform: {current_platform!r}', mode='warn', exitcode=1)
                raise SystemExit(exitcode)
    else:
        exitcode = output('Failed to fetch supported compiler versions. Check your internet connection.', mode='warn', exitcode=1)
        raise SystemExit(exitcode)

# ---------------------------------------------------------

def match_version(version: str, /) -> None:
    """ Match the given version and sets the
        zig_url constant.
    """
    if not isinstance(version, str):
        raise SystemExit(f"[<function match_version>] expected 'version: str' got 'version: {type(version).__name__}'")
    else:
        zig_versions = {
            '0.1.0', '0.2.0', '0.3.0', '0.4.0', '0.5.0', '0.6.0', '0.7.0', '0.7.1', '0.8.0',
            '0.8.1', '0.9.0', '0.9.1', '0.10.0', '0.10.1', '0.11.0', '0.12.0'
        }
        if version not in zig_versions:
            exitcode = output(f"'{version}' isn't a valid Zig compiler version number.\n", mode='warn', exitcode=1)
            raise SystemExit(exitcode)
        else:
            for url in constants['supported']:
                if version in url:
                    constants.update({'zig_url': url})
                    break
            if constants['zig_url'] == '':
                exitcode = output(f'{version!r} does not support your platform', mode='error', exitcode=2)
                raise SystemExit(exitcode)
    return None

def carve_archive_name() -> None:
    """ Carve out the archive name from the url. """
    name = constants['zig_url'].split('/')[-1]
    constants.update({'archive': name})
    if constants['archive'] == '':
        raise SystemExit(f"[<function carve_archive_name>] failed to carve out the archive name.")

def carve_compiler_name() -> None:
    """ Extract the name from the url to use as
        the directory name.
    """
    name = constants['zig_url'].split('/')[-1]
    name = name.replace(constants['extension'], '')
    constants.update({'dirname': name})
    if constants['dirname'] == '':
        raise SystemExit(f"[<function carve_compiler_name>] failed to carve out the compiler name.")


def have_compiler(version: str, /) -> str:
    """ Check if a Zig compiler of a specified
        version exists and return the compiler
        name, otherwise return False.
    """
    if not isinstance(version, str):
        raise SystemExit(f"[<function have_compiler>] expected 'version: str' got 'version: {type(version).__name__}'")
    else:
        for installed in Path(constants['ziggy']).iterdir():
            if version in installed.name:
                return installed.name
        return ''

def get_symlink_name() -> str:
    """ Get the name of the symlink. """
    if Path(constants['symlink']).is_symlink():
        return Path(constants['symlink']).readlink().parent.name
    else:
        return ''

# constants must be set before this function is invoked
# match_version() must be invoked before this function
# carve_archive_name() must be invoked before this function
# carve_compiler_name() must be invoked before this function
def shell_operation(*, option: str = 'move', name: str = constants['dirname']) -> None:
    """ Perform a shell operation based on a given option. """
    if not isinstance(option, str):
        raise SystemExit(f"[<function shell_operation>] expected 'option: str' got 'option: {type(option).__name__}'")
    
    if not isinstance(name, str):
        raise SystemExit(f"[<function shell_operation>] expected 'name: str' got 'name: {type(dirname).__name__}'")

    ziggy = constants['ziggy']
    symlink = constants['symlink']
    link = constants['link']
    unlink = constants['unlink']
    extension = constants['extension']
    redirect = constants['redirect']
    extract = constants['extract']
    mkdir = constants['mkdir']
    move = constants['move']
    remove = constants['remove']
    rmdirs = constants['rmdirs']

    match option:
        case 'move':
            cwd = Path.cwd()
            if Path(f'{cwd}{sep}{name}').exists():
                shutil.move(f'{cwd}{sep}{name}', f'{ziggy}')
                if not Path(f'{ziggy}{sep}{name}').exists():
                    exitcode = output('Failed to move archive', mode='error', exitcode=2)
                    raise SystemExit(exitcode)
            else:
                exitcode = output(f'{name!r} file not found', mode='error', exitcode=2)
                raise SystemExit(exitcode)
        case 'extract':
            if Path(f'{ziggy}{sep}{name}').exists():
                shutil.unpack_archive(f'{ziggy}{sep}{name}', extract_dir=ziggy, format=constants['format'])
                if not Path(f'{ziggy}{sep}{name.replace(extension, "")}').exists():
                    exitcode = output(f'Failed to extract archive contents', mode='error', exitcode=2)
                    raise SystemExit(exitcode)
            else:
                exitcode = output(f'{name!r} file not found', mode='error', exitcode=2)
                raise SystemExit(exitcode)
        case 'remove':
            returncode = 1
            if Path(f'{ziggy}{sep}{name}').exists():
                if Path(f'{ziggy}{sep}{name}').is_dir():
                    returncode = subprocess.run(f'{rmdirs} {ziggy}{sep}{name} {redirect}', shell=True).returncode
                else:
                    returncode = subprocess.run(f'{remove} {ziggy}{sep}{name} {redirect}', shell=True).returncode
                
                if returncode != 0:
                    exitcode = output(f'Failed to remove {name!r}', mode='error', exitcode=2)
                    raise SystemExit(exitcode)
            else:
                exitcode = output('Nothing to delete', mode='warn', exitcode=1)
                raise SystemExit(exitcode)
        case 'link':
            if Path(symlink).is_symlink():
                subprocess.run(f'{unlink} {symlink} {redirect}', shell=True)

            returncode = subprocess.run(f'{link} {ziggy}{sep}{name}{sep}zig {symlink} {redirect}', shell=True).returncode
            if returncode != 0:
                exitcode = output('Failed to create symlink', mode='error', exitcode=2)
                raise SystemExit(exitcode)
        case 'unlink':
            if Path(symlink).is_symlink():
                subprocess.run(f'{unlink} {symlink} {redirect}', shell=True)
        case _:
            raise SystemExit(f"[<function shell_operation>] invalid option {option!r}")