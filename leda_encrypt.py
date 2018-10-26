import numpy as np
from gf_math_ops import gf2_add, gf2_mul, circtranspose
from rng import sha_prng, quasi_trng

from hashlib import sha3_256


def leda_enc(n0, p, t, M):

    seed = quasi_trng(256)

    e = sha_prng(seed, n0*p, t) # LEDAKem uses AES-256 generator here

    e = np.reshape(e, (n0,p))

    Ks = sha3_256(e).digest()  # LEDAKem SHA-3 uses

    tmp = np.zeros(p, dtype='uint8')

    for i in range(n0 - 1):
        tmp = gf2_add(tmp, gf2_mul(circtranspose(e[i,:]), M[i]))

    c = gf2_add(tmp, circtranspose(e[-1, :]))

    return Ks, c







