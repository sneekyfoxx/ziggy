from modules.utils import sys
from modules.utils import ZiggyUtils
from modules.options import ZiggyOptions

def main(argc: int, argv: list[str], /) -> None:
    ziggy_utils = ZiggyUtils()
    ziggy_options = ZiggyOptions()

    if argc == 0:
        return ziggy_options.option_help()
    elif argc == 1:
        match argv[0]:
            case 'delete':
                exitcode = ziggy_utils.output('Not enough arguments', mode='error', exitcode=2)
                raise SystemExit(exitcode)
            case 'fetch':
                exitcode = ziggy_utils.output('Not enough arguments', mode='error', exitcode=2)
                raise SystemExit(exitcode)
            case 'help':
                ziggy_options.option_help()
            case 'use':
                exitcode = ziggy_utils.output('Not enough arguments', mode='error', exitcode=2)
                raise SystemExit(exitcode)
            case _:
                exitcode = ziggy_utils.output('Invalid option', mode='error', exitcode=2)
                raise SystemExit(exitcode)
    elif argc == 2:
        match argv[0]:
            case 'delete':
                ziggy_options.option_delete(argv[1])
            case 'fetch':
                ziggy_options.option_fetch(argv[1])
            case 'help':
                exitcode = ziggy_utils.output('Too many arguments', mode='error', exitcode=2)
                raise SystemExit(exitcode)
            case 'use':
                ziggy_options.option_use(argv[1])
            case _:
                exitcode = ziggy_utils.output('Invalid option', mode='error', exitcode=2)
                raise SystemExit(exitcode)
    else:
        exitcode = ziggy_utils.output('Too many options and arguments', mode='error', exitcode=2)
        raise SystemExit(exitcode)

if __name__ == '__main__':
    argv = sys.argv[1:]
    argc = len(argv)
    main(argc, argv)
