from . import utils

utils.set_constants()

# ziggy activate version
def option_activate(version: str, /) -> None:
    """ Activate the the given compiler as the
        primary compiler version if installed.
    """
    if not isinstance(version, str):
        raise SystemExit(f"[<function option_activate>] expected 'version: str' got 'version: {type(version).__name__}'")
    else:
        if not utils.Path(utils.constants['ziggy']).exists():
            utils.Path(utils.constants['ziggy']).mkdir()

        symlink = utils.constants['symlink']
        if utils.Path(symlink).is_symlink() and version in utils.get_symlink_name():
            exitcode = utils.output(f'{version!r} is already active.', mode='warn', exitcode=1)
            raise SystemExit(exitcode)
        else:
            name = utils.have_compiler(version)
            utils.shell_operation(option='link', name=name)
            exitcode = utils.output(f'{name!r} is active', mode='normal', exitcode=0)
            raise SystemExit(exitcode)

# ziggy delete version
def option_delete(version: str, /) -> None:
    """ Delete the given compiler version if
        installed.
    """
    if not isinstance(version, str):
        raise SystemExit(f"[<function option_delete>] expected 'version: str' got 'version: {type(version).__name__}'")
    else:
        if not utils.Path(utils.constants['ziggy']).exists():
            utils.Path(utils.constants['ziggy']).mkdir()

        name = utils.have_compiler(version)
        if name != '':
            if name == utils.get_symlink_name():
                utils.shell_operation(option='unlink')
                utils.shell_operation(option='remove', name=name)
                exitcode = utils.output(f'Deleted {name!r}', mode='normal', exitcode=0)
                raise SystemExit(exitcode)
            else:
                utils.shell_operation(option='remove', name=name)
                exitcode = utils.output(f'Deleted {name!r}', mode='normal', exitcode=0)
                raise SystemExit(exitcode)
        else:
            exitcode = utils.output(f'Version {version!r} not installed', mode='warn', exitcode=1)
            raise SystemExit(exitcode)

# ziggy fetch version
def option_fetch(version: str, /) -> None:
    """ Fetch the given compiler version from
        the internet if such a version exists
        or if it supports the currrent platform
        and architecture and install it to the
        system.
    """
    if not isinstance(version, str):
        raise SystemExit(f"[<function option_fetch>] expected 'version: str' got 'version: {type(version).__name__}'")
    else:
        if not utils.Path(utils.constants['ziggy']).exists():
            utils.Path(utils.constants['ziggy']).mkdir()

        utils.match_version(version)
        utils.carve_archive_name()
        utils.carve_compiler_name()
        name = utils.have_compiler(version)
        if name:
            exitcode = utils.output(f'{version!r} is already installed', mode='warn', exitcode=1)
            raise SystemExit(exitcode)
        else:
            utils.match_version(version)
            response = utils.requests.get(utils.constants['zig_url'])
            if response.status_code == 200:
                with open(utils.constants['archive'], 'wb') as archive:
                    archive.write(response.content)
                    archive.close()
                utils.shell_operation(option='move', name=utils.constants['archive'])
                utils.shell_operation(option='extract', name=utils.constants['archive'])
                utils.shell_operation(option='remove', name=utils.constants['archive'])
                exitcode = utils.output(f'Install Successful', mode='normal', exitcode=0)
                raise SystemExit(exitcode)
            else:
                exitcode = utils.output(f'Failed to fetch version {version!r}', mode='error', exitcode=2)
                raise SystemExit(exitcode)

# ziggy help
def option_help() -> None:
    """ Display all options for the ziggy utility. """
    green = "\x1b[38;2;50;255;50m"
    yellow = "\x1b[38;2;255;255;50m"
    cyan = "\x1b[38;2;50;255;255m"
    reset = "\x1b[0m"
    utils.sys.stdout.write(f'\n{yellow}NOTE:{reset} {cyan}[VERSION] must take the form "major.minor.patch", eg. 0.0.0{reset}\n')
    utils.sys.stdout.write(f'\n{cyan}Options              Description{reset}\n')
    utils.sys.stdout.write('-------              -----------\n')
    utils.sys.stdout.write(f' {green}activate{reset}  VERSION    {cyan}activate version as the primary compiler{reset}\n\n')
    utils.sys.stdout.write(f' {green}delete{reset}    VERSION    {cyan}delete the given compiler version{reset}\n\n')
    utils.sys.stdout.write(f' {green}fetch{reset}     VERSION    {cyan}fetch the given compiler version from the internet{reset}\n\n')
    utils.sys.stdout.write(f' {green}help{reset}                 {cyan}display all options for ziggy{reset}\n\n')
    utils.sys.stdout.write(f' {green}show{reset}      COMMAND    {cyan}display the [active], [inactive], or [supported] version(s){reset}\n')
    raise SystemExit(0)

# ziggy show [active | inactive | supported]
def option_show(option: str, /) -> None:
    """ Show the active, inactive, and supported compilers.
        Show all compiler versions.
    """
    if not isinstance(option, str):
        raise SystemExit(f"[<function option_show>] expected 'option: str' got 'option: {type(option).__name__}'")
    else:
        exitcode = 1
        if not utils.Path(utils.constants['ziggy']).exists():
            utils.Path(utils.constants['ziggy']).mkdir()

        match option:
            case 'active':
                name = utils.get_symlink_name()
                if name:
                    exitcode = utils.output(f'{utils.get_symlink_name()}', mode='normal', exitcode=0)
                    raise SystemExit(exitcode)
                else:
                    exitcode = utils.output('There is no active compiler', mode='normal', exitcode=0)
                    raise SystemExit(exitcode)
            case 'inactive':
                name = utils.get_symlink_name()
                if name != '':
                    for installed in utils.Path(utils.constants['ziggy']).iterdir():
                        if installed.name != name:
                            exitcode = utils.output(f'{installed}', mode='normal', exitcode=0)
                        raise SystemExit(exitcode)
                else:
                    for installed in utils.Path(utils.constants['ziggy']).iterdir():
                        exitcode = utils.output(f'{installed}', mode='normal', exitcode=0)
                    raise SystemExit(exitcode)
            case 'supported':
                for supported in utils.constants['supported']:
                    supported = supported.split('/')[-1].replace(utils.constants['extension'], '')
                    exitcode = utils.output(f'{supported}', mode='normal', exitcode=0)
                raise SystemExit(exitcode)
            case _:
                exitcode = utils.output(f'Invalid option {option!r}', mode='error', exitcode=2)
                raise SystemExit(exitcode)
