import pandas as pd
import nltk
# from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
lemma = nltk.WordNetLemmatizer()
stemmer = PorterStemmer()
import numpy as np
# nltk.download("wordnet")


def english_preprocess():
    ted_talks = pd.read_csv('data/ted_talks.csv')
    titles = list(ted_talks['title'])
    descriptions = list(ted_talks['description'])
    # casefold and lemmatize
    titles = [lemma.lemmatize(t.casefold()) for t in titles]
    descriptions = [lemma.lemmatize(d.casefold()) for d in descriptions]
    # find most common words = stopwords
    stopwords = {}
    for s in (titles + descriptions):
        token = nltk.word_tokenize(s)
        token = [word for word in token if word.isalpha()]
        for t in token:
            if t in stopwords.keys():
                stopwords[t] += 1
            else:
                stopwords[t] = 1
    stopwords = {k: v for k, v in sorted(stopwords.items(), key=lambda item: item[1], reverse=True)}
    most_common = []
    for k in stopwords.keys():
        if stopwords[k] > (0.03 * len(stopwords)):
            most_common += [k]
    # print(most_common)
    title_tokens = []
    description_tokens = []
    for i in range(len(titles)):
        # tokenize
        t_tokens = nltk.word_tokenize(titles[i])
        d_tokens = nltk.word_tokenize(descriptions[i])
        # remove punctuations
        t_tokens = [word for word in t_tokens if word.isalpha()]
        d_tokens = [word for word in d_tokens if word.isalpha()]
        # Remove stop_word
        t_tokens = [word for word in t_tokens if word not in most_common]
        d_tokens = [word for word in d_tokens if word not in most_common]
        # stem
        t_tokens = [stemmer.stem(word) for word in t_tokens]
        d_tokens = [stemmer.stem(word) for word in d_tokens]
        title_tokens += [t_tokens]
        description_tokens += [d_tokens]
    return title_tokens, description_tokens, most_common


def cache_preprocessed_docs(filename, tokens):
    np.saves(filename, np.array(tokens))


def load_preprocessed_docs(filename):
    return np.load(filename)

# if __name__ == '__main__':
#     title_tokens, description_tokens, most_common_word = english_preprocess()
