""" Contain a single function for handling all of the
    command line options.
"""

from . import (
        RED,
        GREEN,
        WHITE,
        RESET
        )
from .ziggyMethods import ZiggyMethods

def ziggy_options(count: int, /, *options) -> int:
    """ Map the first command line option
        to a function and return the function.
    """
    Methods = ZiggyMethods()
    match count:
        case 0: return Methods.ziggy_help()
        case 1:
            match options[0]:
                case 'help': return Methods.ziggy_help()
                case 'list': return Methods.ziggy_emitter(f"{RED}missing{RESET} '{GREEN}installed or available{RESET}'\n")
                case 'primary': return Methods.ziggy_primary()
                case 'install': return Methods.ziggy_install()
                case 'upgrade': return Methods.ziggy_upgrade()
                case 'destroy': return Methods.ziggy_destroy()
                case 'version': return Methods.ziggy_version()
                case _: return Methods.ziggy_emitter(f"'{WHITE}{options[0]}{RESET}' {RED}isn't a valid option{RESET}\n")
        case 2:
            match options[0]:
                case 'help': return Methods.ziggy_emitter(f"{GREEN}help{RESET} {RED}doesn't need an input{RESET}\n")
                case 'list': return Methods.ziggy_list(options[1])
                case 'primary': return Methods.ziggy_primary(options[1])
                case 'install': return Methods.ziggy_install(options[1])
                case 'upgrade': return Methods.ziggy_emitter(f"{GREEN}upgrade{RESET} {RED}doesn't need an input{RESET}\n")
                case 'destroy': return Methods.ziggy_destroy(options[1])
                case 'version': return Methods.ziggy_emitter(f"{GREEN}version{RESET} {RED}doesn't need an input{RESET}\n")
                case _: return Methods.ziggy_emitter(f"'{WHITE}{options[0]}{RESET}' {RED}isn't a valid option{RESET}\n")
        case _: return Methods.ziggy_emitter(f"{RED}Too many options{RESET}\n")
