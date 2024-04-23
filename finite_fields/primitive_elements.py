from pyfinite import ffield
from vbf_functions.vbfs import field_exp


def find_primitive_element(field):
    for alpha in range(1, field.order):
        powers = set()
        for i in range(1, field.order):
            powers.add(field.Pow(alpha, i))
        if len(powers) == field.order - 1:  # Check if all non-zero elements are covered
            return alpha
    return None


def all_primitve_elements(field):
    primitve_elements = []
    n = field.n
    for alpha in range(1, 2 ** n):
        powers = set()
        for i in range(1, 2 ** n):
            powers.add(field_exp(alpha, i, field))
        if len(powers) == int(2 ** n) - 1:  # Check if all non-zero elements are covered
            primitve_elements.append(alpha)
    return primitve_elements


if __name__ == '__main__':
    for n in range(1, 20):
        F = ffield.FField(n)
        primitive_elements = all_primitve_elements(F)
        # print(primitive_elements)
        print(len(primitive_elements))
