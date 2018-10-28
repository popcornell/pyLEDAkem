import secrets
import numpy as np

from hashlib import sha3_256, sha256


def quasi_trng(n_bits): # almost cryptographically secure

    return secrets.token_bytes(n_bits)

#TODO Python wrapper for NIST AES PRNG


def sha_prng(seed, size, weight): # more secure but not cryptographically secure


    digest = sha3_256(seed).digest() # seed must be trng

    num = int.from_bytes(digest, 'little')

    pos = num % size

    arr = np.zeros(size, dtype='uint8')

    while np.sum(arr) != weight: #not most efficient

        arr[pos] = not arr[pos]

        digest = sha3_256(seed+digest).digest()

        num = int.from_bytes(digest, 'little')

        pos = num % size

    return arr


