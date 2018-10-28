import numpy as np
from HQ_generation import HQgen
from parameters import LEDAkem_GLOBAL_PARAMS
from math_ops import gf2_add, gf2_inv, circmatprod_GF2x


def keygen(pseed):

    irr_poly = LEDAkem_GLOBAL_PARAMS.irr_poly
    n0 = LEDAkem_GLOBAL_PARAMS.n0
    p = LEDAkem_GLOBAL_PARAMS.p
    dv = LEDAkem_GLOBAL_PARAMS.dv
    m = LEDAkem_GLOBAL_PARAMS.m


    H, Q = HQgen(n0, p, dv, m, pseed)

    L = []

    for i in range(n0):

        temp = np.zeros(p, dtype='uint8')

        for j in range(n0):
            temp = gf2_add(temp, circmatprod_GF2x(H[j], Q[j, i]))

        L.append(temp)

    Linv = gf2_inv(L[-1], irr_poly)

    M = []

    for i in range(n0 - 1):
        M.append(circmatprod_GF2x(Linv, L[i]))

    if __debug__:
        from math_ops import gf2_div

        check_inverse = gf2_div(circmatprod_GF2x(Linv, L[-1]), irr_poly)[1]

        assert (np.sum(check_inverse) == 1)
        assert check_inverse[0] == 1

        print("Inverse in GF(2)/(x^p+1) is correct")

    return H, Q, M
