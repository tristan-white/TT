from dataclasses import dataclass
from pathlib import Path

@dataclass
class Echo():
    in_file: str
    chunk_size: int
    no_n: bool

    def printable(self, i: int) -> bool:
        if i < 0x20 or i >= 0x7f:
            return False
        if i == 0x22 or i == 0x27 or i == 0x5c or i == 0x60:
            return False
        return True

    def intToStr(self, i: int) -> str:
        if self.printable(i):
            return chr(i)
        else:
            return f"\\x{i:02x}"

    def getCmd(self, data: bytes) -> str:
        cmd = 'echo -ne "'
        for d in data:
            cmd += self.intToStr(d)
        return cmd + '"'

    def run(self):
        with open(self.in_file, "rb") as fd:
            chunk = fd.read(self.chunk_size)
            while chunk:
                print(self.getCmd(chunk))
                chunk = fd.read(self.chunk_size)
            