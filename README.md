# TinyTyper
TinyTyper is a tool that utilizes creative techniques to write files to devices when other file transfer tools aren't an option.

## Why
It's not always easy to write a file to devices with limited environments, such as embedded devices. In such cases, traditional file transfer tools (samba, scp, nc, tftp, etc.) may not available.

TinyTyper aims to help by living off the land, leveraging [whatever is available](https://gtfobins.github.io/#+file%20write) to write files to the target device.

## Usage

```
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
```