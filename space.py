#!/usr/bin/env python3

import os, time
import numpy as np
from util import load, save
from model import Model, Pair, RULES, STATES

from ggplot import * # https://stackoverflow.com/questions/50591982/importerror-cannot-import-name-timestamp
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from pandas import DataFrame


# # load models
# path = os.path.abspath(os.path.join(os.path.dirname(__file__), "models.pkl"))
# baseline, models = load(path)


# def linearize(model):
#     point = []
#     for state_1 in STATES:
#         for state_2 in STATES:
#             point.append(model.rules[state_1][state_2])
#     return point

# baseline = linearize(baseline)
# points = np.array(list(map(linearize, models)))


# save("points.pkl", (baseline, points))

baseline, X = load("points.pkl")
np.append(X, baseline)
print(X.shape)

def classify(x):
    x = list(x)
    return "Others"
    return "%d" % x.index(max(x))
    # if x[0] >= .5:
    #     return "++"
    # if x[3] >= .5:
    #     return "--"
    # else:
    #     return "?"

print(baseline)
print(classify(baseline))


types = list(map(classify, X))
types[-1] = "Homophily"

# categories = list(map(lambda x: int(x), list(set(types))))
# categories.sort()
# print(categories)

# if dimensions were greater than 50, should use PCA to reduce first
# results = TSNE(n_components=2).fit_transform(X)
results = PCA(n_components=2).fit_transform(X)
print(results.shape)


# clusters = DBSCAN(eps=2, min_samples=2).fit(results)
# print(clusters.labels_)
# types = clusters.labels_


results = {'x': results[:, 0], 'y': results[:, 1], 'type': types}

chart = ggplot(DataFrame(results), aes(x='x', y='y', color='type')) + geom_point(size=50, alpha=1) + ggtitle("Generated models")
chart.show()


