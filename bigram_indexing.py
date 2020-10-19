import pickle


def build_index(tokens):
    bigram_dict = {}
    for token in tokens:
        for t in token:
            t_new = '$' + t + '$'
            for i in range(len(t_new) - 1):
                new_key = t_new[i]+t_new[i+1]
                if new_key in bigram_dict.keys():
                    bigram_dict[new_key].add(t)
                else:
                    bigram_dict[new_key] = {t}
    return bigram_dict


def save(filename, index):
    with open(filename, 'wb') as handle:
        pickle.dump(index, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_pickle(filename):
    with open(filename, 'rb') as handle:
        index = pickle.load(handle)
    return index
