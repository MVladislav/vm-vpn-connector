import os
import re

import click
from decouple import config

from ..cli import Context, pass_context

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


class Connector():

    ctx: Context = None

    path = config('VPN_PATH', default=None)
    file_pass = f"pass.txt"
    file_extension = ".ovpn"
    size = 10
    search = None
    location = None

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def connect(self):
        self.ctx.utils.logging.info("SETUP:")
        self.ctx.utils.logging.info(f"  - {self.path=}")
        self.ctx.utils.logging.info(f"  - {self.file_pass=}")
        self.ctx.utils.logging.info(f"  - {self.size=}")
        self.ctx.utils.logging.info(f"  - {self.search=}")

        if self.path is not None:
            file_path_list = []
            [file_path_list.append((path, name)) for path, _, files in os.walk(self.path) for name in files if name.endswith(self.file_extension)]

            if len(file_path_list) > 0:
                if self.search != None:
                    file_path_list = [file for file in file_path_list if self.ctx.utils.normalize_caseless(
                        self.search) in self.ctx.utils.normalize_caseless(file[1])]

                self.print_locations(file_path_list)

                try:
                    file_path = next((file for file in file_path_list if re.search(fr'{self.location}', file[1])), None)
                    if file_path is not None:
                        file = os.path.join(file_path[0], file_path[1])
                        file_pass = os.path.join(file_path[0], self.file_pass)

                        if not os.path.isfile(file_pass):
                            file_pass = None

                        print()
                        self.ctx.utils.logging.info(f"{file=}")
                        self.ctx.utils.logging.info(f"{file_pass=}")

                        self.vpn_add(file)

                        if file_pass is not None:
                            self.ctx.utils.run_command_endless(
                                ['sudo', 'openvpn', '--auth-nocache', '--allow-compression', 'yes', '--data-ciphers', 'AES-256-GCM:AES-128-GCM:AES-256-CBC',
                                 '--cipher', 'AES-256-GCM', '--config', file, '--auth-user-pass', file_pass])
                        else:
                            self.ctx.utils.run_command_endless(['sudo', 'openvpn', '--auth-nocache', '--allow-compression', 'yes',
                                                               '--data-ciphers', 'AES-256-GCM:AES-128-GCM:AES-256-CBC', '--cipher', 'AES-256-GCM', '--config', file])
                    else:
                        print()
                        self.ctx.utils.logging.warning("choosed file not found")
                except re.error:
                    self.ctx.utils.logging.exception(f"location is not a valid regex:: {self.location}")
            else:
                print()
                self.ctx.utils.logging.warning("no vpn files found")
        else:
            print()
            self.ctx.utils.logging.warning("no path defined 'export VPN_PATH='")

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def print_locations(self, file_path_list):
        if self.location is None:
            file_path_list.sort(key=lambda tup: tup[1])

            files_s = [f"{file[1].split('.')[0]}/{(file[1].split('.')[3] if len(file[1].split('.')) > 3 else '')}" for file in file_path_list]
            files_s = self.ctx.utils.group(files_s, self.size)
            print()
            [self.ctx.utils.logging.info(file) for file in files_s]

            print()
            self.location = input("location?: ")

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def vpn_add(self, file):
        add_list = [
            "dhcp-option DOMAIN 1.1.1.1",
            "script-security 2",
            "up /etc/openvpn/update-resolv-conf",
            "up-restart",
            "down /etc/openvpn/update-resolv-conf",
            "down-pre",
            "dhcp-option DOMAIN-ROUTE .",
        ]

        with open(file, 'r+') as fh:
            # text = fh.read()

            # for add_l in add_list:
            #     add_l_r = re.escape(add_l)
            #     print(rf"^{add_l_r}")

            #     # fh.seek(0)
            #     fh.write(re.sub(rf'^{add_l_r}', rf'{add_l_r}\n', text))

            for add_l in add_list:
                for line in fh:
                    if add_l in line:
                        break
                else:  # not found, we are at the eof
                    fh.write(f"{add_l}\r\n")  # append missing data

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------

@click.command()
@click.option("-p", "--path", help="path to vpn files", type=str, required=False)
@click.option("-s", "--search", help="search to search for openvpn files", type=str, required=False)
@click.option("-m", "--matrix", help="matrix size to print locations", type=int, required=False)
@click.option("-l", "--location", help="location to connect to", type=str, required=False)
@pass_context
def cli(ctx: Context, path, search, matrix, location):
    '''
        Connect to VPN
    '''
    # ctx.utils.logging.info(ctx.verbose)

    ctx.conn = Connector(ctx)
    if path is not None:
        ctx.conn.path = path
    if search is not None:
        ctx.conn.search = search
    if matrix is not None:
        ctx.conn.size = matrix
    if location is not None:
        ctx.conn.location = location
    ctx.conn.connect()
