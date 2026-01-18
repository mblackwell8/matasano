from crypto import hamming_distance, to_bytes, base64_decode, from_bytes, find_closest_fullkey, find_best_keysize, pretty_print, xor_repeating

print(hamming_distance(to_bytes('this is a test'), to_bytes('wokka wokka!!!')))


encrypted = ''
with open('sets/set1/6.txt', 'r') as file:
    encrypted = base64_decode(''.join(line.strip() for line in file))
    
best_keysizes = find_best_keysize(encrypted, test_block_count=4)

for keysize, hd_score in best_keysizes.items():
    fullkey = find_closest_fullkey(encrypted, keysize)
    
    print(f"For keysize {keysize} the best key is '{from_bytes(fullkey)}' (hd={hd_score})")

# print(pretty_print(xor_repeating(encrypted, b'Terminator X: Bring the noise')))
