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


def jaccard_distance(wrong_dictation, word):
    bigram_wrong = count_bigrams(wrong_dictation)
    bigram_word = count_bigrams(word)
    intersection = len(list(set(bigram_wrong).intersection(bigram_word)))
    union = (len(bigram_wrong) + len(bigram_word)) - intersection
    return float(intersection) / union


def count_bigrams(word):
    bigrams = []
    for i in range(len(word) - 1):
        new_key = word[i] + word[i + 1]
        bigrams.append(new_key)
    return bigrams


# print(jaccard_distance('bord', 'boardroom'))

# print(edit_distance('snow', 'osio'))
