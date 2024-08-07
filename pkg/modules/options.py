from . import utils

utils.get_json()
utils.set_constants()

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

        name = utils.have_compiler(version)
        if name:
            exitcode = utils.output(f'{name!r} is already installed', mode='warn', exitcode=1)
            raise SystemExit(exitcode)
        else:
            exitcode = utils.output(f"Fetching version {utils.constants[version]!r}",  mode='normal', exitcode=0)
            utils.get_url(version)
            response = utils.requests.get(utils.constants['zig_url'])
            if response.status_code == 200:
                with open(utils.constants['archive'], 'wb') as archive:
                    archive.write(response.content)
                    archive.close()
                utils.shell_operation(option='move', name=utils.constants['archive'])
                utils.shell_operation(option='extract', name=utils.constants['archive'])
                utils.shell_operation(option='remove', name=utils.constants['archive'])
                exitcode = utils.output('Install Successful', mode='normal', exitcode=0)
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
    utils.sys.stdout.write(f'\n{cyan}Options              Description{reset}\n')
    utils.sys.stdout.write('-------              -----------\n')
    utils.sys.stdout.write(f' {green}delete{reset}    VERSION    {cyan}delete the given compiler version{reset}\n\n')
    utils.sys.stdout.write(f' {green}fetch{reset}     VERSION    {cyan}fetch the given compiler version from the internet{reset}\n\n')
    utils.sys.stdout.write(f' {green}help{reset}                 {cyan}display all options for ziggy{reset}\n\n')
    utils.sys.stdout.write(f' {green}use{reset}       VERSION    {cyan}use version as the primary compiler{reset}\n\n')
    utils.sys.stdout.write(f' {green}upgrade{reset}   VERSION    {cyan}upgrade the given compiler to the latest version{reset}\n\n')
    utils.sys.stdout.write(f'{cyan}Usage{reset}\n-----\n')
    utils.sys.stdout.write(f'  {yellow}ziggy{reset} {green}delete{reset}   <stable | master>\n')
    utils.sys.stdout.write(f'  {yellow}ziggy{reset} {green}fetch{reset}    <stable | master>\n')
    utils.sys.stdout.write(f'  {yellow}ziggy{reset} {green}use{reset}      <stable | master>\n')
    utils.sys.stdout.write(f'  {yellow}ziggy{reset} {green}upgrade{reset}  <stable | master>\n\n')
    raise SystemExit(0)

# ziggy use version
def option_use(version: str, /) -> None:
    """ Use the the given compiler as the
        primary compiler version if installed.
    """
    if not isinstance(version, str):
        raise SystemExit(f"[<function option_activate>] expected 'version: str' got 'version: {type(version).__name__}'")
    else:
        if not utils.Path(utils.constants['ziggy']).exists():
            utils.Path(utils.constants['ziggy']).mkdir()

        name = utils.have_compiler(version)
        symlink = utils.constants['symlink']
        if utils.Path(symlink).is_symlink() and utils.constants[version] in utils.get_symlink_name():
            exitcode = utils.output(f'{name!r} is already in use.', mode='warn', exitcode=1)
            raise SystemExit(exitcode)
        else:
            utils.shell_operation(option='link', name=name)
            exitcode = utils.output(f'Using {name!r}', mode='normal', exitcode=0)
            raise SystemExit(exitcode)

# ziggy upgrade master
def option_upgrade(version: str, /) -> None:
    """ Upgrade the given compiler version to the lastest available version. """
    if not isinstance(version, str):
        raise SystemExit(f"[<function option_upgrade>] expected 'version: str' got 'version: {type(version).__name__}'")
    else:
        if not utils.Path(utils.constants['ziggy']).exists():
            utils.Path(utils.constants['ziggy']).mkdir()

        name = utils.have_compiler(version)
        if name != '':
            exitcode = utils.output(f"{name!r} is already installed.", mode="warn", exitcode=1)
            raise SystemExit(exitcode)
        elif version == "master":
            latest = utils.constants[version].split("-dev")[0]
            symlink = utils.constants['symlink']
            if utils.Path(symlink).is_symlink() and latest in utils.get_symlink_name():
                utils.shell_operation(option="unlink")
                utils.shell_operation(option="remove", name=utils.get_symlink_name())
                option_fetch(version)
            else:
                option_fetch(version)
        elif version == "stable":
            latest = utils.constants[version]
            symlink = utils.constants['symlink']
            if utils.Path(symlink).is_symlink() and latest in utils.get_symlink_name():
                utils.shell_operation(option="unlink")
                utils.shell_operation(option="remove", name=utils.get_symlink_name())
                option_fetch(version)
            else:
                option_fetch(version)
        else:
            exitcode = utils.output(f"{version!r} is not a valid version.", mode='error', exitcode=2)
            raise SystemExit(exitcode)




