def printable(i: int) -> bool:
    """Returns True if chr(i) is a printable char and not a
    apostraphe, quotation mark, backtick, or back slash.
    """
    if i < 0x20 or i >= 0x7F:
        return False
    if i == 0x22 or i == 0x27 or i == 0x5C or i == 0x60:
        return False
    return True

def int_to_hex(i: int) -> str:
    if printable(i):
        return chr(i)
    else:
        return f"\\x{i:02x}"