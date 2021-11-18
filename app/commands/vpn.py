import io
import logging
import sys
import zipfile

import click
import requests

from ..service.connector_service import ConnectorService
from ..utils.config import VPN_PATH
from ..utils.utils import Context, pass_context

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


@click.group()
@pass_context
def cli(ctx: Context):
    '''
        VPN tool
    '''
    if ctx.utils is not None:
        ctx.service = ConnectorService(ctx)
    else:
        logging.log(logging.ERROR, f'utils are not set')
        sys.exit(1)


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


@cli.command()
@click.option("-p", "--path", type=click.Path(exists=True),
              help=f"path to vpn files folder [{VPN_PATH}]", required=True, default=VPN_PATH)
@click.option("-s", "--search", type=str,
              help="to search for openvpn files (regex)")
@click.option("-m", "--matrix", type=int,
              help="matrix size to print locations [10]", default=10)
@click.option("-l", "--location", type=click.Path(exists=True),
              help="location to connect to")
@click.option("-n", "--network", type=str,
              help="define a private network to route extra")
@click.option("-g", "--gateway", type=str,
              help="define a private gateway to route network")
@click.option("-ss", "--script-security", type=int,
              help="script-security [0]", default=0)
@click.option("-p", "--path", type=click.Path(exists=True),
              help=f"path to vpn base download folder [{VPN_PATH}]", required=True, default=VPN_PATH)
@pass_context
def connect(ctx: Context, path: str, search: str, matrix: int, location: str,
            gateway: str, network: str, script_security: int):
    '''
        Connect to VPN
    '''
    try:
        service: ConnectorService = ctx.service
        service.connect(path=path, search=search, matrix=matrix, location=location,
                        network=network, gateway=gateway, script_security=script_security)
    except KeyboardInterrupt as k:
        logging.log(logging.DEBUG, f'process interupted! ({k})')
        sys.exit(5)
    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
        sys.exit(2)

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


@cli.command()
@click.option("-p", "--path", type=click.Path(exists=False),
              help=f"path to vpn base download folder [{VPN_PATH}]", required=True, default=VPN_PATH)
@click.option("-n", "--name", type=str,
              help="folder name to extract [nordVPN]", required=True, default="nordVPN")
@pass_context
def nordvpn(ctx: Context, path: str, name: str):
    '''
        download nordVPN files
    '''
    try:
        service: ConnectorService = ctx.service
        ctx.base_path = path
        path = service.utils.create_service_folder(name=name, split_host=False, split_project=False)
        url = 'https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip'

        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path)
    except KeyboardInterrupt as k:
        logging.log(logging.DEBUG, f'process interupted! ({k})')
        sys.exit(5)
    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
        sys.exit(2)
