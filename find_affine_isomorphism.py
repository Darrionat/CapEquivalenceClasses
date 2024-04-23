from cap import *


def affinely_equiv(cap1, cap2, debug=True):
    if debug:
        assert is_cap(cap1)
        assert is_cap(cap2)
    arank = calc_arank(cap1)
    if calc_arank(cap2) != arank:
        return False
    basis = find_basis(cap1)
    cap1_as_affine_combinations = []  # Find the relations w.r.t basis
    for comb in combinations(cap2, arank):
        # Go through all possible bases for second cap
        potential_basis_2 = [p for p in comb]
        

if __name__ == '__main__':
    pass
