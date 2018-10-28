import unittest
import time
import numpy as np
from parameters import ledakem_session, LEDAkem_GLOBAL_PARAMS

from leda_encrypt import leda_enc
from leda_decrypt import leda_dec
from rng import quasi_trng
from threshold_lut import choose_threshold_lut
from keygen import keygen





class test_ledakem(unittest.TestCase):

    def test_LEDAKem(self):

        self.category = [1, 2, 3, 4, 5]
        self.n0 = [2, 3, 4]

        self.test_parameters = []

        for i in self.category:

            for j in self.n0:
                self.test_parameters.append(ledakem_session(i, j))

        n_test = 0

        for session in self.test_parameters:
            i_max = 20

            p = session.p
            n0 = session.n0
            t = session.t
            m = session.m
            dv = session.dv
            TRNG_byte_len = session.TRNG_byte_len



            n_test += 1
            print("\nLEDAKem Testing n:", n_test)
            print("Parameters:\nCATEGORY:{}\nn0:{}\np:{}\nt:{}".format(session.category, n0, p, t))

            pseed = quasi_trng(TRNG_byte_len)

            LEDAkem_GLOBAL_PARAMS.irr_poly = np.array([1] + (p - 1) * [0] + [1], dtype="uint8")
            LEDAkem_GLOBAL_PARAMS.p = p

            print("Beginning Key Generation")
            t0 = time.time()

            H, Q, M = keygen(n0, p, dv, m, pseed)

            print("Private and Public Keys have been generared in: {:3f} s".format(time.time() - t0))

            print("Beginning Encryption")

            t0 = time.time()
            Ks_Alice, c_Alice = leda_enc(n0, p, t, M)

            print("Time taken for Encryption: {:3f} s".format(time.time() - t0))

            thresh_lut = choose_threshold_lut(session.category, n0)  # np.array(((0, 48), (1105, 49)), dtype='int64')#

            print("Beginning Decryption")
            t0 = time.time()
            flag, Ks_Bob = leda_dec(n0, p, m, dv, c_Alice, thresh_lut, i_max, pseed)

            print("Time taken for Decryption: {:3f} s".format(time.time() - t0))

            self.assertEqual(flag, True)
            assert Ks_Alice == Ks_Bob

            print("Decoding succeded!!\n\n")


if __name__ == "__main__":
    unittest.main()
