from .xor import xor_bytes
from operator import itemgetter

def chunkify(buf: bytes, sz: int) -> list[bytes]:
    chunks = []
    for i in range(0, len(buf), sz):
        chunks.append(buf[i: i + sz])

    return chunks

def transpose(buf: bytes, keysize: int) -> list[bytes]:
    transposed = [bytearray() for i in range(0, keysize)]
    for i in range(0, len(buf)):
        transposed[i % keysize].append(buf[i])

    return [bytes(bv) for bv in transposed]

def hamming_distance(str1: bytes, str2: bytes) -> int:
    # number of differing bits...
    # which is effectively the xor, i think?
    xor = xor_bytes(str1, str2)
    true_bit_n = 0
    for b in xor:
        for shift in range(0, 8):
            if (b >> shift) & 1:
                true_bit_n += 1

    return true_bit_n

# def find_best_keysize(encrypted: bytes, test_range=range(2, 41), test_block_count=2) -> dict[int, float]:
#     hds = dict()
#     for keysize in test_range:
#         if keysize * test_block_count > len(encrypted):
#             break
#         test_blocks = chunkify(encrypted, keysize)[0: test_block_count]

#         total_hd = sum([hamming_distance(test_blocks[i], test_blocks[i+1]) for i in range(0, test_block_count-1)])
#         avg_hd = float(total_hd) / (test_block_count-1)

#         hds[keysize] = avg_hd / keysize

#     return dict(sorted(hds.items(), key=itemgetter(1)))

def find_best_keysize(encrypted: bytes, test_range=range(2, 41), test_block_count=2) -> dict[int, float]:
    hds = {}

    for keysize in test_range:
        # remove any trailing blocks of less than keysize
        blocks = [b for b in chunkify(encrypted, keysize) if len(b) == keysize]
        if len(blocks) < test_block_count:
            continue

        test_blocks = blocks[:test_block_count]

        total = 0.0
        pairs = 0
        for i in range(test_block_count - 1):
            for j in range(i+1, test_block_count):
                total += hamming_distance(test_blocks[i], test_blocks[j])
                pairs += 1

        avg_hd = total / pairs
        hds[keysize] = avg_hd / keysize   # normalized

    return dict(sorted(hds.items(), key=itemgetter(1)))


