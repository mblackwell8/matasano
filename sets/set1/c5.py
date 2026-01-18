from crypto import xor_repeating, hex_encode, to_bytes

stanza = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

key = to_bytes('ICE')

def encrypt(content: str):
    bytes = to_bytes(content)

    encrypted = xor_repeating(bytes, key)
    print(hex_encode(encrypted))

encrypt(stanza)


