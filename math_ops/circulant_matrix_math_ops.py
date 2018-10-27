import numpy as np
from math_ops.pyGF2.generic_functions import to_same_dim
from math_ops import gf2_div

def circmatprod_Z(a, b):

    """given two numpy arrays 'a' and 'b' which elements corresponds to the elements of the first rows
       of two circulant matrices 'A' and 'B' returns an array whose elements corresponds to the elements of the first row
       of the circulant matrix obtained as the product of the two circulant matrices A and B in the integer domain Z

    """

    a,b = to_same_dim(a, b)

    return np.rint(np.real(np.fft.ifft(np.fft.fft(a) * np.fft.fft(b))))


def circmatprod_GF2x(a, b):
    """given two numpy arrays 'a' and 'b' which elements corresponds to the elements of the first rows
           of two circulant matrices 'A' and 'B' returns an array whose elements corresponds to the elements of the first row
           of the circulant matrix obtained as the product of the two circulant matrices A and B in GF2[x]

    """



    return np.mod(np.rint(np.real(np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)))),2).astype("uint8")


def circtranspose(a):
    at = np.copy(a)

    at[1:] = np.flip(at[1:], axis=0)

    return at


def gf2_add(a, b):
    a, b = to_same_dim(a, b)

    return np.logical_xor(a, b, dtype='uint8').astype('uint8')