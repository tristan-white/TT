# TinyTyper
TinyTyper is a tool that utilizes various techniques to write files to devices when other tools aren't an option.

## Why
It's not always easy to write a file to devices with limited environments, such as embedded devices. In such cases, traditional file transfer tools (samba, scp, nc, tftp, etc.) are not available.

TinyTyper aims to help by living off the land, leveraging whatever is available to write files to the target device.

## Usage

```
Usage: tt.py [OPTIONS] COMMAND [ARGS]...

  TinyTyper is a tool that utilizes various techniques to write  files to
  devices when other tools aren't an option.

Options:
  -i, --input PATH  Input file  [required]
  --help            Show this message and exit.

Commands:
  awk     Use awk on target to write files.
  echo    Write files to the target using echo.
  printf  Use printf on target to write files.
  vi      Use vi on target to write files.
```