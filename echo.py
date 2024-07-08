from dataclasses import dataclass
from pathlib import Path
from utils import int_to_hex
import click


@dataclass
class Echo:
    input: click.utils.LazyFile
    output: click.utils.LazyFile
    chunk_size: int
    format: str
    remote_file: str
    head_c: bool

    first_line = True

    def __post_init__(self):
        pass



    def get_cmd_echo_ne(self, data: bytes) -> str:
        cmd = 'echo -n -e "'
        for d in data:
            cmd += int_to_hex(d)
        if self.first_line:
            self.first_line = False
            return f'{cmd}" > {self.remote_file}'
        return f'{cmd}" >> {self.remote_file}'

    def get_cmd_env_var(self, data: bytes) -> str:
        cmd = "tt=${tt}$'"
        if self.first_line:
            self.first_line = False
            cmd = "tt=$'"
        for d in data:
            cmd += int_to_hex(d)
        return cmd + "'"

    def add_redirect(self, cmd: str) -> str:
        if self.first_line:
            return f"{cmd} > {self.remote_file}"
        else:
            return f"{cmd} >> {self.remote_file}"

    def get_cmd_ansic(self, data: bytes) -> str:
        """
        See here for info about ANSI-C Quoting:
        https://www.gnu.org/software/bash/manual/html_node/ANSI_002dC-Quoting.html
        """
        assert b"\x00" not in data, "ANSI-C Quotes cannot be null"
        cmd = ""
        for d in data:
            cmd += int_to_hex(d)
        cmd = f"echo $'{cmd}'"
        return cmd
    
    def get_cmd_null(self, num_bytes: int) -> str:
        cmd = f"head -c {num_bytes} /dev/zero"
        return cmd

    def get_tmux_cmd(self, cmd: str) -> str:
        return f"send-keys '{cmd}'\nsend-keys Enter"

    def run(self):
        chunk = self.input.read(self.chunk_size)
        while chunk:
            cmd = self.get_cmd_echo_ne(chunk)
            if self.format == "tmux":
                cmd = self.get_tmux_cmd(cmd)
            print(cmd, file=self.output)
            chunk = self.input.read(self.chunk_size)
