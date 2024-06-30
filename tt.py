import click
from echo import Echo
from pathlib import Path


@click.group(
    help="""TinyTyper is a tool that utilizes various techniques to write 
    files to devices when other tools aren't an option.""",
)
@click.option(
    "-i",
    "--in-file",
    type=click.Path(exists=True),
    help="""Input file""",
    required=True,
)
@click.option(
    "-d",
    "--dest",
    type=click.Path(),
    help="""The remote destination on the target to which the in file will be written.""",
)
@click.pass_context
def cli(ctx, **kwargs):
    ctx.ensure_object(dict)
    for key, val in kwargs.items():
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
    "--chunk-size",
    default=64,
    show_default=True,
    help="""The number of bytes written with each echo command.""",
)
@click.option(
    "--no-n",
    is_flag=True,
    default=False,
    help="""Use this flag when the '-n' option is not available on the target.""",
)
@click.pass_context
def echo(ctx: dict, no_n: bool, chunk_size: int):
    Echo(ctx.obj["in_file"], no_n=no_n, chunk_size=chunk_size).run()

@click.command(short_help="Use vi on target to write files.")
def vi():
    print("TODO")


@click.command(short_help="Use lua on target to write files.")
def lua():
    print("TODO")


cli.add_command(echo)
cli.add_command(awk)
cli.add_command(printf)
cli.add_command(vi)

if __name__ == "__main__":
    cli()
