import numpy as np
from math_ops import gf2_add
from math_ops import circmatprod_GF2x, circtranspose
from Qdecoder import Qdecoder
from HQ_generation import HQgen
from hashlib import sha3_256


def leda_dec(n0, p, m, dv, c, thresh_lut, i_max, pseed):

    H, Q = HQgen(n0, p, dv, m, pseed)

    Llast = np.zeros(p, dtype='uint8')

    for i in range(n0):
        Llast = gf2_add(Llast, circmatprod_GF2x(H[i], Q[i][n0 - 1]))

    s1 = circmatprod_GF2x(Llast, c)

    s2 = circtranspose(s1)  #TODO transpose Q e H instead in Qdecoder

    ok, e = Qdecoder(H, Q, n0, p, s2, thresh_lut, i_max)

    Ks = sha3_256(e).digest()

    return ok, Ks