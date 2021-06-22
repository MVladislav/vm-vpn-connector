import os

import click

# -------------------------------------------------------------------------------------------
#
#
#
# -------------------------------------------------------------------------------------------


class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(os.path.join(os.path.dirname(__file__), "../commands")):
            if filename.endswith(".py") and not filename.startswith("__"):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"vm_vpn_connector.commands.{name}", None, None, ["cli"])
        except ImportError:
            return
        return mod.cli

# -------------------------------------------------------------------------------------------
#
#
#
# -------------------------------------------------------------------------------------------


@click.command(cls=ComplexCLI)
@click.option("-v", "--verbose", is_flag=True, help="enables verbose mode")
@click.pass_context
def cli(ctx, verbose):
    """Welcome to vpn connector"""
    ctx.verbose = verbose
