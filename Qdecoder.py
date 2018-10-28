from math_ops import gf2_add
from math_ops import circtranspose, circmatprod_Z, circmatprod_GF2x, z_add
import numpy as np
from math_ops.pyGF2.generic_functions import padding


def Qdecoder(H, Q, n0, p, s, look_up, i_max):
    i_iter = 1

    e = np.zeros(n0 * p, dtype='uint8')
    e = np.reshape(e, (n0, p))

    s_i = s

    while (i_iter < i_max) and (s_i.any()):  # syndrome not zeros

        if __debug__:
            print("Decoding....")
            print("Iteration n:", i_iter)
            print("Syndrome weight:", np.sum(s_i))

        counter = []
        for i in range(n0):
            counter.append(circmatprod_Z(s_i, (H[i])))


        corr = []
        for i in range(n0):
            corr.append(circmatprod_Z(counter[0], Q[0, i]))
            for j in range(1, n0):

                 corr[i] = z_add(corr[i], circmatprod_Z(counter[j], (Q[j, i])))

        ws = np.count_nonzero(s_i)

        pos =  np.where(look_up[:, 0] < ws)[0]

        b = look_up[pos[-1], 1]

        for i in range(n0):
            pos = np.where(corr[i] >= b)[0]
            e[i, pos] = np.logical_not(e[i, pos])


        ep = []
        for i in range(n0):

            temp = np.zeros(p, dtype='uint8')

            for j in range(n0):
                temp = gf2_add(temp, circmatprod_GF2x(e[j, :], circtranspose(Q[i, j])))

            ep.append(temp)

        delta_s = np.zeros(p, dtype='uint8')
        for i in range(n0):
            delta_s = gf2_add(delta_s, circmatprod_GF2x(ep[i], circtranspose(H[i])))

        s_i = gf2_add(s, delta_s)
        i_iter += 1

    if i_iter == i_max:
        flag = False
    else:
        flag = True

        for i in range(n0):
            e[i] = padding(e[i], p) #pad each block of e to have p length

    return flag, e
