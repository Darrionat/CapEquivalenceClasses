def get_triples(rank):
    to_return = []
    # 5 <= m <= n < r where m,n odd
    for n in range(5, rank, 2):
        for m in range(5, n + 1, 2):
            # i is the overlap
            for i in range(1, (m + 1) // 2 + 1):
                if m + n - rank <= i:
                    to_return.append((m, n, i))
    return to_return


if __name__ == '__main__':
    for cap_size in range(5, 51):
        rank = cap_size - 2
        triple_str = ''
        for triple in get_triples(rank):
            triple_str = triple_str + '\t' + str(triple)
        print(str(cap_size) + '\t' + triple_str)
