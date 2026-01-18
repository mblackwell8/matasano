import string
from crypto import hex_decode, xor_repeating, english_sort, from_bytes


encrypted_str = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
encrypted_bytes = hex_decode(encrypted_str)
decrypts = [xor_repeating(encrypted_bytes, ord(c)) for c in string.ascii_uppercase]

# best_guess, score = find_closest(decrypts)
sorted_decrypts = english_sort(decrypts)
best = sorted_decrypts[0]

print(f"{from_bytes(best[0])} scored {best[1]}")

# print(f"The key is most likely {best_key} ({min_score}).")
# print(''.join(decrypts[best_key][0]))

