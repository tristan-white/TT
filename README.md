# TinyTyper
TinyTyper is a tool that utilizes creative techniques to write files to devices when other file transfer tools aren't an option.

## Why
It's not always easy to write a file to devices with limited environments, such as embedded devices. In such cases, traditional file transfer tools (samba, scp, nc, tftp, etc.) may not available.

TinyTyper aims to help by living off the land, leveraging [whatever is available](https://gtfobins.github.io/#+file%20write) to write files to the target device.

## Usage
TinyTyper outputs scripts that when run. By default, it outputs bash scripts to stdout, but the type of script and destination file can be configured.

To see the top level help menu, use the `--help` flag before the COMMAND. To see a COMMAND's help menu, place `--help` after the COMMAND. 

Example:
```
$ python3 tt.py --help
Usage: tt.py [OPTIONS] COMMAND [ARGS]...

  TinyTyper is a tool that utilizes various techniques to write  files to
  devices when other tools aren't an option.

Options:
  -i, --input FILE        Input file  [required]
  -o, --output FILENAME   Output file. If not provided, prints to stdout.
  -r, --remote-file FILE  The remote destination to which the file will be
                          written. Can be a base file name or path, but file
                          name must still be provided if path is given.
                          [required]
  --help                  Show this message and exit.

Commands:
  awk   Use awk on target to write files.
  echo  Use echo on target to write files.
$ python3 tt.py -i <input_file> -r <remote_file> echo --help
Usage: tt.py echo [OPTIONS]

Options:
  --chunk-size INTEGER      The number of bytes written with each echo command.  [default: 64]
  --no-n                    Use this flag when the '-n' option is not available on the target.
  -f, --format [bash|tmux]  Format of the output script.  [default: bash]
  --help                    Show this message and exit.
```