import click
from pathlib import Path


@click.group(
    help="""TinyTyper is a tool that utilizes various techniques to write 
    files to devices when other tools aren't an option.""",
)
@click.option("-i", "--input", type=click.Path(exists=True), help="""Input file""", required=True)
@click.pass_context
def cli(ctx, **kwargs):
    ctx.ensure_object(dict)
    for key,val in kwargs.items():
        ctx.obj[key] = val
    pass


@click.command(short_help="Use printf on target to write files.")
def printf():
    print("TODO")


@click.command(short_help="Use awk on target to write files.")
@click.option("--stdout", is_flag=True, help="Print awk commands to stdout.")
def awk():
    print("TODO")


@click.command(short_help="Use echo on target to write files.")
@click.option(
    "--no-n",
    is_flag=True,
    default=False,
    help="""Use this flag when the '-n' option is not available on the target.""",
)
@click.pass_context
def echo(ctx, no_n):
    print(ctx.obj)
    print("TODO")


@click.command(short_help="Use vi on target to write files.")
def vi():
    print("TODO")

cli.add_command(echo)
cli.add_command(awk)
cli.add_command(printf)
cli.add_command(vi)

if __name__ == "__main__":
    cli()
