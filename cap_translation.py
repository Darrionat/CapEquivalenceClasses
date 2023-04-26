from decompose_cap_pts import *
import numpy as np


def translate_cap(cap, p, dim):
    '''
    Translates the whole cap by (p,f(p)).
    :param cap: The cap to translate
    :param p: The representative
    :return:
    '''
    translation = stitch_pts(p, p, dim)
    return [translation ^ x for x in cap]


def scale_cap(cap, p, dim):
    translation = stitch_pts(p, p, dim)
    F = ffield.FField(dim)
    return [F.Multiply(translation, x) for x in cap]


if __name__ == '__main__':
    cap1 = [0, 33, 258, 483, 324, 997, 742, 135, 840, 809, 106, 203, 300, 973, 174, 655, 464, 593, 722, 403, 788, 533,
            694, 887, 88, 921, 378, 635, 444, 253, 574, 959]
    cap_1_sub = [0, 33, 90, 116, 131, 189, 219, 234, 267, 316, 335, 375, 409, 433, 479, 504, 517, 566, 597, 617, 642,
                 686, 720, 755, 776, 813, 838, 876, 926, 932, 978, 999]
    cap_1_sub_kasami = [0, 33, 94, 105, 147, 171, 213, 251, 273, 317, 332, 374, 415, 426, 474, 505, 520, 559, 596, 613,
                        668, 674, 728, 752, 781, 807, 850, 878, 900, 951, 963, 998]

    cap2 = [0, 65, 514, 963, 196, 1413, 3782, 2567, 1544, 1161, 3466, 3723, 1100, 973, 974, 1487, 336, 1553, 1426, 851,
            3732, 3285, 1622, 1431, 920, 1561, 3802, 2779, 3804, 3677, 3998, 3743, 2592, 3681, 354, 1187, 3492, 3301,
            2790, 2599, 1640, 233, 1194, 939, 876, 237, 3502, 4015, 3312, 4017, 370, 947, 1140, 565, 1526, 567, 1144,
            1529, 122, 123, 3708, 2813, 1662, 895]
    cap3 = [0, 129, 1026, 1923, 8196, 10885, 15366, 13703, 1544, 8841, 5002, 13323, 9356, 2573, 10510, 1167, 12304,
            15249, 4626, 6803, 7956, 7829, 9494, 10135, 8728, 3481, 4506, 15643, 3996, 10781, 9246, 671, 1312, 6561,
            6306, 1827, 4900, 1445, 5798, 807, 15016, 553, 13994, 3371, 11820, 7341, 14894, 2991, 5680, 433, 11698,
            14643, 3892, 4789, 11446, 12855, 15800, 3641, 6074, 10043, 9788, 8125, 5182, 11967, 10304, 14529, 3778,
            7491,
            1732, 7237, 14406, 8647, 6984, 12233, 11338, 7115, 14156, 2509, 6222, 9679, 4304, 2897, 4178, 2259, 12628,
            8405, 10710, 15191, 14296, 2137, 9946, 6747, 5340, 8541, 7646, 11103, 13152, 16353, 3170, 995, 11236, 11621,
            3302, 2407, 14824, 4457, 5994, 15595, 9196, 365, 5486, 13551, 10480, 12145, 12786, 13683, 16244, 13045,
            15990, 12535, 13944, 5625, 16122, 7803, 9084, 2813, 13310, 6527]
    cap4 = [0, 257, 2050, 3843, 16388, 21765, 30726, 27399, 35080, 49161, 8458, 28171, 52748, 37645, 22030, 3343, 56592,
            19217, 7186, 35859, 36628, 3349, 32278, 64023, 27672, 45593, 3354, 54555, 14620, 62237, 26654, 42015, 62496,
            16417, 53538, 25379, 57380, 16421, 62758, 21287, 60712, 4393, 26666, 37419, 65068, 5677, 19246, 42287,
            28208, 19761, 33330, 42803, 26676, 24373, 46134, 34103, 20280, 9273, 826, 28219, 20028, 12605, 12862, 19263,
            15168, 42817, 35138, 4931, 37956, 7237, 5702, 38983, 39752, 20297, 35146, 23371, 13132, 62285, 4430, 55119,
            62288, 63569, 34898, 34131, 20052, 20821, 1366, 7255, 27480, 10329, 45146, 62811, 53596, 34397, 14942,
            27487, 32352, 22369, 57698, 52835, 34148, 47205, 10854, 4455, 20072, 12137, 29034, 5739, 45676, 51053,
            48494, 52847, 61808, 20337, 42866, 8051, 6260, 45685, 32374, 53879, 63864, 3961, 3962, 65403, 6012, 62845,
            53630, 13695, 24448, 42113, 10882, 55171, 56708, 12933, 39046, 29063, 13704, 34441, 57482, 21899, 45196,
            6029, 21902, 62607, 19856, 8593, 61842, 39827, 56724, 42389, 20886, 12183, 8088, 15257, 922, 8603, 34972,
            47261, 42142, 37535, 928, 19873, 23458, 5027, 54692, 36773, 48550, 57767, 63912, 65449, 426, 427, 10412,
            15021, 57518, 62639, 22192, 36785, 51122, 6323, 37556, 24501, 13238, 63671, 38072, 1465, 42426, 12987,
            22460, 53949, 22206, 54719, 65216, 39105, 12738, 20931, 37828, 57797, 27846, 6343, 48584, 37833, 53962,
            64203, 55244, 60877, 35022, 46287, 63952, 2257, 65490, 2259, 34516, 25557, 45270, 21463, 33496, 15321, 9434,
            39899, 64220, 22493, 27870, 51167, 5088, 49377, 61922, 9443, 10980, 60901, 63718, 14823, 49384, 23529,
            33514, 8171, 65260, 29165, 36078, 1519, 21488, 6129, 30962, 15091, 30964, 10485, 25590, 13815, 47352, 46329,
            13306, 14843, 38140, 36093, 12286, 12799]

    # func = lambda x: kasami(x, ffield.FField(5), 10, find_nontrivial_k=True)
    # cap1 = build_points(10, func)
    # caps = [cap1, cap2, cap3, cap4]
    caps = [cap_1_sub_kasami]
    for cap in caps:
        print(cap)
        dim = dimension(cap)
        F = ffield.FField(int(dim / 2))
        total_points = []
        for p in range(0, 2 ** int(dim / 2)):
            f = lambda x: kasami(x, F, dim, find_nontrivial_k=True)
            translation = translate_cap(cap, p, dim)
            print('Shared with cap\t', len(np.intersect1d(cap, translation)))
            total_points.extend(translation)
            if not (is_cap(translation)):
                # Should be impossible. Always a cap by translation
                print('Is not a cap,', translation)
        count = 0
        not_count = 0
        for p in range(2 ** dim):
            if p not in total_points:
                not_count += 1
            else:
                count += 1

        print(count, not_count)