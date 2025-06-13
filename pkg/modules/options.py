from . import utils


class ZiggyOptions:

    def __init__(self, /):
        self.ziggy_utils = utils.ZiggyUtils()

    def option_delete(self, branch, /):
        """ Delete the given compiler branch if
            installed.
        """
        if not isinstance(branch, str):
            raise SystemExit(f"[<function option_delete>] expected 'branch: str' got 'branch: {type(branch).__name__}'")
        else:
            self.ziggy_utils.branch_check(branch)
            if branch == 'master':
                self.ziggy_utils.prefetch_master()
            else:
                self.ziggy_utils.prefetch_stable()

            self.ziggy_utils.operation('remove')
            exitcode = self.ziggy_utils.output(f'Removed {self.ziggy_utils.branch_upstream["dirname"]}', mode='normal', exitcode=0)
            raise SystemExit(exitcode)

    def option_fetch(self, branch, /):
        """ Fetch the given compiler if the current platform and architecture are supported. """
        if not isinstance(branch, str):
            raise SystemExit(f"[<function option_fetch>] expected 'branch: str' got 'branch: {type(branch).__name__}'")

        self.ziggy_utils.branch_check(branch)
        if branch == 'master':
            self.ziggy_utils.prefetch_master()
        else:
            self.ziggy_utils.prefetch_stable()

        if self.ziggy_utils.branch_local.name == self.ziggy_utils.branch_upstream['dirname'].name:
            exitcode = self.ziggy_utils.output(f"{self.ziggy_utils.branch_local} is already installed", mode='warn', exitcode=1)
            raise SystemExit(exitcode)
        else:
            _ = self.ziggy_utils.output(f'Fetching {self.ziggy_utils.platform_info["archive_name"]}', mode='normal', exitcode=0)
            archive_download = utils.requests.get(self.ziggy_utils.branch_upstream['archive_url'])

            if archive_download.status_code == 200:
                with open(self.ziggy_utils.platform_info['archive_name'].name, 'wb') as zig_archive:
                    zig_archive.write(archive_download.content)
                    zig_archive.close()

                self.ziggy_utils.operation("unlink")
                self.ziggy_utils.operation("remove")
                self.ziggy_utils.operation('extract', self.ziggy_utils.platform_info['archive_name'].name)
                self.ziggy_utils.operation('remove', self.ziggy_utils.platform_info['archive_name'].name)
                raise SystemExit(self.ziggy_utils.output('Install Successful', mode='normal', exitcode=0))
            else:
                raise SystemExit(self.ziggy_utils.output('Fetch Failed', mode='error', exitcode=2))

    def option_help(self, /):
        """ Display all options for the ziggy utility. """
        green = "\x1b[1;32m"
        yellow = "\x1b[1;33m"
        cyan = "\x1b[1;36m"
        reset = "\x1b[0m"

        utils.sys.stdout.write(f'\n{cyan}OPTIONS{reset}\n-------\n')
        utils.sys.stdout.write(f' {green}delete    {yellow}stable|master    {cyan}delete the given compiler{reset}\n\n')
        utils.sys.stdout.write(f' {green}fetch     {yellow}stable|master    {cyan}fetch the given compiler{reset}\n\n')
        utils.sys.stdout.write(f' {green}help                       {cyan}display all options for ziggy{reset}\n\n')
        utils.sys.stdout.write(f' {green}use       {yellow}stable|master    {cyan}use branch as the primary compiler{reset}\n\n')
        raise SystemExit(0)

    def option_use(self, branch, /):
        """ Use the the given compiler as the
            primary compiler branch if installed.
        """
        if not isinstance(branch, str):
            raise SystemExit(f"[<function option_activate>] expected 'branch: str' got 'branch: {type(branch).__name__}'")
        else:
            self.ziggy_utils.branch_check(branch)
            if branch == 'master':
                self.ziggy_utils.prefetch_master()
            else:
                self.ziggy_utils.prefetch_stable()

            for local_branch in self.ziggy_utils.ziggy_path.iterdir():
                match branch:
                    case 'master':
                        if self.ziggy_utils.branch_default.name != local_branch.name and 'dev' in local_branch.name:
                            self.ziggy_utils.operation('link', utils.os.path.join(local_branch.name, 'zig'))
                            raise SystemExit(self.ziggy_utils.output(f'Using {local_branch.name!r}', mode='normal', exitcode=0))

                        elif self.ziggy_utils.branch_default.name == local_branch.name and 'dev' in local_branch.name:
                            self.ziggy_utils.operation('link', utils.os.path.join(local_branch.name, 'zig'))
                            raise SystemExit(self.ziggy_utils.output(f'{local_branch.name!r} already set as default.', mode='warn', exitcode=1))

                        else:
                            continue
                    case 'stable':
                        if self.ziggy_utils.branch_default.name != local_branch.name and 'dev' not in local_branch.name:
                            self.ziggy_utils.operation('link', utils.os.path.join(local_branch.name, 'zig'))
                            raise SystemExit(self.ziggy_utils.output(f'Using {local_branch.name!r}', mode='normal', exitcode=0))

                        elif self.ziggy_utils.branch_default.name == local_branch.name and 'dev' not in local_branch.name:
                            self.ziggy_utils.operation('link', utils.os.path.join(local_branch.name, 'zig'))
                            raise SystemExit(self.ziggy_utils.output(f'{local_branch.name!r} already set as default.', mode='warn', exitcode=1))

                        else:
                            continue
