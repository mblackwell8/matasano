# from .bytes_utils import to_bytes, from_bytes
def to_bytes(content: str) -> bytes:
    return bytes([ord(c) for c in content])

def from_bytes(content: bytes) -> str:
    return ''.join(chr(c) for c in content)

def pretty_print(content: bytes) -> str:
    return ''.join(chr(c) if c in (9, 10, 13) or 32 <= c <= 126 else '*' for c in content)

def join_bytes(content: list[bytes]) -> bytes:
    return b''.join(content)