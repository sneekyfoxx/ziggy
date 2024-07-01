""" Utility functions for simplifying 'ziggy' operations. """

import os
import sys
import platform
import shutil
import json
import subprocess
from os.path import sep
from pathlib import Path

try:
    import requests
except ModuleNotFoundError:
    raise SystemExit(f"[{__file__}] failed to import 'requests'")

constants = dict({
    'master': '',
    'stable': '0.13.0',
    'json': '',
    'zig_url': '',
    'version': '',
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
    """ Output a specific message based on a given mode.
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

def get_json() -> None:
    """ Get the JSON representation of compiler downloads. """
    schema = requests.get("https://ziglang.org/download/index.json")

    if schema.status_code == 200:
        contents = json.loads(schema.content)
        constants["json"] = contents
        constants["master"] = contents["master"]["version"].split("-")[0]
        constants["archive"] = contents["master"]["version"]
    else:
        raise SystemExit("Failed to retrieve JSON from 'https://ziglang.org'")

    return None

def get_url(option: str, /) -> None:
    """ Carve out the platform and architecture specific url
        from the request response.
    """
    if not isinstance(option, str):
        raise SystemExit(f"[<function carve_url>] expected 'option: str' got 'option: {type(option).__name__}'")
    
    current_processor = platform.machine().lower()
    current_platform = platform.system().lower()

    if current_processor == "AMD64":
        current_processor = "x86_64"
    
    if current_processor == "i386":
        current_processor = "x86"

    try:
        get_json()
        stable = constants["stable"]
        key = f"{current_processor}-{current_platform}"

        if option == "stable":
            constants["zig_url"] = constants["json"][stable][key]["tarball"]
            constants["version"] = constants[stable]
        elif option == "master":
            constants["zig_url"] = constants["json"]["master"][key]["tarball"]
            constants["version"] = constants["master"]
        else:
            raise SystemExit("Invalid option")
    except KeyError:
        raise SystemExit(f"{current_processor}-{current_platform} not supported.")
    finally:
        return None

def set_constants() -> None:
    """ Set the values for each key in the constants dict.
        Values are based on the current platform and architecture.
    """
    current_platform = platform.system().lower()
    current_processor = platform.machine().lower()

    match current_platform:
        case 'windows':
            constants.update({
                'format': 'zip',
                'ziggy': f'{Path.home()}{sep}.ziggy',
                'symlink': f'c:{sep}Windows{sep}System32{sep}zig.exe',
                'link': 'mklink',
                'unlink': 'del',
                'extension': '.zip',
                'redirect': '2>NUL',
                'extract': 'unzip',
                'mkdir': 'mkdir',
                'move': 'move',
                'remove': 'del',
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

# ---------------------------------------------------------

def have_compiler(version: str, /) -> str:
    """ Check if a Zig compiler of a specified
        version exists and return the compiler
        name, otherwise return False.
    """
    if not isinstance(version, str):
        raise SystemExit(f"[<function have_compiler>] expected 'version: str' got 'version: {type(version).__name__}'")
    else:
        for installed in Path(constants['ziggy']).iterdir():
            if constants[version] in installed.name:
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
            returncode = 1
            if Path(symlink).is_symlink():
                subprocess.run(f'{unlink} {symlink} {redirect}', shell=True)
            
            if platform.system().lower() == 'windows':
                returncode = subprocess.run(f'{link} {symlink} {ziggy}{sep}{name}{sep}zig.exe {redirect}', shell=True).returncode
            else:
                returncode = subprocess.run(f'{link} {ziggy}{sep}{name}{sep}zig {symlink} {redirect}', shell=True).returncode
            
            if returncode != 0:
                exitcode = output('Failed to create symlink', mode='error', exitcode=2)
                raise SystemExit(exitcode)
        case 'unlink':
            if Path(symlink).is_symlink():
                subprocess.run(f'{unlink} {symlink} {redirect}', shell=True)
        case _:
            raise SystemExit(f"[<function shell_operation>] invalid option {option!r}")
