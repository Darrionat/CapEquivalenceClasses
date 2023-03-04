def rankOfMatrix(M, R, C):
    rank = C
    row = 0
    while row < rank:
        if row < R and M[row][row] != 0:
            for col in range(R):
                if col == row:
                    continue
                mult = M[col][row] / M[row][row]
                mult %= 2
                for i in range(rank):
                    M[col][i] -= mult * M[row][i]
                    M[col][i] %= 2
        else:
            reduce = True
            for i in range(row + 1, R):
                if M[i][row] == 0:
                    continue
                swap(M, row, i, rank)
                reduce = False
                break
            if reduce:
                rank -= 1
                for i in range(R):
                    M[i][row] = M[i][rank]
            row -= 1
        row += 1
    return rank


def swap(mat, row1, row2, col):
    for i in range(col):
        temp = mat[row1][i]
        mat[row1][i] = mat[row2][i]
        mat[row2][i] = temp
