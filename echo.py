from dataclasses import dataclass
from pathlib import Path
import click

@dataclass
class Echo:
    input: str
    output: click.utils.LazyFile
    chunk_size: int
    format: str
    remote_file: str
    no_n: bool

    first_line = True

    def __post_init__(self):
        pass

    def printable(self, i: int) -> bool:
        """Returns True if chr(i) is a printable char and not a
        apostraphe, quotation mark, backtick, or back slash.
        """
        if i < 0x20 or i >= 0x7F:
            return False
        if i == 0x22 or i == 0x27 or i == 0x5C or i == 0x60:
            return False
        return True

    def int_to_echo_hex(self, i: int) -> str:
        if self.printable(i):
            return chr(i)
        else:
            return f"\\x{i:02x}"

    def get_echo_ne_cmd(self, data: bytes) -> str:
        cmd = 'echo -n -e "'
        for d in data:
            cmd += self.int_to_echo_hex(d)
        if self.first_line:
            self.first_line = False
            return f'{cmd}" > {self.remote_file}'
        return f'{cmd}" >> {self.remote_file}'
    
    def get_env_var_cmd(self, data: bytes) -> str:
        cmd = "tt=${tt}$'"
        if self.first_line:
            self.first_line = False
            cmd = "tt=$'"
        for d in data:
            cmd += self.int_to_echo_hex(d)
        return cmd + "'"

    def get_tmux_cmd(self, cmd: str) -> str:
        return f"send-keys '{cmd}'\nsend-keys Enter"

    def run(self):
        with open(self.input, "rb") as fd:
            chunk = fd.read(self.chunk_size)
            while chunk:
                if self.no_n:
                    cmd = self.get_env_var_cmd(chunk)
                else:
                    cmd = self.get_echo_ne_cmd(chunk)
                if self.format == "tmux":
                    cmd = self.get_tmux_cmd(cmd)
                print(cmd, file=self.output)
                chunk = fd.read(self.chunk_size)
            if self.no_n:
                cmd = f"echo $tt > {self.remote_file}"
                if self.format == "tmux":
                    cmd = self.get_tmux_cmd(cmd)
                print(cmd, file=self.output)

