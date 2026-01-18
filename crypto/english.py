from string import ascii_uppercase
from operator import itemgetter
from .xor import xor_repeating
from .blocks import transpose

def sample_freq(sample: bytes) -> dict[int, float]:
    # just work with the raw bytes provided
    s_f = {}
    if len(sample) == 0:
        return s_f
    
    for s in sample:
        if s in s_f.keys():
            s_f[s] += 1.0
        else:
            s_f[s] = 1.0
    
    return {c: count / len(sample) for c, count in s_f.items()}

# def char_freq(chars: bytes) -> dict[str, float]:
#     counts = {c: 0.0 for c in ascii_uppercase}

#     if len(chars) == 0:
#         return counts

#     for c in chars:
#         uppercase_c = chr(c).upper()
#         if uppercase_c in counts.keys():
#             counts[uppercase_c] += 1
    
#     freq = {c: count / len(chars) * 100 for c, count in counts.items()}
#     return freq

# english_freq = {
#     'E' : 12.0,
#     'T' : 9.10,
#     'A' : 8.12,
#     'O' : 7.68,
#     'I' : 7.31,
#     'N' : 6.95,
#     'S' : 6.28,
#     'R' : 6.02,
#     'H' : 5.92,
#     'D' : 4.32,
#     'L' : 3.98,
#     'U' : 2.88,
#     'C' : 2.71,
#     'M' : 2.61,
#     'F' : 2.30,
#     'Y' : 2.11,
#     'W' : 2.09,
#     'G' : 2.03,
#     'P' : 1.82,
#     'B' : 1.49,
#     'V' : 1.11,
#     'K' : 0.69,
#     'X' : 0.17,
#     'Q' : 0.11,
#     'J' : 0.10,
#     'Z' : 0.07 
#     }

EN_FREQ = {
    ' ': 0.1828846265,
    'e': 0.1026665037,
    't': 0.0751699827,
    'a': 0.0653216702,
    'o': 0.0615957725,
    'n': 0.0571201113,
    'i': 0.0566844326,
    's': 0.0531700534,
    'r': 0.0498790855,
    'h': 0.0497856396,
    'l': 0.0331754796,
    'd': 0.0328292305,
    'u': 0.0227579536,
    'c': 0.0223367596,
    'm': 0.0202656783,
    'f': 0.0198306716,
    'w': 0.0170389377,
    'g': 0.0162490441,
    'p': 0.0150432428,
    'y': 0.0142766662,
    'b': 0.0125888074,
    'v': 0.0079611644,
    'k': 0.0056096272,
    'x': 0.0014092016,
    'j': 0.0009752181,
    'q': 0.0008367550,
    'z': 0.0005128469,
}

def english_freq_diff(sample_freq: dict[int, float], non_printable_penalty=5.0) -> float:
    sum = 0.0
    for c, e_f  in EN_FREQ.items():
        freq = 0.0
        if ord(c) in sample_freq.keys():
            freq = sample_freq[ord(c)]
        elif ord(c.upper()) in sample_freq.keys():
            freq = sample_freq[ord(c.upper())]

        sum += (e_f - freq) ** 2
    
    for k, v in sample_freq.items():
        if k not in (9, 10, 13) and k not in range(32, 127):
            sum += v * non_printable_penalty
    
    return sum

# def find_closest(decrypts:list[bytes]) -> tuple[bytes, float]:
#     best_score = -1.0
#     best_ix = 0
#     for i, decrypt in enumerate(decrypts):
#         freq = sample_freq(decrypt)
#         score = english_freq_diff(freq)
#         print(f"{decrypt} scored {score}")
#         if best_score == -1 or score < best_score:
#             best_score = score
#             best_ix = i

#     return decrypts[best_ix], best_score

def english_sort(decrypts:list[bytes]) -> list[tuple[bytes, float]]:

    scored_decrypts = list()

    for i, decrypt in enumerate(decrypts):
        freq = sample_freq(decrypt)
        score = english_freq_diff(freq)

        scored_decrypts.append((decrypt, score))

    sorted_decrypts = sorted(scored_decrypts, key=itemgetter(1))

    return sorted_decrypts

def find_closest_char(encrypted:bytes, key_range=range(0, 256)) -> int:
    closest_key = -1
    closest_score = 0.0
    for key in key_range:
        decrypt = xor_repeating(encrypted, key)
        score = english_freq_diff(sample_freq(decrypt))
        if closest_key == -1 or score < closest_score:
            closest_score = score
            closest_key = key

    return closest_key 

def find_closest_fullkey(encrypted: bytes, keysize: int) -> bytes:
    transposed_blocks = transpose(encrypted, keysize)
    fullkey = []
    for block in transposed_blocks:
        closest_key = find_closest_char(block, range(32, 127))
        fullkey.append(closest_key)
    
    return bytes(fullkey)
