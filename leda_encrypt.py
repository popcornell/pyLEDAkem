import numpy as np
from math_ops import gf2_add
from math_ops import circmatprod_GF2x, circtranspose
from parameters import LEDAkem_GLOBAL_PARAMS
from rng import sha_prng, quasi_trng

from hashlib import sha3_256


def leda_enc(M):

    n0 = LEDAkem_GLOBAL_PARAMS.n0
    p = LEDAkem_GLOBAL_PARAMS.p
    t = LEDAkem_GLOBAL_PARAMS.t
    sha3 = LEDAkem_GLOBAL_PARAMS.sha3_version
    TRNG_byte_len = LEDAkem_GLOBAL_PARAMS.TRNG_byte_len

    seed = quasi_trng(TRNG_byte_len)

    e = sha_prng(seed, n0*p, t) # LEDAKem uses AES-256 generator here

    e = np.reshape(e, (n0,p))

    Ks = sha3(e).digest()  # LEDAKem SHA-3 uses

    tmp = np.zeros(p, dtype='uint8')

    for i in range(n0 - 1):
        tmp = gf2_add(tmp, circmatprod_GF2x(circtranspose(e[i,:]), M[i]))

    c = gf2_add(tmp, circtranspose(e[-1, :]))

    return Ks, c







