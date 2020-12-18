import pandas as pd
import math
import operator
import numpy as np


class KNN:
    def __init__(self):
        self.k = 1
        self.X = None
        self.Y = None
        self.columns = None

    def fit(self, X, Y):
        self.X = X
        self.Y = Y
        self.columns = X.columns

    def sample_distance(self, train_sample, test_sample):
        diff = test_sample - train_sample
        dist = np.power(diff, 2)
        return math.sqrt(dist)

    def distances(self, test):
        dist = []
        for i in range(len(self.X)):
            dist.append(self.sample_distance(self.X[i, :], test))
        return dist

    def predict(self, test, k):
        self.k = k
        predict = []
        for j in range(len(test)):
            t = test[j, :]
            dist = self.distances(t)
            labels = []
            for i in range(len(dist)):
                item = dist[i]
                labels.append([item, self.Y[i]])
            s = sorted(labels, key=lambda x: x[0])
            s = s[:self.k]
            classes = {}
            for i in range(self.k):
                vote = s[i][1]
                if classes.__contains__(vote):
                    classes[vote] += 1
                else:
                    classes.update({vote: 1})
            predict.append(max(classes.items(), key=operator.itemgetter(1))[0])
        return predict


