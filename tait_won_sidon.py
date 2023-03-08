"""
All below is coded by Raf Walker
"""
import argparse
import itertools
from functools import lru_cache
from sympy import symbols, FF, Poly


def EuclidianDivisionF2(num, denom):
    assert denom != 0

    quotient = 0
    remainder = num

    bitrm = msb(remainder)
    bitdn = msb(denom)

    while remainder != 0 and bitrm >= bitdn:
        t = 1 << (bitrm - bitdn)
        quotient ^= t
        remainder ^= clm(t, denom)

        bitrm = msb(remainder)

    return (quotient, remainder)


def msb(x):
    """Linear search to find index of most significant bit"""
    i = 0
    while x >= (1 << i):
        i += 1
    return i - 1


def clm(a, b):
    """Carryless multiply.
    Could in theory use CMLUL."""
    c = b
    acc = 0
    i = 0
    while c >> i != 0:
        if (c >> i) & 1:
            acc ^= a << i
        i += 1
    return acc


def FindFieldPoly(n):
    # First, find an irreducible polynomial of degree n. We'll use sympy for this.
    f = FF(2)
    x = symbols('x')
    q = 0
    for exps in itertools.chain.from_iterable(itertools.combinations(range(1, n), r) for r in range(1, n, 2)):
        # Ask sympy if the polynomial corresponding to i is irreducible.
        if Poly(x ** n + 1 + sum(x ** i for i in exps), domain=f).is_irreducible:
            # This polynomial is irreducible.
            q = (1 << n) + 1 + sum(1 << i for i in exps)
            break
    assert q
    return q


def build_tait_won_sidon(dim):
    assert dim > 0
    assert dim % 2 == 0
    n = dim // 2
    q = FindFieldPoly(n)
    # Now, we will construct the sidon set.
    res = []
    for e in range(1 << n):
        e3r = clm(clm(e, e), e)
        (eq, e3) = EuclidianDivisionF2(e3r, q)
        res.append(e | (e3 << n))
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Tait and Won's cap of size 2^{d/2}.")
    parser.add_argument('-d', '--dim', type=int, required=True)
    args = parser.parse_args()

    dim = args.dim
    print(build_tait_won_sidon(dim))
