import os.path
import numpy as np
import requests
import time


def data_exists(cap_size, arank):
    return os.path.exists(get_folder_path(cap_size) + os.sep + get_file_path(cap_size, arank, True))


def load_data(cap_size, arank):
    return np.load(get_folder_path(cap_size) + os.sep + get_file_path(cap_size, arank, True), allow_pickle=True)


def get_file_path(cap_size, arank, add_file_ext=False):
    name = str(cap_size) + '_' + str(arank) + '_classes'
    return name + '.npy' if add_file_ext else name


def get_folder_path(cap_size):
    return str(cap_size) + '_caps'


# Gets the lowest possible affine rank for a given cap size
def get_min_arank(cap_size):
    for arank in range(5, cap_size + 1):
        if data_exists(cap_size, arank):
            return arank


def build_cap(M):
    r = len(M)
    k = r + len(M[0])  # r + k-r = k
    cap = [0]
    # Init the basis
    for i in range(1, k - r):
        cap.append(pow(2, i - 1))
    for row in M:
        pt = 0
        for i in range(0, len(row)):
            if row[i] == 1:
                pt ^= int(pow(2, i - 1))
        cap.append(pt)
    return cap


def analyze(cap_size, arank):
    if not data_exists(cap_size, arank):
        # print('No data exists for k=', cap_size, 'r=', arank)
        return
    complete_url = "http://127.0.0.1:8080/complete-qap/"
    cover_url = "http://127.0.0.1:8080/cover-number/"
    matrices = load_data(cap_size, arank)
    for M in matrices:
        cap = build_cap(M)
        params = {'points': cap, 'dim': arank - 1}
        complete_res = requests.get(url=complete_url, params=params)
        cover_res = requests.get(url=cover_url, params=params)
        # The responses
        cover_value = cover_res.json()['cover']
        complete = complete_res.json()['complete']

        if complete and cover_value != -1:
            print('cap=', cap, 'arank=', arank, 'cover_value=', cover_value)
        elif complete:
            print('cap=', cap, 'arank=', arank)
        time.sleep(1)


if __name__ == '__main__':
    cap_size_bound = 25
    curr_min_arank = 5
    for C in range(23, cap_size_bound):
        # tasks = []
        for R in range(curr_min_arank, C + 1):
            if R >= cap_size_bound + 1:
                break
            analyze(C, R)
        curr_min_arank = get_min_arank(C)

#
# def send_request():
#     # api-endpoint
#     complete_url = "http://127.0.0.1:8080/complete-qap/"
#     PARAMS = {
#         'points': [0, 129, 1026, 1923, 8196, 10885, 15366, 13703, 1544, 8841, 5002, 13323, 9356, 2573, 10510, 1167,
#                    12304, 15249, 4626, 6803, 7956, 7829, 9494, 10135, 8728, 3481, 4506, 15643,
#                    3996, 10781, 9246, 671, 1312, 6561, 6306, 1827, 4900, 1445, 5798, 807, 15016, 553, 13994, 3371,
#                    11820, 7341, 14894, 2991, 5680, 433, 11698, 14643, 3892, 4789, 11446, 12855, 15800, 3641, 6074,
#                    10043, 9788, 8125, 5182, 11967, 10304, 14529, 3778, 7491, 1732, 7237, 14406, 8647, 6984, 12233,
#                    11338, 7115, 14156, 2509, 6222, 9679, 4304, 2897, 4178, 2259, 12628, 8405, 10710, 15191, 14296, 2137,
#                    9946, 6747, 5340, 8541, 7646, 11103, 13152, 16353, 3170, 995, 11236, 11621, 3302, 2407, 14824, 4457,
#                    5994, 15595, 9196, 365, 5486, 13551, 10480, 12145, 12786, 13683, 16244, 13045, 15990, 12535, 13944,
#                    5625, 16122, 7803, 9084, 2813, 13310, 6527], 'dim': 14}
#     r = requests.get(url=complete_url, params=PARAMS)
#     print(r.json())
#     cover_url = "http://127.0.0.1:8080/cover-number/"
#     r = requests.get(url=cover_url, params=PARAMS)
#     print(r.json())
#     print(r.json()['cover'] == 21)
