""" Utility functions for simplifying 'ziggy' operations. """

from io import UnsupportedOperation
import os
import sys
import platform
import shutil
import json
from pathlib import Path

try:
    import requests
except ModuleNotFoundError:
    raise SystemExit(f"[{__file__}] failed to import 'requests'")

class ZiggyUtils:
    """ Contain methods for handling fetch requests and shell operations. """
    __slots__ = {'ziggy_path', 'branch_upstream', 'platform_info', 'branch_local', 'branch_default'}

    def __init__(self, /):
        self.ziggy_path = Path(os.path.join(Path.home(), '.ziggy'))
        self.branch_upstream = dict({'branch_version': '', 'archive_url': '', 'dirname': Path('')})
        self.platform_info = dict({'archive_extension': '', 'archive_format': '', 'archive_name': Path(''), 'symlink_path': Path('')})
        self.branch_local = Path('')
        self.branch_default = Path('')

        if not self.ziggy_path.exists():
            self.ziggy_path.mkdir()
        os.chdir(self.ziggy_path)

    def output(self, message, /, mode = 'normal', exitcode = 0):
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
        
        red, green, yellow, blue, reset = "\x1b[1;31m", "\x1b[1;32m", "\x1b[1;33m", "\x1b[34m", "\x1b[0m"
        
        match (mode, exitcode):
            case ('normal', 0):
                sys.stdout.write(f"{green}>>{reset} {blue}{message}{reset}\n")

            case ('warn', 1):
                sys.stdout.write(f"{yellow}>>{reset} {blue}{message}{reset}\n")
            
            case ('error', 2):
                sys.stderr.write(f"{red}>>{reset} {blue}{message}{reset}\n")
            
            case _:
                errors = f"\n  - 'mode=normal, exitcode=0'\n  - 'mode=warn, exitcode=1'\n  - 'mode=error, errorcode=2'\n"
                raise SystemExit(f"[<function output>]\n expected one of: {errors}\n got => 'mode={mode}, exitcode={exitcode}'")

        return exitcode

    def prefetch_master(self, /):
        """ Prefetch the Zig compiler from the master/dev branch. """
        schema = requests.get("https://ziglang.org/download/index.json")

        if schema.status_code == 200:
            contents = json.loads(schema.content)
            master = list(contents.keys())[0]
            system, machine = platform.system().lower(), platform.machine().lower()

            match machine:
                case "i386":
                    machine = "x86"

                case "amd64":
                    machine = "x86_64"

            try:
                self.branch_upstream['branch_version'] = contents[master]['version']
                self.branch_upstream['archive_url'] = contents[master][f'{machine}-{system}']['tarball']
                self.branch_upstream['dirname'] = Path(f'zig-{machine}-{system}-{contents[master]["version"]}')
            except KeyError:
                raise SystemExit(self.output(f"{machine}-{system} is currently not supported", mode='warn', exitcode=1))

            match system:
                case 'windows':
                    self.platform_info['archive_format'] = 'zip'
                    self.platform_info['archive_name'] = Path(f'zig-{machine}-{system}-{contents[master]["version"]}.zip')
                    self.platform_info['symlink_path'] = Path(os.path.join('c:', 'Windows32', 'zig.exe'))
                case _:
                    self.platform_info['archive_format'] = 'xztar'
                    self.platform_info['archive_name'] = Path(f'zig-{machine}-{system}-{contents[master]["version"]}.tar.xz')
                    self.platform_info['symlink_path'] = Path(os.path.join(Path.home().resolve(), '.local', 'bin', 'zig'))

            for installed in self.ziggy_path.iterdir():
                if 'dev' in installed.name:
                    self.branch_local = Path(os.path.basename(installed))
                else:
                    continue

            if self.platform_info['symlink_path'].is_symlink():
                self.branch_default = Path(self.platform_info['symlink_path'].resolve().parent.name)
        else:
            raise SystemExit(self.output("Connection to 'https://ziglang.org' failed", mode='error', exitcode=2))

    def prefetch_stable(self, /):
        """ Prefetch the Zig compiler from the stable branch. """
        schema = requests.get("https://ziglang.org/download/index.json")

        if schema.status_code == 200:
            contents = json.loads(schema.content)
            stable = list(contents.keys())[1]
            system, machine = platform.system().lower(), platform.machine().lower()

            match machine:
                case "i386":
                    machine = "x86"

                case "amd64":
                    machine = "x86_64"

            try:
                self.branch_upstream['branch_version'] = stable
                self.branch_upstream['archive_url'] = contents[stable][f'{machine}-{system}']['tarball']
                self.branch_upstream['dirname'] = Path(f'zig-{machine}-{system}-{stable}')
            except KeyError:
                raise SystemExit(self.output(f"{machine}-{system} is currently not supported", mode='warn', exitcode=1))

            match system:
                case 'windows':
                    self.platform_info['archive_format'] = 'zip'
                    self.platform_info['archive_name'] = Path(f'zig-{machine}-{system}-{stable}.zip')
                    self.platform_info['symlink_path'] = Path(os.path.join('c:', 'Windows32', 'zig.exe'))
                case _:
                    self.platform_info['archive_format'] = 'xztar'
                    self.platform_info['archive_name'] = Path(f'zig-{machine}-{system}-{stable}.tar.xz')
                    self.platform_info['symlink_path'] = Path(os.path.join(Path.home().resolve(), '.local', 'bin', 'zig'))

            for installed in self.ziggy_path.iterdir():
                if 'dev' not in installed.name and installed.name not in ('.', '..'):
                    self.branch_local = Path(os.path.basename(installed))
                else:
                    continue

            if self.platform_info['symlink_path'].is_symlink():
                self.branch_default = Path(self.platform_info['symlink_path'].readlink().parent.name)
        else:
            raise SystemExit(self.output("Connection to 'https://ziglang.org' failed", mode='error', exitcode=2))

    def branch_check(self, branch, /):
        """ Check if the given branch name is valid. """
        if not isinstance(branch, str):
            raise SystemExit(f"[<function branch_check>] expected 'branch: str' got 'branch: {type(branch).__name__}'")
        else:
            if branch not in ('master', 'stable'):
                raise SystemExit(self.output(f"{branch} is an invalid branch name", mode='error', exitcode=2))
            else:
                return None

    def operation(self, option, name = '', /):
        """ Perform a shell operation based on a given option. """
        if not isinstance(option, str):
            raise SystemExit(f"[<function operation>] expected 'option: str' got 'option: {type(option).__name__}'")

        if not isinstance(name, str):
            raise SystemExit(f"[<function operation>] expected 'option: str' got 'option: {type(option).__name__}'")

        os.chdir(self.ziggy_path)

        match option:
            case 'extract':
                try:
                    shutil.unpack_archive(name, extract_dir='.', format=self.platform_info['archive_format'])
                except FileNotFoundError:
                    raise SystemExit(self.output(f'Extract Failed {self.platform_info["archive_name"]} not found', mode='error', exitcode=2))

            case 'remove':
                target = ''
                try:
                    if not name and self.branch_local.name:
                        self.platform_info['symlink_path'].unlink(missing_ok=True)
                        target = self.branch_local.name
                        shutil.rmtree(target)

                    if name and self.platform_info['archive_name'].exists():
                        target = self.platform_info['archive_name']
                        os.remove(target)
                except FileNotFoundError:
                    raise SystemExit(self.output(f'{target} not found', mode='error', exitcode=2))
                except OSError:
                    raise SystemExit(self.output(f'Failed to remove {target}', mode='error', exitcode=2))

            case 'link':
                self.platform_info['symlink_path'].unlink(missing_ok=True)
                self.platform_info['symlink_path'].symlink_to(name)

            case 'unlink':
                self.platform_info['symlink_path'].unlink(missing_ok=True)

            case _:
                raise SystemExit(f"[<function shell_operation>] invalid option {option!r}")
