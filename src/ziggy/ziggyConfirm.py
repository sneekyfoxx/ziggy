""" Contain a single function for confirming whether
    the current operating system and architecture is
    supported by Zig.
"""

def ziggy_confirm(system: str, arch: str, /) -> bool:
    """ Confirm if the current operating system
        and architecture is supported by Zig.
    """
    match (system, arch):
        case ('Windows', 'x86'): return True
        case ('Windows', 'x86_64'): return True
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
