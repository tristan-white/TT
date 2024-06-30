from dataclasses import dataclass
from pathlib import Path
import click

@dataclass
class Awk():
    input: str
    output: click.utils.LazyFile
    chunk_size: int
    format: str
    remote_file: str

    first_line = True

    def getCmd(self, data: bytes) -> str:
        cmd = "LC_ALL=C awk 'BEGIN {printf \""
        for _ in range(len(data)):
            cmd += "%c"
        cmd += "\","
        cmd += ",".join([f"{d}" for d in data])
        cmd += "}'"

        if self.first_line:
            self.first_line = False
            return f'{cmd} > {self.remote_file}'
        return f'{cmd} >> {self.remote_file}'

    def run(self):
        with open(self.input, "rb") as fd:
            chunk = fd.read(self.chunk_size)
            while chunk:
                cmd = self.getCmd(chunk)
                print(cmd, file=self.output)
                chunk = fd.read(self.chunk_size)