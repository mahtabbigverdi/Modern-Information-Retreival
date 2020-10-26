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
    out = np.sqrt(sum([x*x for x in vector]))
    if out == 0 :
        return 1
    return out

def score_tfidf(index, query, total_number_of_docs):
    doc_vectors = [[0] for i in range(total_number_of_docs)]
    query_vector = []
    my_query = list(set(query))


    for term in my_query:

        w_tq = 1 + np.log10(query.count(term))
        query_vector.append(w_tq)

        for doc in index[term].keys():
            w_td = get_idf(index, term, total_number_of_docs) * get_logarithmic_tf(index, term, doc)
            doc_vectors[doc].append(w_td)


    lenghts = [get_normalized(vector) for vector in doc_vectors]
    doc_vectors = [list(np.array(doc_vectors[i])/lenghts[i]) for i in range(total_number_of_docs)]
    query_vector = np.array(query_vector) / get_normalized(query_vector)
    doc_vectors = np.array(doc_vectors)

    scores = doc_vectors * query_vector
    scores = np.sum (scores, axis=1)
    top_docs = np.argsort(scores)[-10: ]
    return top_docs


