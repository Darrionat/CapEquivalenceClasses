from decompose_cap_pts import *


def translate_cap(cap, p1, p2, dim):
    translation = concatenate_binary_strings(p1, p2, dim)
    return [translation ^ x for x in cap]


def special_translate_cap(cap, p, dim):
    """
    Translates the whole cap by (p,f(p)).
    :param cap: The cap to translate
    :param p: The representative
    :return:
    """
    return translate_cap(cap, p, p, dim)


def scale_cap(cap, p, dim):
    translation = concatenate_binary_strings(p, p, dim)
    F = ffield.FField(dim)
    return [F.Multiply(translation, x) for x in cap]


def special_translators_sim(n, apn_not_ab):
    # print('n\t', n)
    dim = n * 2
    field = ffield.FField(n)
    if apn_not_ab:
        if n % 2 == 1:
            f = lambda x: inverse(x, n, field)
        elif n % 5 == 0:
            f = lambda x: dobbertin(x, n, field)
        else:
            return
    else:
        f = lambda x: kasami(x, field, dim=n, find_nontrivial_k=True)

    print('Surjective\t', surjective_function(f, n, field))
    cap = build_points(dim, f)
    total_points = set()
    translations = []
    # two_fixed = 0
    # with open('total_points', 'w') as f:
    for t in range(0, 2 ** n):
        translation = translate_cap(cap, t, t, dim)
        translations.append(translation)
        # for p in translation:
        # print(p)
        total_points.update(translation)
        # fixed_points = len(set(translation) & set(cap))
        # if fixed_points == 2:
        #     two_fixed += 1

    count = len(total_points)
    not_count = 2 ** dim - count
    print('Translation Cover #\t', count, 'Translation Not-Cover #\t', not_count)

    point_dist = {}
    for translation in translations:
        #     print(sort(translation))
        for p in translation:
            point_dist[p] = 1 if p not in point_dist else point_dist[p] + 1
    overlap_dist = {}
    # print('Point Dist')
    for p in point_dist:
        #     print(f'{p}:{point_dist[p]}')
        overlap = point_dist[p]
        overlap_dist[overlap] = 1 if overlap not in overlap_dist else overlap_dist[overlap] + 1
    print('Overlap Dist')
    for overlap in overlap_dist:
        print(f'{overlap}:{overlap_dist[overlap]}')

    # print(point_dist)

    '''
    for translation in translations:
        unique_points = 0
        for p in translation:
            unique = True
            for translation_2 in translations:
                if translation == translation_2:
                    continue
                if p in translation_2:
                    unique = False
                    break
            if unique:
                unique_points += 1
        print(unique_points)
    '''

    # print('2-Fix\t', two_fixed)


if __name__ == '__main__':
    '''
    USAGE: python3 cap_translation.py [0 or 1 for strict_apn] [n] | sort -nu > total_points_sorted && wc -l total_points_sorted
    '''
    # n = int(sys.argv[-1])
    # strict_apn = int(sys.argv[-2])
    # for n in range(4, 16):
    #     print(n)
    #     print('gold')
    special_translators_sim(14, False)
    # print('Inverse/Dobbertin')
    # special_translators_sim(n, True)
