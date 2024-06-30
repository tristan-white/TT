from dataclasses import dataclass
from pathlib import Path
import click

@dataclass
class Echo:
    input: str
    output: click.utils.LazyFile
    chunk_size: int
    no_n: bool
    format: str
    remote_file: str

    first_line = True

    def __post_init__(self):
        pass

    def printable(self, i: int) -> bool:
        if i < 0x20 or i >= 0x7F:
            return False
        if i == 0x22 or i == 0x27 or i == 0x5C or i == 0x60:
            return False
        return True

    def intToStr(self, i: int) -> str:
        if self.printable(i):
            return chr(i)
        else:
            return f"\\x{i:02x}"

    def getCmd(self, data: bytes) -> str:
        cmd = 'echo -n -e "'
        for d in data:
            cmd += self.intToStr(d)
        if self.first_line:
            self.first_line = False
            return f'{cmd}" > {self.remote_file}'
        return f'{cmd}" >> {self.remote_file}'

    def getTmuxCmd(self, cmd: str) -> str:
        return f"send-keys '{cmd}'\nsend-keys Enter"

    def run(self):
        with open(self.input, "rb") as fd:
            chunk = fd.read(self.chunk_size)
            while chunk:
                cmd = self.getCmd(chunk)
                if self.format == "tmux":
                    cmd = self.getTmuxCmd(cmd)
                print(cmd, file=self.output)
                chunk = fd.read(self.chunk_size)
