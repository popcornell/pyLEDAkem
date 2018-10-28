import numpy as np
from rng import sha_prng


def HQgen(n0, p, dv, m, pseed):
    m = np.copy(m)  # avoid changing

    H = []
    for i in range(n0):
        temp = sha_prng(pseed, p, dv) # NB actual specification requires NIST secure AES based PRNG
        H.append(temp)
        pseed = pseed + b'1'

    Q = []

    for i in range(n0):

        Q_col = []

        for j in range(n0):
            Q_submat = sha_prng(pseed, p, m[j])
            Q_col.append(Q_submat)
            pseed = pseed + b'1'

        m = np.roll(m, 1)

        Q.append(Q_col)

    return np.array(H, dtype='uint8'), np.array(Q, dtype='uint8')
