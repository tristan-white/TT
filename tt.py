import click
from echo import Echo
from awk import Awk
from printf import Printf
from pathlib import Path


@click.group(
    help="""TinyTyper is a tool that utlizies various techniuqes to write
    files to devices when other tools aren't an option."""
)
@click.option(
    "-i",
    "--input",
    type=click.File(),
    help="Input file. Defaults to stdin.",
    default="-",
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
    path is given.""",
)
@click.option(
    "-f",
    "--format",
    type=click.Choice(["bash", "tmux"]),
    default="bash",
    help="""Format of the output script.""",
    show_default=True,
)
@click.pass_context
def cli(ctx: click.Context, **kwargs):
    ctx.max_content_width = 120  # makes help menu wider than default (80)
    ctx.ensure_object(dict)
    for key, val in kwargs.items():
        ctx.obj[key] = val
    pass


@click.command(short_help="Use awk on target to write files.")
@click.option(
    "--chunk-size",
    default=16,
    show_default=True,
    help="""The number of bytes written with each echo command.""",
)
@click.pass_context
def awk(ctx: click.Context, **kwargs):
    Awk(
        input=ctx.obj["input"],
        output=ctx.obj["output"],
        remote_file=ctx.obj["remote_file"],
        format=ctx.obj["format"],
        chunk_size=kwargs.get("chunk_size"),
    ).run()


@click.command(short_help="Use echo on target to write files.")
@click.option(
    "--chunk-size",
    default=64,
    show_default=True,
    help="""The number of bytes written with each echo command.""",
)
@click.option(
    "--head-c",
    is_flag=True,
    default=False,
    help="""Use echo in conjuction with 'head -c'. Use when the echo's -n
    option is not available.""",
    show_default=True,
)
@click.option(
    "--ansic",
    help="""Use ANSI-C Quoting to print bytes instead of echo's -e option.
    Note: ANSI-C Quoting cannot print null bytes; therefore, --head-c must 
    but used in conjunction with this option.""",
    is_flag=True,
    default=False,
    show_default=True,
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
        format=ctx.obj["format"],
        chunk_size=kwargs.get("chunk_size"),
        head_c=kwargs.get("head_c"),
    ).run()

@click.command()
@click.option(
    "--chunk-size",
    default=64,
    show_default=True,
    help="""The number of bytes written with each echo command.""",
)
@click.pass_context
def printf(ctx: click.Context, **kwargs):
    Printf(
        input=ctx.obj["input"],
        output=ctx.obj["output"],
        remote_file=ctx.obj["remote_file"],
        format=ctx.obj["format"],
        chunk_size=kwargs.get("chunk_size"),
    ).run()


cli.add_command(echo)
cli.add_command(awk)
cli.add_command(printf)


if __name__ == "__main__":
    cli()
