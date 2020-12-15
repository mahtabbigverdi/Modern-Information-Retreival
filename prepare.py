import pandas as pd
import nltk
from nltk.stem import SnowballStemmer
lemma = nltk.WordNetLemmatizer()
stemmer = SnowballStemmer('english')
import numpy as np
import collections

nltk.download('wordnet')
nltk.download('punkt')

main_path = ""
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
    # plt.bar(list(stopwords.keys())[:20], list(stopwords.values())[:20], color='g')
    most_common = []
    for k in stopwords.keys():
        if stopwords[k] > (0.06 * len(stopwords)):
            most_common += [k]
    return  most_common

def get_docs(path):
    ted_talks = pd.read_csv(path)
    titles = list(ted_talks['title'])
    descriptions = list(ted_talks['description'])
    views = list(ted_talks['views'])
    return titles, descriptions, views

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





most_common_english = find_most_common_words(main_path + 'train.csv')
titles_train, descriptions_train, train_y = get_docs(main_path + 'train.csv')
titles_test, descriptions_test, test_y = get_docs(main_path + 'test.csv')

title_tokens_train = parse_all_docs(titles_train, most_common_english)
description_tokens_train = parse_all_docs(descriptions_train, most_common_english)

train_X = [title_tokens_train[i] + description_tokens_train[i] for i in range(len(title_tokens_train))]


title_tokens_test = parse_all_docs(titles_test, most_common_english)
description_tokens_test = parse_all_docs(descriptions_test, most_common_english)

test_X = [title_tokens_test[i] + description_tokens_test[i] for i in range(len(title_tokens_test))]

print(np.array(train_X).shape)

print(np.array(train_y).shape)

print(np.array(test_X).shape)

print(np.array(test_X).shape)

from sklearn.model_selection import train_test_split
train_X, val_X, train_y, val_y = train_test_split(
    train_X, train_y, test_size=0.1)

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

index = build_positional_index(train_X)

N = len(train_X)

def get_df (positional, term):
    return len (positional[term])


def get_idf (index, term, N):
    df = get_df(index, term)
    return np.log10(N/df)

def build_data(X, index):
    new = [[] for i in range(len(X))]
    for word in index.keys():
        for i in range(len(X)):
            tf = len(list(np.where(np.array(X[i]) == word)[0]))
            new[i].append(tf * get_idf(index, word, N))
    return new





train_X = np.array(build_data(train_X, index))
test_X = np.array(build_data(test_X, index))
val_X = np.array(build_data(val_X, index))



