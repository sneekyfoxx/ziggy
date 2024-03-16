from . import utils

# constants must be set before this function is invoked
# match_version() must be invoked before this function
# extract_name() must be invoked before this function
async def shell_operation(option: str, /, version: str = '') -> int:
    """ Perform a shell operation based on a given option. """
    if not isinstance(option, str):
        raise SystemExit(f"[<function shell_operation>] expected 'option: str' got 'option: {type(option).__name__}'")
    elif option == 'install':
        match_version(version)
        extract_name(constants['version'])
        exitcode = subprocess.run()