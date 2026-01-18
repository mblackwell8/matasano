def hex_encode(data: bytes) -> str:
    # every byte becomes two hex characters
    hex = "0123456789abcdef"
    chars = []
    for d in data:
        big_end = int(d / 16)
        chars.append(hex[big_end])
        small_end = int(d % 16)
        chars.append(hex[small_end])
    
    return ''.join(chars)

def hex_decode(data: str) -> bytes:
    hex = "0123456789abcdef"
    hex_lookup = {hex_ch: i for i, hex_ch in enumerate(hex)}
    buf = bytearray()
    big_end = -1
    for d in data:
        if big_end == -1:
            big_end = hex_lookup[d]
        else:
            small_end = hex_lookup[d]
            buf.append(big_end * 16 + small_end)
            big_end = -1
    
    return bytes(buf)


def base64_encode(data: bytes) -> str:
    base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    encoded = []

    # start with 3 bytes = 24 bits of raw data.
    for i in range(0, len(data), 3):
        block = data[i:i+3]

        pad_len = 3 - len(block)
        block = block + b'\x00' * pad_len

        # build the 24 bit value
        val = 0
        for b in block:
            val = (val << 8) | b
        
        # extract the 4 six bit values
        for shift in (18, 12, 6, 0):
            encoded.append(base64[(val >> shift) & 0x3F])

        # pad with =
        if pad_len > 0:
            encoded[-pad_len:] = '=' * pad_len

    return ''.join(encoded)

# print(base64_encode(b"M"))
# print(base64_encode(b"Ma"))
# print(base64_encode(b"Man"))
def base64_decode(data: str) -> bytes:
    base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    b64_lookup = {b64_char: i for i, b64_char in enumerate(base64)}
    decoded = bytearray()

    # each character represents 6 bits, so 4 characters is a round 24 bits = 3 bytes
    for i in range(0, len(data), 4):
        block = data[i:i+4]

        # build the 24 bit value, ignoring any padding
        val = 0
        pads = 0
        for b in block:
            decoded_char_ix = 0
            if b == '=':
                pads += 1
            else:
            # find the index of the b64 character
                decoded_char_ix = b64_lookup[b]
            val = (val << 6) | decoded_char_ix

        # print(val)
        # extract the 3 eight bit groups
        for shift in (16, 8, 0):
            decoded.append((val >> shift) & 0xFF)

        if pads > 0:
            decoded = decoded[:-pads]

    return bytes(decoded)

def run_tests():
    hex_tests = [
            (b"", ""),
            (b"\x00", "00"),
            (b"\x0f", "0f"),
            (b"\xff", "ff"),
            (b"\x00\xff", "00ff"),
            (b"abc", "616263"),
            (b"\x10\x20\x30", "102030"),
            (b"\xde\xad\xbe\xef", "deadbeef"),
            (b"\x01\x02\x03\x04\x05", "0102030405"),
        ]

    # encode
    for raw, expected in hex_tests:
        out = hex_encode(raw)
        assert out == expected, f"encode {raw!r}: expected {expected!r}, got {out!r}"

    # decode
    for expected, text in hex_tests:
        out = hex_decode(text)
        assert out == expected, f"decode {text!r}: expected {expected!r}, got {out!r}"

    print("hex encode/decode tests passed")

    b64_encode_tests = [
            (b"", ""),
            (b"M", "TQ=="),
            (b"Ma", "TWE="),
            (b"Man", "TWFu"),
            (b"\x00", "AA=="),
            (b"\x00\xff", "AP8="),
            (b"\x00\xff\x10", "AP8Q"),
            (b"abcd", "YWJjZA=="),
            (b"python", "cHl0aG9u"),
            (b"\xff\xff\xff", "////"),
        ]

    for raw, expected in b64_encode_tests:
        out = base64_encode(raw)
        assert out == expected, f"{raw!r}: expected {expected!r}, got {out!r}"

    print("base64 encoding tests passed")


    b64_decode_tests = [
        ("", b""),                       # empty
        ("TQ==", b"M"),                  # 1 leftover byte
        ("TWE=", b"Ma"),                 # 2 leftover bytes
        ("TWFu", b"Man"),                # full 3 bytes
        ("AA==", b"\x00"),               # single zero byte
        ("AP8=", b"\x00\xff"),           # binary + padding
        ("AP8Q", b"\x00\xff\x10"),       # binary, no padding
        ("YWJjZA==", b"abcd"),           # multi-block
        ("cHl0aG9u", b"python"),         # longer
        ("////", b"\xff\xff\xff"),       # max 6-bit values
    ]

    for b64, expected in b64_decode_tests:
        out = base64_decode(b64)
        assert out == expected, f"{b64}: expected {expected}, got {out}"
    print("base64 decoding tests passed")
    

        
