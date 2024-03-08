""" This file contains a class with methods for handling
    common ziggy operations.
"""

# Use lookup table for easier version control
# Reimplement install, primary, upgrade, and destroy
# Update changed names

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
    DEV_URL = "https://ziglang.org/builds"
    HOME = EXPANDUSER('~')
    ZIGGY_DIR = ''
    ZIG_LINK = ''
    SEP = ''
    DEV_NULL = ''
    TAR_CMD = ''
    LINK_CMD = ''
    UNLINK_CMD = ''
    RM_CMD = ''
    MV_CMD = ''
    VERSIONS = [
            '0.1.0', '0.2.0', '0.3.0', '0.4.0', '0.5.0', '0.6.0', '0.7.0', '0.7.1',
            '0.8.0', '0.8.1', '0.9.0', '0.9.1', '0.10.0', '0.10.1', '0.11.0', '0.12.0'
            ]
    DEV_VERSION = '0.12.0'
    EXTENSION = ''
    WINDOWS = ''
    MACOS = ''
    LINUX = ''
    FREEBSD = ''
    LATEST = ''
    AVAILABLE = list()

    def __new__(cls, /) -> object:
        """ Return a new 'signleton' object.
        """
        cls.instance = None
        if cls.PLATFORM == 'windows':
            cls.ZIGGY_DIR = f'{cls.HOME}\\.ziggy'
            cls.ZIG_LINK = 'c:\\Windows\\System32\\zig'
            cls.SEP = "\\"
            cls.EXTENSION = '.zip'
            cls.DEV_NULL = '2 > nul'
            cls.TAR_CMD = 'unzip'
            cls.LINK_CMD = f'mklink'
            cls.UNLINK_CMD = 'del'
            cls.RM_CMD = 'rmdir'
            cls.MV_CMD = 'move'
            if not EXISTS(cls.ZIGGY_DIR):
                RUN(f'mkdir {cls.ZIGGY_DIR} 2> nul', shell=True)
        
        elif cls.PLATFORM in ['darwin', 'linux', 'freebsd']:
            cls.ZIGGY_DIR = f'{cls.HOME}/.ziggy'
            cls.ZIG_LINK = '/usr/bin/zig'
            cls.SEP = "/"
            cls.EXTENSION = '.tar.xz'
            cls.DEV_NULL = '2>/dev/null'
            cls.TAR_CMD = 'tar xJf'
            cls.LINK_CMD = 'sudo ln -s'
            cls.UNLINK_CMD = 'sudo unlink'
            cls.RM_CMD = 'rm -r --interactive=never'
            cls.MV_CMD = 'mv'
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
        elif cls.PLATFORM in ['darwin', 'linux', 'freebsd'] and not EXISTS(f'{cls.HOME}/.ziggy'):
            RUN(f'mkdir {cls.HOME}/.ziggy 2>/dev/null', shell=True)
        return None

    @classmethod
    def ziggy_emitter(cls, message: str, /) -> int:
        """ Emit the given message to standard error.
        """
        STDERR(message)
        return 1

    @classmethod
    def ziggy_windows_collect(cls, /) -> int:
        """ Collect Zig compiler versions for the current
            Windows platform and architecture.
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
                    target = target.split('/')[-1]
                    target = target.replace('.zip', '')

                    if target.endswith('minisig'):
                        continue

                    if f'-{cls.PLATFORM}-{cls.PROCESSOR}-{cls.DEV_VERSION}-dev' in target:
                        cls.LATEST = target

                    match cls.PROCESSOR:
                        case 'x86':
                            if f'-{cls.PLATFORM}-i386-' in target or f'-{cls.PLATFORM}-x86-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case 'AMD64':
                            if f'-win64-' in target or f'-{cls.PLATFORM}-x86_64-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case 'aarch64':
                            if f'-{cls.PLATFORM}-aarch64-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case _:
                            continue
            else:
                STDOUT(f"{WHITE}[{request.status_code}]{RESET} {RED}Request Failed.{RESET}\n")
                return 1
        return 0

    @classmethod
    def ziggy_macos_collect(cls, /) -> int:
        """ Collect Zig compiler versions for the current
            MacOS platform and architecture.
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
                    target = target.split('/')[-1]
                    target = target.replace('.tar.xz', '')

                    if target.endswith('minisig'):
                        continue

                    if f'-{cls.PLATFORM}-{cls.PROCESSOR}-{cls.DEV_VERSION}-dev' in target:
                        cls.LATEST = target

                    match cls.PROCESSOR:
                        case 'x86_64':
                            if f'-{cls.PLATFORM}-x86_64-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case 'aarch64':
                            if f'-{cls.PLATFORM}-aarch64-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case _:
                            continue
            else:
                STDOUT(f"{WHITE}[{request.status_code}]{RESET} {RED}Request Failed.{RESET}\n")
                return 1
        return 0

    @classmethod
    def ziggy_linux_collect(cls, /) -> int:
        """ Collect Zig compiler versions for the current
            Linux platform and architecture.
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
                    target = target.split('/')[-1]
                    target = target.replace('.tar.xz', '')

                    if target.endswith('minisig'):
                        continue

                    if f'-{cls.PLATFORM}-{cls.PROCESSOR}-{cls.DEV_VERSION}-dev' in target:
                        cls.LATEST = target

                    match cls.PROCESSOR:
                        case 'x86':
                            if f'-{cls.PLATFORM}-i386-' in target or f'-{cls.PLATFORM}-x86-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case 'x86_64':
                            if f'-{cls.PLATFORM}-x86_64-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case 'aarch64':
                            if f'-{cls.PLATFORM}-aarch64-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case 'armv6kz':
                            if f'-{cls.PLATFORM}-armv6kz-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case 'armv7a':
                            if f'-{cls.PLATFORM}-armv7a-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case 'riscv64':
                            if f'-{cls.PLATFORM}-riscv64-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case 'powerpc64le':
                            if f'-{cls.PLATFORM}-powerpc64le-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case 'powerpc':
                            if f'-{cls.PLATFORM}-powerpc-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case _:
                            continue
            else:
                STDOUT(f"{WHITE}[{request.status_code}]{RESET} {RED}Request Failed.{RESET}\n")
                return 1
        return 0

    @classmethod
    def ziggy_freebsd_collect(cls, /) -> int:
        """ Collect Zig compiler versions for the current
            FreeBSD platform and architecture.
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
                    target = target.split('/')[-1]
                    target = target.replace('.tar.xz', '')

                    if target.endswith('minisig'):
                        continue

                    if f'-{cls.PLATFORM}-{cls.PROCESSOR}-{cls.DEV_VERSION}-dev' in target:
                        cls.LATEST = target

                    match cls.PROCESSOR:
                        case 'x86_64':
                            if f'-{cls.PLATFORM}-x86_64-' in target:
                                cls.AVAILABLE.insert(0, target)
                        case _:
                            continue
            else:
                STDOUT(f"{WHITE}[{request.status_code}]{RESET} {RED}Request Failed.{RESET}\n")
                return 1

    @classmethod
    def ziggy_populate(cls, /) -> int:
        """ Invoke the appropriate method for the current
            platform and architecture to populate the
            class variable 'AVAILABLE' list with all of
            the Zig compiler versions that support the
            current platform and architecture.
        """
        match cls.PLATFORM:
            case 'windows': return cls.ziggy_windows_collect()
            case 'darwin': return cls.ziggy_macos_collect()
            case 'linux': return cls.ziggy_linux_collect()
            case 'freebsd': return cls.ziggy_freebsd_collect()
            case _: return 1

    @classmethod
    def ziggy_get_target(cls, version: str, /) -> str | int:
        """ Get the target archive url containing the
            given version.
        """
        if version not in cls.VERSIONS:
            return 1
        elif cls.ziggy_populate() == 0:
            for available in cls.AVAILABLE:
                if version in available:
                    return available
                else:
                    continue
        else:
            return ""

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
        STDOUT(f"\n {PURPLE}version{RESET}            {WHITE}display the current ziggy version and exit{RESET}\n")
        return 0

    @classmethod
    def ziggy_list(cls, option: str = 'installed', /) -> int:
        """ List all of the installed Zig compilers
            on the system or the Zig compiler versions
            supported for the current platform and architecture.
        """
        if cls.ziggy_populate() == 1:
            STDOUT(f"{RED}Request Failed. Couldn't populate version list.{RESET}\n")
            return 1
        else:
            if option == 'supported':
                for version in cls.AVAILABLE:
                    STDOUT(f'{WHITE}->{RESET} {GREEN}{version}{RESET}\n')
                return 0
            elif option == 'installed':
                versions = [version.name for version in PATH(cls.ZIGGY_DIR).iterdir()]
                for version in versions:
                    version = version.split(cls.SEP)[-1]
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
        status = cls.ziggy_populate()
        supported = False
        if status == 1:
            STDERR(f'{RED}Couldn\'t populate version list.\n')
            return 1

        for available in cls.AVAILABLE:
            if version in available:
                supported = True
                break

        if supported is False:
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
                    set_this = ''
                    for entry in SCANDIR(cls.ZIGGY_DIR):
                        if entry.is_dir(follow_symlinks=False) and version in entry.name:
                            if version == '0.12.0' and entry.name == cls.LATEST:
                                link_zig = f'{cls.LINK_CMD} {cls.ZIGGY_DIR}{cls.SEP}{entry.name}{cls.SEP}zig {cls.ZIG_LINK} {cls.DEV_NULL}'
                                if zig_linked:
                                    RUN(f'{cls.UNLINK_CMD} {cls.ZIG_LINK} {cls.DEV_NULL}', shell=True)
                                    linked = RUN(link_zig, shell=True).returncode
                                    primary = entry.name
                                    break
                                else:
                                    linked = RUN(link_zig, shell=True).returncode
                                    primary = entry.name
                                    break
                            elif version != '0.12.0':
                                link_zig = f'{cls.LINK_CMD} {cls.ZIGGY_DIR}{cls.SEP}{entry.name}{cls.SEP}zig {cls.ZIG_LINK} {cls.DEV_NULL}'
                                if zig_linked:
                                    RUN(f'{cls.UNLINK_CMD} {cls.ZIG_LINK} {cls.DEV_NULL}', shell=True)
                                    linked = RUN(link_zig, shell=True).returncode
                                    primary = entry.name
                                    break
                                else:
                                    linked = RUN(link_zig, shell=True).returncode
                                    primary = entry.name
                                    break
                            else:
                                continue
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
        target = cls.ziggy_get_target(version)
        if target == 1:
            STDERR(f"'{WHITE}{version}{RESET}' {RED}isn't a valid Zig compiler version.{RESET}\n")
            return 1
        elif target is None:
            STDERR(f"'{WHITE}{version}{RESET}' {RED}is not a valid version for your platform.{RESET}\n")
            return 1
        else:
            url = ''
            if version == '0.12.0':
                url = f'{cls.DEV_URL}/{cls.LATEST}{cls.EXTENSION}'
                for installed in SCANDIR(cls.ZIGGY_DIR):
                    if installed.is_dir(follow_symlinks=False) and version in installed.name:
                        RUN(f'{cls.RM_CMD} {installed.name} {cls.DEV_NULL}', shell=True)
            else:
                for available in cls.AVAILABLE:
                    if version in available:
                        url = f'{cls.BASE_URL}/{version}/{available}{cls.EXTENSION}'
                        break

            request = REQUEST('GET', url)
            zig_archive = target + cls.EXTENSION

            if request.status_code == 200:
                with open(zig_archive, 'wb') as archive:
                    archive.write(request.content)
                    request.close()
                    RUN(f'{cls.MV_CMD} .{cls.SEP}{zig_archive} {cls.ZIGGY_DIR}{cls.SEP}{zig_archive}', shell=True)
                    RUN(f'cd {cls.ZIGGY_DIR} && {cls.TAR_CMD} {zig_archive} && {cls.RM_CMD} {zig_archive}', shell=True)
                    STDOUT(f'{GREEN}Install Complete!{RESET}\n')
                    return 0
            else:
                STDERR(f'{RED}Install Failed!{RESET}\n')
                return 1


    @classmethod
    def ziggy_upgrade(cls, /) -> int:
        """ Upgrade the primary Zig compiler to the
            latest Zig compiler version if not installed.
        """
        status = cls.ziggy_populate()

        if status == 1:
            return 1
        else:
            installed = False
            for version in PATH(cls.ZIGGY_DIR).iterdir():
                version = version.name.split(cls.SEP)[-1]
                if version == cls.LATEST:
                    installed = True
                    STDOUT(f'{GREEN}The latest Zig compiler is already installed{RESET}\n')
                    break
                else:
                    continue
            
            if installed:
                return 0
            else:
                cls.ziggy_install('0.12.0')
                return 0

    @classmethod
    def ziggy_destroy(cls, version: str = "", /) -> int:
        """ Destroy / remove a compiler of choice if the
            specified version is installed.
        """
        if cls.ziggy_populate() == 1:
            return 1

        if version not in cls.VERSIONS:
            STDERR(f'\'{WHITE}{version}{RESET}\' {RED}isn\'t a valid Zig compiler version{RESET}\n')
            return 1
        else:
            destroyed = False
            primary = PATH(cls.ZIG_LINK).resolve().parent.name
            for installed in PATH(cls.ZIGGY_DIR).iterdir():
                installed = installed.name.split(cls.SEP)[-1]

                if version in installed and installed != primary:
                    status = RUN(f'{cls.RM_CMD} {cls.ZIGGY_DIR}{cls.SEP}{installed} {cls.DEV_NULL}', shell=True)
                    STDOUT(f'{GREEN}Destroyed{RESET} \'{WHITE}{installed}{RESET}\'\n')
                    if status.returncode == 0:
                        destroyed = True
                else:
                    continue
            if destroyed is False:
                STDERR(f'{RED}Version{RESET} \'{WHITE}{version}{RESET}\' {RED}isn\'t installed{RESET}\n')
                return 1
        return 0

    @classmethod
    def ziggy_version(cls, /) -> int:
        """ Display the current 'ziggy' version.
        """
        STDOUT(f'{GREEN}ziggy-v1.0{RESET}\n')
        return 0
