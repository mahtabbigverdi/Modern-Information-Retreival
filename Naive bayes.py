import numpy as np
import pandas
from preprocess import *


class NaiveBayes:

    def __init__(self):
        self.prob_c = 0
        self.prob_c_not = 0
        self.count_per_word_c = dict()
        self.count_per_word_c_not = dict()
        self.all_c = 0
        self.all_c_not = 0

    def train(self, X, y):
        self.prob_c = y.count(1) / len(y)
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
        print("c:", self.count_per_word_c)
        print("c_not:", self.count_per_word_c_not)

    def predict(self, X):
        p = [np.math.log(self.prob_c), np.math.log(self.prob_c_not)]
        for x in X:
            if x in self.count_per_word_c.keys():
                p[0] += np.math.log((self.count_per_word_c[x] + 1) / self.all_c)
            else:
                p[0] += np.math.log(1 / self.all_c)
            if x in self.count_per_word_c_not.keys():
                p[1] += np.math.log((self.count_per_word_c_not[x] + 1) / self.all_c_not)
            else:
                p[1] += np.math.log(1 / self.all_c_not)
        print(p)
        return 1 if np.argmax(p) == 0 else -1


train = pandas.read_csv('data/train.csv')
y_train = train['views'].values
x_train = train[['title', 'description']].values

# x = NaiveBayes()
# x.train([['c', 'b', 'c'], ['c', 'c', 's'], ['c', 'm'], ['t', 'j', 'c']], [1, 1, 1, -1])
# pred = x.predict(['c', 'c', 'c', 't', 'j'])
# print(pred)

