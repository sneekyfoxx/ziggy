""" This file contains a class with methods for handling
    common ziggy operations.
"""

from . import (
        RED,
        GREEN,
        BLUE,
        PURPLE,
        WHITE,
        RESET,
        EXISTS,
        EXPANDUSER,
        STDOUT,
        STDERR,
        PATH,
        SCANDIR,
        SYSTEM,
        MACHINE,
        RUN,
        FIND,
        REQUEST,
        REQ_ERROR,
        SCRAPER
        )

class ZiggyMethods:
    """ Contains methods for common ziggy operations.
    """
    __slots__ = ()
    PLATFORM = SYSTEM().lower()
    PROCESSOR = MACHINE()
    BASE_URL = "https://ziglang.org/download"
    HOME = EXPANDUSER('~')
    ZIGGY_DIR = ''
    ZIG_LINK = ''
    VERSIONS = [
            '0.1.0', '0.2.0', '0.3.0', '0.4.0', '0.5.0', '0.6.0', '0.7.0', '0.7.1',
            '0.8.0', '0.8.1', '0.9.0', '0.9.1', '0.10.0', '0.10.1', '0.11.0', '0.12.0'
            ]
    VMAP = dict({
        'windows-x86': list(),
        'windows-x86_64': list(),
        'windows-aarch64': list(),
        'darwin-x86_64': list(),
        'darwin-aarch64': list(),
        'linux-x86': list(),
        'linux-x86_64': list(),
        'linux-aarch64': list(),
        'linux-armv6kz': list(),
        'linux-armv7a': list(),
        'linux-riscv64': list(),
        'linux-powerpc64le': list(),
        'linux-powerpc': list(),
        'freebsd-x86_64': list()
        })
    VMAP_KEY = f'{PLATFORM}-{PROCESSOR}'

    def __new__(cls, /) -> object:
        """ Return a new 'signleton' object.
        """
        cls.instance = None
        if cls.PLATFORM == 'windows':
            cls.ZIGGY_DIR = f'{cls.HOME}\\.ziggy'
            cls.ZIG_LINK = 'c:\\Windows\\system32\\zig'
            if not EXISTS(cls.ZIGGY_DIR):
                RUN(f'mkdir {cls.ZIGGY_DIR} 2> nul', shell=True)
        elif cls.PLATFORM in ['darwin', 'linux', 'freebsd']:
            cls.ZIGGY_DIR = f'{cls.HOME}/.ziggy'
            cls.ZIG_LINK = '/usr/bin/zig'
            if not EXISTS(cls.ZIGGY_DIR):
                RUN(f'mkdir {cls.ZIGGY_DIR} 2>/dev/null', shell=True)

        if cls.instance is None:
            cls.instance = super(ZiggyMethods, cls).__new__(cls)
        return cls.instance

    @classmethod
    def ziggy_ensure_ziggy(cls, /) -> None:
        """ Ensure that the '.ziggy' directory is present.
        """
        if cls.PLATFORM == 'windows' and not EXISTS(f'{cls.HOME}\\.ziggy'):
            RUN(f'mkdir {cls.HOME}\\.ziggy 2> nul', shell=True)
        if cls.PLATFORM in ['darwin', 'linux', 'freebsd'] and not EXISTS(f'{cls.HOME}/.ziggy'):
            RUN(f'mkdir {cls.HOME}/.ziggy 2>/dev/null', shell=True)
        return None

    @classmethod
    def ziggy_emitter(cls, message: str, /) -> int:
        """ Emit the given message to standard error.
        """
        STDERR(message)
        return 1

    @classmethod
    def ziggy_collect(cls, /) -> int:
        """ Send a 'GET' request to 'ziglang.org' and
            collect the URL's for each compiler version.
        """
        try:
            request = REQUEST('GET', cls.BASE_URL)
        except REQ_ERROR:
            STDOUT(f"{RED}Failed To Connect To Server.{RESET}\n")
            return 1
        else:
            if request.status_code == 200:
                scraped = SCRAPER(request.content, 'html.parser')
                request.close()

                for string in scraped.findAll('a'):
                    target = string.decode().replace('<a href=', '')
                    target = target.replace('"', '')
                    target = target.split('>')[0]

                    if target.endswith('.zip'):
                        if 'win64' in target or 'windows-x86_64' in target:
                            cls.VMAP['windows-x86_64'].append(target)
                        elif 'windows-i386' in target or 'windows-x86' in target:
                            cls.VMAP['windows-x86'].append(target)
                        elif 'windows-aarch64' in target:
                            cls.VMAP['windows-aarch64'].append(target)
                        else:
                            continue
                    elif target.endswith('.xz'):
                        if 'macos-x86_64-' in target:
                            cls.VMAP['darwin-x86_64'].append(target)
                        elif 'macos-aarch64-' in target:
                            cls.VMAP['darwin-aarch64'].append(target)
                        elif 'linux-i386-' in target or 'linux-x86-' in target:
                            cls.VMAP['linux-x86'].append(target)
                        elif 'linux-x86_64-' in target:
                            cls.VMAP['linux-x86_64'].append(target)
                        elif 'linux-aarch64-' in target:
                            cls.VMAP['linux-aarch64'].append(target)
                        elif 'linux-armv6kz-' in target:
                            cls.VMAP['linux-armv6kz'].append(target)
                        elif 'linux-armv7a-' in target:
                            cls.VMAP['linux-armv7a'].append(target)
                        elif 'linux-riscv64-' in target:
                            cls.VMAP['linux-riscv64'].append(target)
                        elif 'linux-powerpc64le-' in target:
                            cls.VMAP['linux-powerpc64le'].append(target)
                        elif 'linux-powerpc-' in target:
                            cls.VMAP['linux-powerpc'].append(target)
                        elif 'freebsd-x86_64-' in target:
                            cls.VMAP['freebsd-x86_64'].append(target)
                        else:
                            continue
                    else:
                        continue
                return 0
            else:
                STDOUT(f"{WHITE}[{request.status_code}]{RESET} {RED}Request Failed.{RESET}\n")
                return 1

    @classmethod
    def ziggy_get_target(cls, version: str, /) -> str:
        """ Get the target archive url containing the
            given version.
        """
        archives = cls.VMAP[cls.VMAP_KEY]

        for available in archives:
            if cls.PLATFORM == 'windows' and cls.PROCESSOR == 'x86_64':
                if version in ['0.1.0', '0.2.0'] and 'win64' in available:
                    return available
                elif version in available:
                    return available
            elif cls.PLATFORM == 'windows' and cls.PROCESSOR == 'x86':
                if version in ['0.6.0', '0.7.0', '0.7.1', '0.8.0', '0.8.1', '0.9.0', '0.9.1'] and 'i386' in available:
                    return available
            elif cls.PLATFORM == 'windows' and version in available:
                return available
            elif cls.PLATFORM == 'linux' and cls.PROCESSOR == 'x86':
                if version not in ['0.11.0', '0.12.0'] and 'i386' in available:
                    return available
            elif cls.PLATFORM == 'linux' and version in available:
                return available
            elif version in available:
                return available
            else:
                continue
        return ""

    @classmethod
    def ziggy_install_zig_windows(cls, version: str, /) -> int:
        """ Handle Zig compiler installation for Windows.
        """
        target_url = cls.ziggy_get_target(version)
        if target_url == '':
            STDERR(f"'{WHITE}{version}{RESET}' {RED}is not a known or valid version for your platform.{RESET}\n")
            return 1
        else:
            zig_archive = target_url.split('/')[-1]
            zig_dir = zig_archive.replace('.zip', '')
            request = REQUEST('GET', target_url)

            if request.status_code == 200:
                with open(zig_archive, 'wb') as archive:
                    archive.write(request.content)
                    request.close()
                RUN(f'mv .\\{zig_archive} {cls.ZIGGY_DIR}\\{zig_archive}', shell=True)
                RUN(f'cd {cls.ZIGGY_DIR} && tar xJf {zig_archive} && rm {zig_archive}', shell=True)
                STDOUT(f'{GREEN}Install Complete!{RESET}\n')
                return 0
            else:
                STDERR(f'{RED}Install Failed!{RESET}\n')
                return 1

    @classmethod
    def ziggy_install_zig_unix(cls, version: str, /) -> int:
        """ Handle Zig compiler installation for Unix
            based platforms.
        """
        target_url = cls.ziggy_get_target(version)
        if target_url == '':
            STDERR(f"'{WHITE}{version}{RESET}' {RED}is not a known or valid version for your platform.{RESET}\n")
            return 1
        else:
            zig_archive = target_url.split('/')[-1]
            zig_dir = zig_archive.replace('.tar.xz', '')
            request = REQUEST('GET', target_url)

            if request.status_code == 200:
                with open(zig_archive, 'wb') as archive:
                    archive.write(request.content)
                    request.close()
                RUN(f'mv ./{zig_archive} {cls.ZIGGY_DIR}/{zig_archive} 2>/dev/null', shell=True)
                RUN(f'cd {cls.ZIGGY_DIR} && tar xJf {zig_archive} && rm {zig_archive} 2>/dev/null', shell=True)
                STDOUT(f'{GREEN}Install Complete!{RESET}\n')
                return 0
            else:
                STDERR(f'{WHITE}[{request.status_code}]{RESET} {RED}Install Failed!{RESET}\n')
                return 1

    @classmethod
    def ziggy_help(cls, /) -> int:
        """ Show all available options for
            'ziggy'.
        """
        STDOUT(f"\n{GREEN}OPTIONS            DESCRIPTION{RESET}")
        STDOUT(f"\n{WHITE}-------            -----------{RESET}")
        STDOUT(f"\n {PURPLE}help{RESET}               {WHITE}show all ziggy options{RESET}\n")
        STDOUT(f"\n {PURPLE}list{RESET}               {WHITE}list all installed or supported compilers{RESET}")
        STDOUT(f"\n   {BLUE}installed          all installed versions{RESET}")
        STDOUT(f"\n   {BLUE}available          all available versions for the current platform{RESET}\n")
        STDOUT(f"\n {PURPLE}primary{RESET}            {WHITE}show or set the primary comipler version{RESET}")
        STDOUT(f"\n   {BLUE}VERSION            major.minor.patch (optional){RESET}\n")
        STDOUT(f"\n {PURPLE}install{RESET}            {WHITE}install a specific compiler version{RESET}")
        STDOUT(f"\n   {BLUE}VERSION            major.minor.patch (default 'master'){RESET}\n")
        STDOUT(f"\n {PURPLE}upgrade{RESET}            {WHITE}upgrade the primary compiler to 'master'{RESET}\n")
        STDOUT(f"\n {PURPLE}destroy{RESET}            {WHITE}destroy the primary or a specific compiler version{RESET}")
        STDOUT(f"\n   {BLUE}VERSION            major.minor.patch (default 'primary'){RESET}\n")
        return 0

    @classmethod
    def ziggy_list(cls, option: str = 'installed', /) -> int:
        """ List all of the installed Zig compilers
            on the system or the Zig compiler versions
            supported for the current platform and architecture.
        """
        if cls.ziggy_collect() == 1:
            STDOUT(f"{RED}Request Failed.{RESET}\n")
            return 1
        else:
            if option == 'supported':
                versions = cls.VMAP[cls.VMAP_KEY]
                for version in versions:
                    version = version.split('/')[-1] if cls.PLATFORM != 'windows' else version.split('\\')[-1]
                    version = version.replace('.tar.xz', '') if cls.PLATFORM != 'windows' else version.replace('.zip', '')
                    STDOUT(f'{WHITE}->{RESET} {GREEN}{version}{RESET}\n')
                return 0
            elif option == 'installed':
                versions = [version.name for version in PATH(cls.ZIGGY_DIR).iterdir()]
                for version in versions:
                    version = version.split('/')[-1] if cls.PLATFORM != 'windows' else version.split('\\')[-1]
                    STDOUT(f'{WHITE}->{RESET} {GREEN}{version}{RESET}\n')
                return 0
            else:
                STDERR(f'{RED}Invalid option for{RESET} {GREEN}ziggy list{RESET} {RED}->{RESET} \'{WHITE}{option}{RESET}\'\n')
                return 1

    @classmethod
    def ziggy_primary(cls, version: str = "", /) -> int:
        """ Show the primary Zig compiler in use or
            set the primary Zig compiler.
        """
        if version != '' and version not in cls.VERSIONS:
            STDERR(f'\'{WHITE}{version}{RESET}\' {RED}isn\'t a valid Zig compiler version{RESET}\n')
            return 1
        else:
            zig_linked = False if not EXISTS(cls.ZIG_LINK) else True
            has_ziggy = False if not EXISTS(cls.ZIGGY_DIR) else True

            if version == '':
                if zig_linked:
                    compiler_name = PATH(cls.ZIG_LINK).resolve().parent.name
                    STDOUT(f'{GREEN}{compiler_name}{RESET}\n')
                    return 0
                else:
                    STDOUT(f'{RED}Primary Compiler Not Set{RESET}\n')
                    return 1
            else:
                linked = 1
                primary = ''
                if has_ziggy:
                    for entry in SCANDIR(cls.ZIGGY_DIR):
                        if entry.is_dir(follow_symlinks=False) and version in entry.name:
                            if cls.PLATFORM == 'windows':
                                make_link_win = f'mklink {cls.ZIGGY_DIR}\\{entry.name}\\zig {cls.ZIG_LINK} 2> nul'
                                if zig_linked:
                                    RUN(f'del {cls.ZIG_LINK} 2> nul', shell=True)
                                    linked = RUN(make_link_win, shell=True).returncode
                                    primary = entry.name
                                    break
                                else:
                                    linked = RUN(make_link_win, shell=True).returncode
                                    primary = entry.name
                                    break
                            else:
                                make_link_unix = f'sudo ln -s {cls.ZIGGY_DIR}/{entry.name}/zig {cls.ZIG_LINK} 2>/dev/null'
                                if zig_linked:
                                    RUN(f'sudo unlink {cls.ZIG_LINK} 2>/dev/null', shell=True)
                                    linked = RUN(make_link_unix, shell=True).returncode
                                    primary = entry.name
                                    break
                                else:
                                    linked = RUN(make_link_unix, shell=True).returncode
                                    primary = entry.name
                                    break
                        else:
                            continue

                    if linked == 0:
                        STDOUT(f'{GREEN}Primary ->{RESET} \'{WHITE}{primary}{RESET}\'')
                        return linked
                    else:
                        STDERR(f'{RED}Zig compiler version{RESET} \'{WHITE}{version}{RESET}\' {RED}isn\'t installed.{RESET}\n')
                        return 1
                else:
                    STDERR(f'{RED}Cannot set primary compiler. No directory named{RESET} \'{WHITE}{cls.ZIGGY_DIR}{RESET}\'\n')
                    return 1

    @classmethod
    def ziggy_install(cls, version: str = "0.12.0", /) -> int:
        """ Install the Zig compiler containing the specified version.
            Install the latest Zig compiler if no version is specified.
        """
        if version not in cls.VERSIONS:
            STDERR(f"'{WHITE}{version}{RESET}' {RED}is not a known or valid Zig compiler version.{RESET}\n")
            return 1
        else:
            cls.ziggy_ensure_ziggy()
            status = cls.ziggy_collect()
            if status == 1:
                return status
            else:
                if cls.PLATFORM == 'windows':
                    return cls.ziggy_install_zig_windows(version)
                else:
                    return cls.ziggy_install_zig_unix(version)


    @classmethod
    def ziggy_upgrade(cls, /) -> int:
        """ Upgrade the primary Zig compiler to the
            latest Zig compiler version if not installed.
        """
        latest = '0.12.0'
        installed = False
        for version in PATH(cls.ZIGGY_DIR).iterdir():
            if latest in version.name:
                installed = True
                STDOUT(f'{GREEN}The latest Zig compiler is already installed{RESET}\n')
                break
            else:
                continue
        if installed:
            return 0
        else:
            cls.ziggy_install(latest)
            return 0

    @classmethod
    def ziggy_destroy(cls, version: str = "", /) -> int:
        """ Destroy / remove a compiler of choice if the
            specified version is installed.
        """
        if version not in cls.VERSIONS:
            STDERR(f'\'{WHITE}{version}{RESET}\' {RED}isn\'t a valid Zig compiler version{RESET}\n')
            return 1
        else:
            for versions in PATH(cls.ZIGGY_DIR).iterdir():
                versions = versions.name.split('/')[-1] if cls.PLATFORM != 'windows' else versions.name.split('\\')[-1]
                if cls.PLATFORM == 'windows' and version in versions:
                    RUN(f'rmdir /s /q {cls.ZIGGY_DIR}\\{versions} 2> nul', shell=True)
                    RUN(f'del {cls.ZIG_LINK} 2> nul', shell=True)
                    STDOUT(f'{GREEN}Destroyed{RESET} \'{WHITE}{versions}{RESET}\'')
                    return 0
                elif version in versions:
                    RUN(f'rm -r --interactive=never {cls.ZIGGY_DIR}/{versions} 2>/dev/null', shell=True)
                    RUN(f'sudo unlink {cls.ZIG_LINK} 2>/dev/null', shell=True)
                    STDOUT(f'{GREEN}Destroyed{RESET} \'{WHITE}{versions}{RESET}\'')
                    return 0
                else:
                    continue
            STDERR(f'{RED}Version{RESET} \'{WHITE}{version}{RESET}\' {RED}isn\'t installed{RESET}\n')
            return 1
