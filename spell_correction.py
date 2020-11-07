from bigram_indexing import read
import math

from preprocess import english_preprocess


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
    # print(table)
    return table[-1][-1]


def jaccard_distance(wrong_dictation, word):
    bigram_wrong = find_bigrams(wrong_dictation)
    bigram_word = find_bigrams(word)
    intersection = len(list(set(bigram_wrong).intersection(bigram_word)))
    union = (len(bigram_wrong) + len(bigram_word)) - intersection
    return float(intersection) / union


def find_bigrams(word):
    bigrams = []
    for i in range(len(word) - 1):
        new_key = word[i] + word[i + 1]
        bigrams.append(new_key)
    return bigrams


def spell_correction(word):
    bigrams = read("description_bigram")
    bigrams.update(read("title_bigram"))
    word_bigrams = find_bigrams(word)
    min_dist = math.inf
    possible_correct_words = []
    distances = set()
    for b in word_bigrams:
        # print(b)
        # print(bigrams[b])
        for w in bigrams[b]:
            if jaccard_distance(word, w) >= 0.3:
                dist = edit_distance(word, w)
                if dist <= min_dist:
                    min_dist = dist
                    distances.add((w, dist))
    for w, d in distances:
        if d == min_dist:
            possible_correct_words.append(w)
    return possible_correct_words


def correct_query(q):
    words = english_preprocess(q)
    for w in words:
        print(w)
        print(spell_correction(w))


# print(jaccard_distance('bord', 'boardroom'))
# print(edit_distance('snow', 'osio'))
# spell_correction("scholo")
# print(find_bigrams("school"), find_bigrams("scholo"))
correct_query("gok to scholo")
