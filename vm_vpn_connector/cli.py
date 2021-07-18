import os

import click

from .config import PROJECT, VERBOSE, VERSION
from .utilities.utils import Utils

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------

# Program Header
# Basic user interface header
print(r'''    __  ____    ____          ___      __
   /  |/  / |  / / /___ _____/ (_)____/ /___ __   __
  / /|_/ /| | / / / __ `/ __  / / ___/ / __ `/ | / /
 / /  / / | |/ / / /_/ / /_/ / (__  ) / /_/ /| |/ /
/_/  /_/  |___/_/\__,_/\__,_/_/____/_/\__,_/ |___/''')
print('**************** 4D 56 6C 61 64 69 73 6C 61 76 *****************')
print('****************************************************************')
print('* Copyright of MVladislav, 2021                                *')
print('* https://mvladislav.online                                    *')
print('* https://github.com/MVladislav                                *')
print('****************************************************************')
print()

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


class Context:

    def __init__(self):
        self.verbose = VERBOSE

        self.utils: Utils = None

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(os.path.join(os.path.dirname(__file__), "./commands")):
            if filename.endswith(".py") and not filename.startswith("__"):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"{PROJECT}.commands.{name}", None, None, ["cli"])
            return mod.cli
        except ImportError as e:
            pass
            print(e)


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], ignore_unknown_options=True, auto_envvar_prefix="COMPLEX")

pass_context = click.make_pass_decorator(Context, ensure=True)


@click.command(cls=ComplexCLI, context_settings=CONTEXT_SETTINGS)
@click.version_option(VERSION)
@click.option('-v', '--verbose', count=True, help='Enables verbose mode', default=None)
@click.option('-pom', '--print-only-mode', is_flag=True, help='command wil only printed and not run')
@pass_context
def cli(ctx, verbose, print_only_mode):
    """Welcome to vm-hack"""
    if verbose != None:
        ctx.verbose = verbose
    ctx.print_only_mode = print_only_mode
    ctx.utils = Utils(ctx)
