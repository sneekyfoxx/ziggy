""" Contain a single function for confirming whether
    the current operating system and architecture is
    supported by Zig.
"""

from . import SYSTEM, MACHINE

def ziggy_confirm() -> bool:
    """ Confirm if the current operating system
        and architecture is supported by Zig.
    """
    match (SYSTEM(), MACHINE()):
        case ('Windows', 'x86'): return True
        case ('Windows', 'AMD64'): return True
        case ('Windows', 'aarch64'): return True
        case ('Darwin', 'x86_64'): return True
        case ('Darwin', 'aarch64'): return True
        case ('Linux', 'x86'): return True
        case ('Linux', 'x86_64'): return True
        case ('Linux', 'aarch64'): return True
        case ('Linux', 'armv6kz'): return True
        case ('Linux', 'armv7a'): return True
        case ('Linux', 'riscv64'): return True
        case ('Linux', 'powerpc64le'): return True
        case ('Linux', 'powerpc'): return True
        case ('FreeBSD', 'x86_64'): return True
        case _: return False
