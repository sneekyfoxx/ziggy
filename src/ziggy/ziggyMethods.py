""" This file contains a class with methods for handling
    common ziggy operations.
"""

# Options:
#  help
#  show [installed | supported | active]
#  trigger VERSION
#  collect VERSION (default 'master')
#  install VERSION (default 'master')
#  upgrade
#  destroy VERSION

class ZiggyMethods:
    """ Contains methods for common ziggy operations.
    """
    __slots__ = ()
    stdout = sys.stdout.write
    stderr = sys.stderr.write
    red = "\x1b[1;31m"
    green = "\x1b[1;32m"
    cyan = "\x1b[1;36m"
    white = "\x1b[1;37m"
    reset = "\x1b[0m"

    def __new__(cls, /) -> object:
        cls.instance = None
        if cls.instance is None:
            cls.instance = super(ZiggyMethods, cls).__new__(cls)
        return cls.instance

    @classmethod
    def emiterr(msg: str) -> int:
        """ Output an error to standard error.
        """
        cls.stderr(f"{cls.red}{msg}{cls.reset}")
        return 1

    @classmethod
    def ziggy_help(cls, /) -> int:
        pass

    @classmethod
    def ziggy_show(cls, option: str, /) -> int:
        pass

    @classmethod
    def ziggy_trigger(cls, option: str, /) -> int:
        pass

    @classmethod
    def ziggy_collect(cls, option: str = "master", /) -> int:
        pass

    @classmethod
    def ziggy_install(cls, option: str = "master", /) -> int:
        pass

    @classmethod
    def ziggy_upgrade(cls, /) -> int:
        pass

    @classmethod
    def ziggy_destroy(cls, option: str, /) -> int:
        pass
