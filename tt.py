import click
from echo import Echo
from awk import Awk
from pathlib import Path


@click.group(
    help="""TinyTyper is a tool that utlizies various techniuqes to write
    files to devices when other tools aren't an option."""
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
    ctx.max_content_width = 120     # makes help menu wider than default (80)
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
        format=ctx.obj["format"],    
        chunk_size=kwargs.get("chunk_size"),
    ).run()


cli.add_command(echo)
cli.add_command(awk)


if __name__ == "__main__":
    cli()
