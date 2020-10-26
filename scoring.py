from positional import *
import numpy as np
import math

def get_logarithmic_tf(index, term, doc):
    tf = get_tf(index, term, doc)
    if tf == 0:
        return 0
    return 1 + np.log10(tf)

def get_idf (index, term, total_number_docs):
    df = get_df(index, term)
    return np.log10(total_number_docs/df)

def get_normalized (vector):
    return np.sqrt(sum([x*x for x in vector]))


def lenght_doc(index, doc_id, total_number_of_docs):
    out = []
    for term in index.keys():
        if doc_id in index[term]:
            w_td = get_logarithmic_tf(index, term, doc_id) * get_idf(index, term, total_number_of_docs)
            out.append(w_td)
    return get_normalized(out)



def score_tfidf(index, query, total_number_of_docs):
    scores = [0 for i in range(total_number_of_docs)]
    query_vector = []

    my_query = list(set(query))


    for term in my_query:

        w_tq = 1 + np.log10(query.count(term))
        query_vector.append(w_tq)

        for doc in index[term].keys():
            w_td = get_idf(index, term, total_number_of_docs) * get_logarithmic_tf(index, term, doc)
            scores[doc]+=(w_td*w_tq)


    lengths = [lenght_doc(index, doc_id, total_number_of_docs) for doc_id in range(total_number_of_docs)]

    query_size = get_normalized(query_vector)

    scores = np.array(scores)
    lengths =np.array(lengths)

    scores /= lengths
    scores /= query_size

    top_docs = np.argsort(scores)[-10: ][::-1]
    return top_docs


index = (load_index('pos_index' + '.pkl'))
query =['i','am','good', 'girl']

print(score_tfidf(index, query, 3))