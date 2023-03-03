import os.path
import numpy as np
import equivalence_classes


def get_folder_path(cap_size):
    return str(cap_size) + '_caps'


def path(cap_size, arank):
    return get_folder_path(cap_size) + os.sep + get_file_path(cap_size, arank, True)


def data_exists(cap_size, arank):
    return os.path.exists(path(cap_size, arank))


def load_data(cap_size, arank):
    return np.load(path(cap_size, arank), allow_pickle=True)


def get_file_path(cap_size, arank, add_file_ext=False):
    name = str(cap_size) + '_' + str(arank) + '_classes'
    return name + '.npy' if add_file_ext else name


def save_data(cap_size, arank, data):
    if data is None:
        raise ValueError('No data provided to save')
    # Data already exists or this is a max cap
    if data_exists(cap_size, arank) or data_exists(cap_size, arank + 1):
        raise ValueError('Data already exists')
    folder = get_folder_path(cap_size)
    try:
        os.mkdir(folder)
    except OSError:
        pass
    np.save(folder + os.sep + get_file_path(cap_size, arank), data)


def get_min_arank(cap_size):
    """
    Gets the lowest possible affine rank for a given cap size
    :param cap_size: The cap size
    :return:  Lowest affine rank of the cap in the saved data
    """
    for arank in range(5, cap_size + 1):
        if data_exists(cap_size, arank):
            return arank


def get_equiv_class_count(cap_size, arank):
    if not data_exists(cap_size, arank):
        return -1
    data = load_data(cap_size, arank)
    return len(data) if cap_size != arank else 1


def get_cap_num_classes(cap_size):
    arr = []
    minrank = get_min_arank(cap_size)
    if minrank is None:
        minrank = 5
    for arank in range(minrank, cap_size + 1):
        count = get_equiv_class_count(cap_size, arank)
        if count != -1:
            arr.append(count)
    print(str(cap_size) + '-Cap Equiv Class Count', arr)
