from dataclasses import dataclass
from pathlib import Path
import click
from tinytyper.utils import int_to_hex

@dataclass
class Printf:
    input: click.utils.LazyFile
    output: click.utils.LazyFile
    chunk_size: int
    format: str
    remote_file: str

    first_line = True

    def get_printf_cmd(self, data: bytes) -> str:
        cmd = "".join([int_to_hex(d) for d in range(len(data))])
        return "printf '" + cmd + "'"

    def run(self):
        chunk = self.input.read(self.chunk_size)
        while chunk:
            cmd = self.get_printf_cmd(chunk)
            print(cmd, file=self.output)
            chunk = self.input.read(self.chunk_size)
        