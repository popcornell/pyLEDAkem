# pyLEDAkem

**Numpy Python implementation of [LEDAkem](https://www.ledacrypt.org/LEDAkem/)
 key encapsulation module, a post-quantum asymmetric cryptoscheme relying
 on Quasi-Cyclic Low Density Parity Check (QC-LDPC) codes.**


---

**Official C reference implementation is available also on Github
[here](https://github.com/LEDAcrypt/LEDAkem)**

---

This Python implementation was developed directly from the specification
and not ported from the official C code.

Thus it lacks the high level of optimization of the official C code. In particular
because many operations performed in the LEDAkem algorithm involve multiplication and
addition of sparse arrays, currently this library lacks effective handling of such sparse arrays
and those operations instead are performed on the full arrays.

Nonetheless, as Python was used, speed was never the main ambition
in the development of this implementation for which the official library i believe is unbeatable.

Instead the focus here is to develop a more accessible and readable,
high level implementation of LEDAkem.


---

**NOTE**: Currently this implementation lacks the Pseudo-random number generator
      used in the actual specification: (NIST approved AES-256 CTR PRNG)

---

#### DISCLAIMER:

This Python implementation it is by no means official as it was developed
by me in my free time.

---

##### Special thanks to:
- Dr. Paolo Santini
- Prof. Marco Baldi
