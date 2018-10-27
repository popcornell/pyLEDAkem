import numpy as np
from HQ_generation import HQgen
from math_ops import gf2_add, gf2_inv, circmatprod_GF2x


def keygen(n0, p, dv, m, pseed):
    # size of the seed ?

    irr_poly = np.array([1] + [0] * (p - 1) + [1], dtype='uint8')

    H, Q = HQgen(n0, p, dv, m, pseed)

    L = []

    for i in range(n0):

        temp = np.zeros(p, dtype='uint8')

        for j in range(n0):
            temp = gf2_add(temp, circmatprod_GF2x(H[j], Q[j, i]))

        L.append(temp)

    Linv = gf2_inv(L[-1], irr_poly)  # TODO  with full numba

    Linv = Linv[:p].astype('uint8')  # only last p values

    M = []

    for i in range(n0 - 1):
        M.append(circmatprod_GF2x(Linv, L[i]))

    if __debug__:

        from math_ops import gf2_div

        check_inverse = gf2_div(circmatprod_GF2x(Linv, L[-1]), irr_poly)[1]

        assert (np.sum(check_inverse) == 1)
        assert check_inverse[0] == 1

        #assert M[-1][0] == 1  # unitary
        #assert np.sum(M[-1][0]) == 1

        print("Inverse in GF(2)/(x^p+1) is correct")

    return H, Q, M
