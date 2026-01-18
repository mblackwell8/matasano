from crypto import xor_bytes
from crypto import hex_decode, hex_encode

hex_str1 = "1c0111001f010100061a024b53535009181c"
hex_str2 = "686974207468652062756c6c277320657965"

hex1_bytes = hex_decode(hex_str1)
hex2_bytes = hex_decode(hex_str2)

result = xor_bytes(hex1_bytes, hex2_bytes)

result_str = hex_encode(result)
assert result_str == "746865206b696420646f6e277420706c6179"

print(result_str)