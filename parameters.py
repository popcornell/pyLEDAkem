import numpy as np


class LEDAkem_GLOBAL_PARAMS():  # GLOBAL VARIABLE TO STORE IRRIDUCIBLE POLYNOMIAL X^p+1

    irr_poly = 0  # x^p + 1 irr polynomial
    n0 = 0
    p = 0
    t = 0
    m = 0
    dv = 0
    TRNG_byte_len = 0
    sha3_version = 0


class ledakem_session(object):

    def __init__(self, category, n0):

        self.category = category
        self.n0 = n0

        if category == 1:

            self.TRNG_byte_len = 24

            from hashlib import sha3_256

            self.sha3_version = sha3_256

            if self.n0 == 2:
                self.p = 15013
                self.dv = 9
                self.m = np.array([5, 4], dtype="uint8")
                self.t = 143


            if self.n0 == 3:
                self.p = 9643
                self.dv = 13
                self.m = np.array([3, 2, 2], dtype='uint8')
                self.t = 90

            if self.n0 == 4:
                self.p = 8467
                self.dv = 11
                self.m = np.array([3, 2, 2, 2], dtype='uint8')
                self.t = 72

            else:
                ValueError("Unsupported number of circulants blocks!")



        elif category == 2 or category == 3:

            self.TRNG_byte_len = 32

            from hashlib import sha3_384

            self.sha3_version = sha3_384

            if self.n0 == 2:
                self.p = 24533
                self.dv = 13
                self.m = [5, 4]
                self.t = 208

            elif self.n0 == 3:
                self.p = 17827
                self.dv = 15
                self.m = np.array([4, 3, 2], dtype='uint8')
                self.t = 129

            elif self.n0 == 4:
                self.p = 14717
                self.dv = 15
                self.m = np.array([3, 2, 2, 2], dtype='uint8')
                self.t = 104

            else:
                ValueError("Unsupported number of circulants blocks!")



        elif category == 4 or category == 5:

            self.TRNG_byte_len = 40

            from hashlib import sha3_512

            self.sha3_version = sha3_512

            if self.n0 == 2:
                self.p = 37619
                self.dv = 11
                self.m = [7, 6]
                self.t = 272

            elif self.n0 == 3:
                self.p = 28477
                self.dv = 13
                self.m = np.array([5, 4, 4], dtype='uint8')
                self.t = 172

            elif self.n0 == 4:
                self.p = 22853
                self.dv = 13
                self.m = np.array([4, 3, 3, 3], dtype='uint8')
                self.t = 135

            else:

                 ValueError("Unsupported number of circulants blocks!")
        else:
            ValueError("Unsupported Category!")









