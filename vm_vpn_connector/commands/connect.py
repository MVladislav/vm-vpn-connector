import os
import re
import subprocess
import sys
import time
import unicodedata
from typing import Generator

import click
from decouple import config


class Context:

    path = config('VPN_PATH', default=None)
    file_pass = f"pass.txt"
    file_extension = ".ovpn"
    size = 10
    search = None
    location = None

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def __init__(self) -> None:
        pass

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def connect(self):
        print("SETUP:")
        print(f"  - {self.path=}")
        print(f"  - {self.file_pass=}")
        print(f"  - {self.size=}")
        print(f"  - {self.search=}")

        if self.path is not None:
            file_path_list = []
            [file_path_list.append((path, name)) for path, _, files in os.walk(self.path) for name in files if name.endswith(self.file_extension)]

            if len(file_path_list) > 0:
                if self.search != None:
                    file_path_list = [file for file in file_path_list if self.normalize_caseless(self.search) in self.normalize_caseless(file[1])]

                self.print_locations(file_path_list)

                try:
                    file_path = next((file for file in file_path_list if re.search(fr'{self.location}', file[1])), None)
                    if file_path is not None:
                        file = os.path.join(file_path[0], file_path[1])
                        file_pass = os.path.join(file_path[0], self.file_pass)

                        if not os.path.isfile(file_pass):
                            file_pass = None

                        print()
                        print(f"{file=}")
                        print(f"{file_pass=}")

                        self.vpn_add(file)
                        self.vpn(file, file_pass)
                    else:
                        print()
                        print("choosed file not found")
                except re.error:
                    print(f"location is not a valid regex:: {self.location}")
            else:
                print()
                print("no vpn files found")
        else:
            print()
            print("no path defined 'export VPN_PATH='")

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def print_locations(self, file_path_list):
        if self.location is None:
            file_path_list.sort(key=lambda tup: tup[1])

            files_s = [f"{file[1].split('.')[0]}/{(file[1].split('.')[3] if len(file[1].split('.')) > 3 else '')}" for file in file_path_list]
            files_s = self.group(files_s, self.size)
            print()
            [print(file) for file in files_s]

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

    def vpn(self, file, file_pass):
        x = None
        is_running = True
        try:
            if file_pass is not None:
                x = subprocess.Popen(['sudo', 'openvpn', '--auth-nocache', '--config', file, '--auth-user-pass', file_pass])
            else:
                x = subprocess.Popen(['sudo', 'openvpn', '--auth-nocache', '--config', file, '--auth-user-pass'])
            while is_running:
                time.sleep(600)
        # termination with Ctrl+C
        except:
            is_running = False
            print("process killed!")
        try:
            x.terminate()
        except:
            pass
        if x != None:
            while x.poll() == None:
                time.sleep(1)

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def group(self, flat, size): return [flat[i:i+size] for i in range(0, len(flat), size)]

    def normalize_caseless(self, text):
        return unicodedata.normalize("NFKD", text.casefold())


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
@click.pass_context
def cli(ctx, path, search, matrix, location):
    """Connect to VPN"""
    ctx.obj = Context()
    if path is not None:
        ctx.obj.path = path
    if search is not None:
        ctx.obj.search = search
    if matrix is not None:
        ctx.obj.size = matrix
    if location is not None:
        ctx.obj.location = location
    ctx.obj.connect()
