import logging
import os
import re
import sys
from ipaddress import IPv4Network
from typing import List, Union

from ..utils.utils import Context, Utils

# import verboselogs


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


# class TestService:

#     # --------------------------------------------------------------------------
#     #
#     #
#     #
#     # --------------------------------------------------------------------------

#     def test(self) -> None:
#         '''
#             ...
#         '''
#         service_name: str = 'TEST'
#         log_runBanner(service_name)
#         path: str = self.utils.create_service_folder(f'scan/test', None)

#         self.utils.run_command_output_loop('test', [
#             [],
#             ['tee', f'{path}/test.log']
#         ])

#         logging.log(verboselogs.SUCCESS, f'[*] {service_name} Done! View the log reports under {path}/')


class ConnectorService():

    file_pass = f"pass.txt"
    file_extension = ".ovpn"

    vpn_conf_add_item: List[str] = [
        # "dhcp-option DOMAIN 1.1.1.1",
        # "script-security 2",
        "block-outside-dns",
        "up /etc/openvpn/update-resolv-conf",
        "up-restart",
        "down /etc/openvpn/update-resolv-conf",
        "down-pre",
        # "dhcp-option DOMAIN-ROUTE .",
    ]

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def __init__(self, ctx: Context):
        if ctx is not None and ctx.utils is not None:
            self.ctx: Context = ctx
            self.utils: Utils = ctx.utils
            logging.log(logging.DEBUG, 'connection-service is initiated')
        else:
            logging.log(logging.ERROR, "context or utils are not set")
            sys.exit(1)

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def connect(self, path: Union[str, None] = None, search: Union[str, None] = None,
                matrix: int = 10, location: Union[str, None] = None,
                network: Union[str, None] = None, gateway: Union[str, None] = None,
                metric: int = 50, script_security: int = 0, append_options_to_file: bool = True) -> None:
        try:
            logging.log(logging.DEBUG, "SETUP:")
            logging.log(logging.DEBUG, f"  - {path=}")
            logging.log(logging.DEBUG, f"  - {self.file_pass=}")
            logging.log(logging.DEBUG, f"  - {self.file_extension=}")
            logging.log(logging.DEBUG, f"  - {matrix=}")
            logging.log(logging.DEBUG, f"  - {search=}")
            logging.log(logging.DEBUG, f"  - {network=}")
            logging.log(logging.DEBUG, f"  - {gateway=}")
            logging.log(logging.DEBUG, f"  - {metric=}")
            logging.log(logging.DEBUG, f"  - {script_security=}")

            self.location = location

            option_route = []
            if network is not None:
                ip = IPv4Network(network)
                option_route = ['--route', str(ip.network_address)]
                if gateway is not None:
                    option_route.append(str(ip.netmask))
                    option_route.append(gateway)
                    option_route.append(str(metric))
            options = ['--auth-nocache', '--data-ciphers', 'AES-256-GCM:AES-128-GCM:AES-256-CBC:AES-128-CBC',
                       '--allow-compression', 'yes', '--script-security', str(script_security), '--cipher', 'AES-256-GCM']+option_route

            if path is not None:
                file_path_list = []
                for path, _, files in os.walk(path):
                    for name in files:
                        if name.endswith(self.file_extension):
                            file_path_list.append((path, name))

                if len(file_path_list) > 0:
                    if search is not None:
                        file_path_list = [file for file in file_path_list if self.utils.normalize_caseless(
                            search) in self.utils.normalize_caseless(file[1])]

                    self.print_locations(file_path_list=file_path_list, matrix=matrix)

                    try:
                        file_path = next((file for file in file_path_list if re.search(fr'{self.location}', file[1])), None)
                        if file_path is not None:
                            file = os.path.join(file_path[0], file_path[1])
                            file_pass: Union[str, None] = os.path.join(file_path[0], self.file_pass)

                            if file_pass is not None and not os.path.isfile(file_pass):
                                file_pass = None

                            print()
                            logging.log(logging.INFO, f"{file=}")
                            logging.log(logging.INFO, f"{file_pass=}")

                            if append_options_to_file:
                                self.vpn_add(file=file)

                            command: List[str] = []
                            if file_pass is not None:
                                command = ['sudo', 'openvpn',
                                           '--config', file,
                                           '--auth-user-pass', file_pass]+options
                            else:
                                command = ['sudo', 'openvpn',
                                           '--config', file]+options
                            self.utils.run_command_endless(command)
                            # self.utils.run_command(command_list=command)
                        else:
                            logging.log(logging.WARNING, "choosed file not found")
                    except re.error:
                        logging.log(logging.CRITICAL, f"location is not a valid regex:: {self.location}")
                else:
                    logging.log(logging.WARNING, "no vpn files found")
            else:
                logging.log(logging.WARNING, "no path defined 'export VPN_PATH='")
        except KeyboardInterrupt:
            pass

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def print_locations(self, file_path_list, matrix: int):
        if self.location is None:
            file_path_list.sort(key=lambda tup: tup[1])

            files_s = [
                f"{file[1].split('.')[0]}/{(file[1].split('.')[3] if len(file[1].split('.')) > 3 else '')}" for file in file_path_list]
            files_s = self.utils.group(files_s, matrix)
            print()
            for file in files_s:
                logging.log(logging.INFO, file)

            print()
            self.location = input("location?: ")

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    def vpn_add(self, file: str):

        with open(file, 'r+') as fh:
            # text = fh.read()

            # for add_l in vpn_conf_add_item:
            #     add_l_r = re.escape(add_l)
            #     print(rf"^{add_l_r}")

            #     # fh.seek(0)
            #     fh.write(re.sub(rf'^{add_l_r}', rf'{add_l_r}\n', text))

            for add_l in self.vpn_conf_add_item:
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
