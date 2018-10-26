import unittest
import numpy as np
import time

from leda_encrypt import leda_enc
from leda_decrypt import leda_dec
from rng import quasi_trng
from threshold_lut import choose_threshold_lut

from M_generation import keygen
from gf_math_ops import gf2_add, gf2_mul, circtranspose


class ledakem_session(object):

    def __init__(self, category, n0):

        self.category= category
        self.n0 = n0

        if category == 1:

            if self.n0 == 2:
                self.p = 27779
                self.dv = 17
                self.m = [4, 3]
                self.t = 224

            if self.n0 == 3:
                self.p = 18701
                self.dv = 19
                self.m = np.array([3, 2, 2], dtype='uint8')
                self.t = 141

            if self.n0 == 4:
                self.p = 17027
                self.dv = 21
                self.m = np.array([4, 1, 1, 1], dtype='uint8')
                self.t = 112-50

        elif category == 2 or category == 3:

            if self.n0 == 2:
                self.p = 27779
                self.dv = 17
                self.m = [4, 3]
                self.t = 224

            if self.n0 == 3:
                self.p = 18701
                self.dv = 19
                self.m = np.array([3, 2, 2], dtype='uint8')
                self.t = 141

            if self.n0 == 4:
                self.p = 17027
                self.dv = 21
                self.m = np.array([4, 1, 1, 1], dtype='uint8')
                self.t = 112

        elif category == 4 or category ==5:

            if self.n0 == 2:
                self.p = 27779
                self.dv = 17
                self.m = [4, 3]
                self.t = 224

            if self.n0 == 3:
                self.p = 18701
                self.dv = 19
                self.m = np.array([3, 2, 2], dtype='uint8')
                self.t = 141

            if self.n0 == 4:
                self.p = 17027
                self.dv = 21
                self.m = np.array([4, 1, 1, 1], dtype='uint8')
                self.t = 112



class Testledakem(unittest.TestCase):


    def test_LEDAKem(self):

        self.category = [1, 2, 3, 4, 5]
        self.n0 = [2, 3, 4]

        self.test_parameters = []

        for i in self.category:

            for j in self.n0:
                self.test_parameters.append(ledakem_session(1, 4))

        n_test = 0

        for session in self.test_parameters:

            i_max = 20

            p = session.p
            n0 = session.n0
            t = session.t
            m = session.m
            dv = session.dv

            n_test+=1
            print("\nLEDAKem Testing n:", n_test)
            print("Parameters:\nCATEGORY:{}\nn0:{}\np:{}\nt:{}".format(session.category, n0, p, t))

            '''
            n0 = 4
            m = np.array([2, 2, 2, 1], dtype='uint8')
            p = 11083
            dv = 13
            t = 24
            i_max = 100

            #pseed = 1
            '''

            pseed = quasi_trng(256)

            print("Beginning Key Generation")
            t0 = time.time()

            H, Q, M = keygen(n0,p,dv,m,pseed)

            print("Private and Public Keys have been generared in: {:3f} s".format(time.time()-t0))

            print("Beginning Encryption")

            t0 = time.time()
            Ks_Alice, c_Alice= leda_enc(n0, p, t, M)

            print("Time taken for Encryption: {:3f} s".format(time.time() - t0))

            thresh_lut = choose_threshold_lut(session.category, n0) #np.array(((0, 48), (1105, 49)), dtype='int64')#

            print("Beginning Decryption")
            t0 = time.time()
            flag, Ks_Bob = leda_dec(n0,p,m,dv,c_Alice,thresh_lut,i_max,pseed)

            print("Time taken for Decryption: {:3f} s".format(time.time() - t0))

            self.assertEqual(flag, True)
            assert Ks_Alice==Ks_Bob

            print("Decoding succeded!!\n\n")








