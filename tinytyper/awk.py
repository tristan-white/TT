from dataclasses import dataclass
from pathlib import Path
import click


@dataclass
class Awk:
    input: click.utils.LazyFile
    output: click.utils.LazyFile
    chunk_size: int
    format: str
    remote_file: str

    first_line = True

    def getCmd(self, data: bytes) -> str:
        cmd = f'awk \'BEGIN{{printf "{"%c" * len(data)}",'
        cmd += ",".join([f"{d}" for d in data])
        cmd += "}'"

        if self.first_line:
            self.first_line = False
            return f"{cmd} > {self.remote_file}"
        return f"{cmd} >> {self.remote_file}"

    def run(self):
        chunk = self.input.read(self.chunk_size)
        while chunk:
            cmd = self.getCmd(chunk)
            if self.format == "tmux":
                cmd = '" \'"\' "'.join(cmd.split('"'))
                cmd = f'send-keys "{cmd}"\nsend-keys Enter'
            print(cmd, file=self.output)
            chunk = self.input.read(self.chunk_size)
