import collections
import pickle

import numpy as np


def build_positional_index(docs):
    positional_index = {}

    for i in range(len(docs)):
        for word in docs[i]:
            if word in positional_index:
                if i in positional_index[word]:
                    continue
            else:
                positional_index[word] = {}

            l = np.array(docs[i])
            positions = list(np.where(l == word)[0])
            positional_index[word][i] = positions
    positional_index = dict(collections.OrderedDict(sorted(positional_index.items())))
    return positional_index


def save_index(obj):
    with open('pos_index' + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_index(PATH):
    with open(PATH, 'rb') as f:
        return pickle.load(f)


def add_doc(doc, number_new_doc, PATH):
    positional_index = load_index(PATH)
    for word in doc:
        if word in positional_index:
            if number_new_doc in positional_index[word]:
                continue
        else:
            positional_index[word] = {}

        l = np.array(doc)
        positions = list(np.where(l == word)[0])
        positional_index[word][number_new_doc] = positions

    positional_index = dict(collections.OrderedDict(sorted(positional_index.items())))
    save_index(positional_index)


def show_posting(word, PATH):
    positional_index = load_index(PATH)
    print(list(positional_index[word].keys()))


def show_positions(word, PATH):
    positional_index = load_index(PATH)
    for key, value in positional_index[word].items():
        print('doc number ' + str(key) + ' positions: ', value)


def del_doc(doc, number_of_doc, PATH):
    positional_index = load_index(PATH)
    words = list(set(doc))
    for word in words:
        del positional_index[word][number_of_doc]
        ### delete that word if it has no docs
        if not bool(positional_index[word]):
            del positional_index[word]
    positional_index = dict(collections.OrderedDict(sorted(positional_index.items())))
    save_index(positional_index)


def get_df (positional, term):
    return len (positional[term])

def get_tf (positional, term, doc):
    return len(positional[term][doc]) if doc in positional[term] else 0

def get_cf(positional, term):
    return sum([len(positions) for positions in positional[term].values()])

# docs =[
#     ['i','am','a', 'very', 'good' ,'girl' ,'really' ,'really' ,'good'],
#     ['good','girl','is', 'a', 'girl' ,'who' ,'studies' ,'well' ],
#     ['i','am','a', 'very', 'nice' ,'one'],
# ]
#
# save_index(build_positional_index(docs))
x = (load_index('pos_index' + '.pkl'))
print(x)
# print(get_tf(x, 'girl',0))
# add_doc(['i','am','a', 'very', 'nice' ,'person'], 3,'pos_index.pkl')
# show_positions('good', 'pos_index.pkl')
# del_doc(['i','am','a', 'very', 'good' ,'girl' ,'really' ,'really' ,'good'],0,'pos_index.pkl')
