import click
from echo import Echo
from pathlib import Path


@click.group(
    help="""TinyTyper is a tool that utilizes various techniques to write 
    files to devices when other tools aren't an option.""",
)
@click.option(
    "-i",
    "--input",
    type=click.Path(exists=True, dir_okay=False),
    help="Input file",
    required=True,
)
@click.option(
    "-o",
    "--output",
    type=click.File("w"),
    help="Output file. If not provided, prints to stdout.",
)
@click.option(
    "-r",
    "--remote-file",
    type=click.Path(dir_okay=False),
    required=True,
    help="""The remote destination to which the file will be written. Can
    be a base file name or path, but file name must still be provided if
    path is given."""
)
@click.pass_context
def cli(ctx: click.Context, **kwargs):
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
@click.option(
    "-f",
    "--format",
    type=click.Choice(["bash", "tmux"]),
    default="bash",
    help="Format of the output script.",
    show_default=True,
)
@click.pass_context
def echo(ctx: click.Context, **kwargs):
    Echo(
        input=ctx.obj["input"],
        output=ctx.obj["output"],
        remote_file=ctx.obj["remote_file"],
        format=kwargs.get("format"),    
        chunk_size=kwargs.get("chunk_size"),
        no_n=kwargs.get("no_n"),
    ).run()


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
