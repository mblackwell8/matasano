# from .xor import xor_byte, xor_bytes, xor_repeating
from typing import Union

def xor_byte(b1: int, b2: int) -> int:
    return b1 ^ b2

def xor_bytes(buf1: bytes, buf2: bytes) -> bytes:
    out = bytearray()
    for i in range(0, len(buf1)):
        out.append(xor_byte(buf1[i], buf2[i]))

    return bytes(out)

def xor_single(buf: bytes, mask: int) -> bytes:
    out = bytearray()
    for i in range(0, len(buf)):
        out.append(xor_byte(buf[i], mask))

    return bytes(out)

def xor_repeating(buf: bytes, mask: Union[int, bytes]) -> bytes:
    if isinstance(mask, int):
        return xor_single(buf, mask)

    out = bytearray()
    for i in range(0, len(buf)):
        out.append(xor_byte(buf[i], mask[i % len(mask)]))

    return bytes(out)


