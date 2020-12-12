import pandas as pd
import nltk
from nltk.stem import SnowballStemmer
lemma = nltk.WordNetLemmatizer()
stemmer = SnowballStemmer('english')
import numpy as np
# nltk.download("wordnet")


def english_preprocess(doc):
    # casefold and lemmatize
    doc = lemma.lemmatize(doc.casefold())
    # tokenize
    tokens = nltk.word_tokenize(doc)
    # remove punctuations
    tokens = [word for word in tokens if word.isalpha()]
    # stem
    tokens = [stemmer.stem(word) for word in tokens]
    return tokens


def cache_preprocessed_docs(filename, tokens):
    np.saves(filename, np.array(tokens))


def load_preprocessed_docs(filename):
    return np.load(filename)


def remove_stop_words(doc, stopwords):
    return [word for word in doc if word not in stopwords]


def find_most_common_words(path):
    ted_talks = pd.read_csv(path)
    titles = list(ted_talks['title'])
    descriptions = list(ted_talks['description'])
    preprocessed_titles = []
    preprocessed_descriptions = []
    for i in range(len(titles)):
        preprocessed_titles += [english_preprocess(titles[i])]
        preprocessed_descriptions += [english_preprocess(descriptions[i])]
    stopwords = {}
    for s in (preprocessed_titles + preprocessed_descriptions):
        for t in s:
            if t in stopwords.keys():
                stopwords[t] += 1
            else:
                stopwords[t] = 1
    stopwords = {k: v for k, v in sorted(stopwords.items(), key=lambda item: item[1], reverse=True)}
    most_common = []
    for k in stopwords.keys():
        if stopwords[k] > (0.03 * len(stopwords)):
            most_common += [k]
    return titles, descriptions, most_common


def parse_all_docs(set, most_common):
    all_tokens = []
    for s in set:
        tokens = doc_preprocess(s, most_common)
        all_tokens += [tokens]
    return all_tokens


def doc_preprocess(doc, most_common):
    tokens = english_preprocess(doc)
    tokens = remove_stop_words(tokens, most_common)
    return tokens
