def edit_distance(t1, t2):
    table = [[0 for _ in range(len(t1) + 1)] for _ in range(len(t2) + 1)]
    for i in range(len(t1)+1):
        table[0][i] = i
    for i in range(len(t2)+1):
        table[i][0] = i
    for i in range(1, len(t2)+1):
        for j in range(1, len(t1)+1):
            top_left = table[i - 1][j - 1]
            top_left += 1 if t2[i-1] != t1[j-1] else 0
            table[i][j] = min(table[i-1][j] + 1, table[i][j-1] + 1, top_left)
    print(table)
    return table[-1][-1]


print(edit_distance('snow', 'osio'))