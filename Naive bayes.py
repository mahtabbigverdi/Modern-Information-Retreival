import numpy as np
import pandas
from preprocess import *
import math


class NaiveBayes:

    def __init__(self):
        self.prob_c = 0
        self.prob_c_not = 0
        self.count_per_word_c = dict()
        self.count_per_word_c_not = dict()
        self.all_c = 0
        self.all_c_not = 0

    def train(self, X, y):
        self.prob_c = np.count_nonzero(y == 1) / len(y)
        self.prob_c_not = 1 - self.prob_c
        for i in range(len(X)):
            for token in X[i]:
                if y[i] == 1:
                    if token in self.count_per_word_c.keys():
                        self.count_per_word_c[token] += 1
                    else:
                        self.count_per_word_c[token] = 1
                else:
                    if token in self.count_per_word_c_not.keys():
                        self.count_per_word_c_not[token] += 1
                    else:
                        self.count_per_word_c_not[token] = 1
        diff_words = len(set(list(self.count_per_word_c.keys()) + list(self.count_per_word_c_not.keys())))
        self.all_c = sum(self.count_per_word_c.values()) + diff_words
        self.all_c_not = sum(self.count_per_word_c_not.values()) + diff_words
        print(diff_words)
        print(self.all_c, self.all_c_not)

    def predict(self, X):
        p = [math.log(self.prob_c), math.log(self.prob_c_not)]
        label = []
        i = 0
        for x in X:
            for x_i in x:
                if x_i in self.count_per_word_c.keys():
                    p[0] += math.log((self.count_per_word_c[x_i] + 1) / self.all_c)
                else:
                    p[0] += math.log(1. / self.all_c)
                if x_i in self.count_per_word_c_not.keys():
                    p[1] += math.log((self.count_per_word_c_not[x_i] + 1) / self.all_c_not)
                else:
                    p[1] += math.log(1. / self.all_c_not)
            label.append(1 if np.argmax(p) == 0 else -1)
        return label


train = pandas.read_csv('data/train.csv')
y_train = train['views'].values
x_train = train[['title', 'description']].values

test = pandas.read_csv('data/test.csv')
y_test = test['views'].values
x_test = test[['title', 'description']].values

x_train_token = []
_, _, mc = find_most_common_words('data/train.csv')
for x in x_train:
    tmp = []
    for x_i in x:
        tmp += doc_preprocess(x_i, mc)
    x_train_token.append(tmp)

x_test_token = []
for x in x_test:
    tmp = []
    for x_i in x:
        tmp += doc_preprocess(x_i, mc)
    x_test_token.append(tmp)

NB = NaiveBayes()
NB.train(x_train_token, y_train)
y_pred = NB.predict(x_test_token)
print(np.sum(y_pred == y_test), "correct predictions out of", len(y_pred))
print(np.sum(y_pred == y_test) * 100 / len(y_pred), "% accuracy")

