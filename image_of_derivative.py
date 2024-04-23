import numpy as np

from decompose_cap_pts import *

from pyfinite import ffield
from generate_functions import print_gamma_matrix


def derivative_image(f, a, n):
    image = set()
    for x in range(2 ** n):
        image.add(f(x) ^ f(x ^ a))
    return image


if __name__ == '__main__':
    for n in range(3, 4, 2):
        print(f'----------{n}-----------')
        dim = 2 * n
        field = ffield.FField(n)
        f = lambda x: gold(x, field)
        for a in range(1, 2 ** n):
            print(f'{a}', derivative_image(f, a, n))
