from math import gcd
from vbf_functions.apn_functions import *


def construct_SSF_set(apn_pow_vbf, j):
    """
    Constructs the Sidon sum-free set {x \in \F_{2^n} - {0} : x^{d-2^j} = 1}
    :param apn_pow_vbf: A power APN function
    :param j: A positive integer in {0, ..., n-1}
    :return The SSF set corresponding to the given power function and given integer
    """
    d = apn_pow_vbf.get_exponent()
    n = apn_pow_vbf.n
    field = apn_pow_vbf.field
    ej = gcd(d - int(2 ** j), int(2 ** n) - 1)
    to_return = set()
    for x in range(1, 2 ** n):
        if field_exp(x, ej, field) == 1:
            to_return.add(x)
    return to_return


if __name__ == '__main__':
    for n in range(5, 16, 5):
        print(f'-------------n={n}-------------')
        field = ffield.FField(n)
        func = dobbertin(field)
        print(f'd={func.exponent}')
        for j in range(n):
            print(j)
            print(construct_SSF_set(func, j))
