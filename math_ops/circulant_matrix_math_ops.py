import numpy as np
from math_ops.pyGF2.generic_functions import strip_zeros, to_same_dim, padding
from math_ops import gf2_div

from parameters import LEDAkem_GLOBAL_PARAMS

def circmatprod_Z(a, b):

    """given two numpy arrays 'a' and 'b' which elements corresponds to the elements of the first rows
       of two circulant matrices 'A' and 'B' returns an array whose elements corresponds to the elements of the first row
       of the circulant matrix obtained as the product of the two circulant matrices A and B in the integer domain Z

    """
    a, b = to_same_dim(a, b)

    return np.rint(np.real(np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)))) #TODO use power of two also here?


def circmatprod_GF2x(a, b):
    """given two numpy arrays 'a' and 'b' which elements corresponds to the elements of the first rows
           of two circulant matrices 'A' and 'B' returns an array whose elements corresponds to the elements of the first row
           of the circulant matrix obtained as the product of the two circulant matrices A and B in GF2[x]

    """
    a, b = strip_zeros(a), strip_zeros(b)

    fsize = len(a) + len(b) + 1

    fsize = 2 ** np.ceil(np.log2(fsize)).astype(int)  # use nearest power of two much faster

    fslice = slice(0, fsize)

    ta = np.fft.fft(a, fsize)
    tb = np.fft.fft(b, fsize)

    res = np.fft.ifft(ta * tb)[fslice].copy()

    k = np.mod(np.rint(np.real(res)).astype("uint64"), 2)

    out = gf2_div(k , LEDAkem_GLOBAL_PARAMS.irr_poly)[1]

    # these operations are equal to do #np.mod(np.rint(np.real(np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)))),2).astype("uint8")
    # but much faster

    return strip_zeros(out)


def circtranspose(a):
    at = np.copy(a) #TODO copy ?
    at = padding(at, LEDAkem_GLOBAL_PARAMS.p)


    at[1:] = np.flip(at[1:], axis=0)

    return at


def gf2_add(a, b):
    a, b = to_same_dim(a, b)

    return np.logical_xor(a, b, dtype='uint8').astype('uint8')

def z_add(a, b):


    '''

    a, b = strip_zeros(a), strip_zeros(b)

    N = len(a)

    D = len(b)

    if N == D:
        res = np.add(a, b)

    elif N > D:

        res = np.concatenate((np.add(a[:D], b), a[D:]))

    else:

        res = np.concatenate((np.add(a, b[:N]), b[N:])
        '''

    return np.add(a,b)#strip_zeros(res)




def Z_div(dividend, divisor):

    N = len(dividend) - 1
    D = len(divisor) - 1

    if dividend[N] == 0 or divisor[D] == 0:
        dividend, divisor = strip_zeros(dividend), strip_zeros(divisor)

    if not divisor.any():  # if every element is zero
        raise ZeroDivisionError("polynomial division")
    elif D > N:
        q = np.array([])
        return q, dividend

    else:
        u = dividend
        v = divisor

        m = N
        n = D
        scale = 1. / v[n]
        q = np.zeros((max(m - n + 1, 1),), dtype="int64")
        r = u.astype("int64")

        for k in range(0, m - n + 1):
            d = (scale * r[m - k]).astype("int64")
            q[-1 - k] = d
            r[m - k - n:m - k + 1] -= (d * v).astype("int64")

        while np.allclose(r[0], 0, rtol=1e-14) and (r.shape[-1] > 1):
            r = r[1:]


        return q, r