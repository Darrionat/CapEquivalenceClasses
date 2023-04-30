# import pickle
#
# if __name__ == '__main__':
#     # objects = []
#     total_len = 0
#     with (open("totalPoints", "rb")) as openfile:
#         while True:
#             try:
#                 l = len(pickle.load(openfile))
#                 total_len += l
#                 print(l)
#                 # objects.append(pickle.load(openfile))
#             except EOFError:
#                 break
#     print('total:', total_len)
#     # while len(objects) != 0:
#     #     total_points.update(objects.pop())
from collections import Counter

input_file = r'totalPoints'


# Main logic
# If hash is different then the contents are different
# If hash is same then the contents may be different


def count_with_index(values):
    '''
    Returns dict like key: (count, [indexes])
    '''
    result = {}
    for i, v in enumerate(values):
        count, indexes = result.get(v, (0, []))
        result[v] = (count + 1, indexes + [i])
    return result


def get_lines(fp, line_numbers):
    return (v for i, v in enumerate(fp) if i in line_numbers)


# Gets hashes of all lines
counter = count_with_index(map(hash, open(input_file, "rb")))

# Sums only the unique hashes
sum_of_unique_hash = sum((c for _, (c, _) in counter.items() if c == 1))

# Filters all non unique hashes
non_unique_hash = ((h, v) for h, (c, v) in counter.items() if c != 1)

total_sum = sum_of_unique_hash

# For all non unique hashes get the actual line and count
# One hash is picked per time. So memory is not consumed much.
for h, v in non_unique_hash:
    counter = Counter(get_lines(open(input_file, "rb"), v))
    total_sum += sum(1 for k, v in counter.items())

print('Total number of unique lines is : ', total_sum)

