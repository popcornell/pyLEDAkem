import secrets
import random
import numpy as np

from hashlib import sha3_256, sha256


def quasi_trng(n_bits): # almost cryptographically secure

    return secrets.token_bytes(n_bits)


def prng(seed, size, weight): #NB not cryptographically secure

    random.seed(seed)

    arr = np.array([0] * (size - weight) + [1] * weight, dtype='uint8')

    #out = []
    #for i in range(n0):

    #    out.append(arr[p*i:p*(i+1)])

    return arr #out


def int_sha256(integer):

    bytes = integer.to_bytes(integer.bit_length(), 'little')

    bytes = sha256(bytes)

    out = int.from_bytes(bytes.digest(), 'little')

    return out





def sha_prng(seed, size, weight): # more secure


    digest = sha3_256(seed).digest()#int_sha256(seed)  # one-way seed must be trng

    num = int.from_bytes(digest, 'little')

    pos = num % size
    #print(pos)

    arr = np.zeros(size, dtype='uint8')

    while np.sum(arr) != weight: #TODO more efficient

        arr[pos] = not arr[pos]

        digest = sha3_256(seed+digest).digest()#int_sha256(digest)

        num = int.from_bytes(digest, 'little')

        pos = num % size

    return arr


