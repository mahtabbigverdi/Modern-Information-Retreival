from positional import *
import numpy as np
import math
import itertools

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

    return scores

def has_all_terms(index, my_query, doc_id):
    for term in my_query:
        if doc_id not in index[term]:
            return False
    return True

def find_total_distance_between_words(indexes):
    out = 0
    for i in range(len(indexes)-1):
        out += (indexes[i+1] - indexes[i])
    return out

def proximity_search(index, total_number_of_docs, query, window):
    my_query = list(set(query))
    relevants = []
    for doc_id in range(total_number_of_docs):
        if not has_all_terms(index,my_query, doc_id):
            continue
        positions = []
        for term in my_query :
            positions.append(index[term][doc_id])
        product = itertools.product(*positions)
        product = [sorted(list(item)) for item in product]
        windows = [find_total_distance_between_words(seq) for seq in product ]
        smallest_window = np.min(windows)
        if smallest_window <= window :
            relevants.append(doc_id)
    return relevants



def proximity_tfidf(index, total_number_of_docs, query, window):
    proximity_relevants = proximity_search(index, total_number_of_docs, query, window)
    scores = score_tfidf(index, query, total_number_of_docs)

    scores_of_relevants = map(scores.__getitem__, proximity_relevants)

    ordered_relevants= [id for _, id in sorted(zip(scores_of_relevants, proximity_relevants))]

    return ordered_relevants







# index = (load_index('pos_index' + '.pkl'))
# query =['good', 'a']
# print(proximity_tfidf(index,3,query,2))

# top_scores = score_tfidf(index, query, 3)[-10,:][::-1]



