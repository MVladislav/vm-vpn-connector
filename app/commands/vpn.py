import logging
import sys

import click

from ..service.connector_service import ConnectorService
from ..utils.config import VPN_PATH
from ..utils.utils import Context, pass_context

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


@click.group(invoke_without_command=True)
@click.option("-p", "--path", type=click.Path(exists=True),
              help=f"path to vpn files folder [{VPN_PATH}]", required=True, default=VPN_PATH)
@click.option("-s", "--search", type=str,
              help="to search for openvpn files (regex)")
@click.option("-m", "--matrix", type=int,
              help="matrix size to print locations [10]", default=10)
@click.option("-l", "--location", type=click.Path(exists=True),
              help="location to connect to")
@pass_context
def cli(ctx: Context, path: str, search: str, matrix: int, location: str):
    '''
        Connect to VPN
    '''
    if ctx.utils is not None:
        ctx.service = ConnectorService(ctx)
        ctx.service.connect(path=path, search=search, matrix=matrix, location=location)
    else:
        logging.log(logging.ERROR, f'utils are not set')
        sys.exit(1)


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
