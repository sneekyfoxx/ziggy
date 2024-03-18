from modules.utils import sys
from modules.utils import output
from modules import options

def main(argc: int, argv: list[str], /) -> None:
    if argc == 0:
        return options.option_help()
    elif argc == 1:
        match argv[0]:
            case 'help':
                options.option_help()
            case 'activate':
                exitcode = output('Not enough arguments', mode='error', exitcode=1)
                raise SystemExit(exitcode)
            case 'delete':
                exitcode = output('Not enough arguments', mode='error', exitcode=1)
                raise SystemExit(exitcode)
            case 'fetch':
                exitcode = output('Not enough arguments', mode='error', exitcode=1)
                raise SystemExit(exitcode)
            case 'show':
                exitcode = output('Not enough arguments', mode='error', exitcode=1)
                raise SystemExit(exitcode)
            case _:
                exitcode = output('Invalid option', mode='error', exitcode=1)
                raise SystemExit(exitcode)
    elif argc == 2:
        match argv[0]:
            case 'help':
                exitcode = output('Too many arguments', mode='error', exitcode=1)
                raise SystemExit(exitcode)
            case 'activate':
                options.option_activate(argv[1])
            case 'delete':
                options.option_delete(argv[1])
            case 'fetch':
                options.option_fetch(argv[1])
            case 'show':
                options.option_show(argv[1])
            case _:
                exitcode = output('Invalid option', mode='error', exitcode=1)
                raise SystemExit(exitcode)
    else:
        exitcode = output('Too many options and arguments', mode='error', exitcode=1)
        raise SystemExit(exitcode)

if __name__ == '__main__':
    argv = sys.argv[1:]
    argc = len(argv)
    main(argc, argv)