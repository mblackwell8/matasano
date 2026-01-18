import string
from crypto import hex_decode, xor_repeating, english_sort, from_bytes, pretty_print

with open('sets/set1/4.txt', 'r') as file:
    best_line_decrypt = bytes
    best_score = 0.0
    for line in file:
        line = line.strip('\n')
        # print(f"{line} is {len(line)} chars long")
        encrypted_bytes = hex_decode(line)
        decrypts = [xor_repeating(encrypted_bytes, c) for c in range(0, 256)]
        sorted_decrypts = english_sort(decrypts)

        best_decrypt = sorted_decrypts[0]
        if best_score == 0.0 or best_decrypt[1] < best_score:
            best_line_decrypt = best_decrypt[0]
            best_score = best_decrypt[1]

    print(pretty_print(best_line_decrypt))
