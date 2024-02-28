""" Contain a single function for handling all of the
    command line options.
"""

from ziggyMethods import ZiggyMethods

def ziggy_options(option: str, /) -> callable:
    """ Map the first command line option
        to a function and return the function.
    """
    ZiggyMethods = ZiggyMethods()
    match option:
        case 'help': return ZiggyMethods.ziggy_help
        case 'show': return ZiggyMethods.ziggy_show
        case 'trigger': return ZiggyMethods.ziggy_trigger
        case 'collect': return ZiggyMethods.ziggy_collect
        case 'install': return ZiggyMethods.ziggy_install
        case 'upgrade': return ZiggyMethods.ziggy_upgrade
        case 'destroy': return ZiggyMethods.ziggy_destroy
        case _: return ZiggyMethods.ziggy_emiterr
