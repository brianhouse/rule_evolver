#!/usr/bin/env python3

import os, time, sys
import numpy as np
from util import load, save, log
from model import Model, RULES, STATES

from ggplot import * # https://stackoverflow.com/questions/50591982/importerror-cannot-import-name-timestamp
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from pandas import DataFrame


if len(sys.argv) < 2:
    exit("[path]")
path = sys.argv[1]

baseline, X = load(path)
np.append(X, baseline)
log.info(X.shape)

print(len(X), "models")

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

log.info(baseline)
log.info(classify(baseline))


types = list(map(classify, X))
types[-1] = "Homophily"

# categories = list(map(lambda x: int(x), list(set(types))))
# categories.sort()
# log.info(categories)

# if dimensions were greater than 50, should use PCA to reduce first
# results = TSNE(n_components=2).fit_transform(X)
results = PCA(n_components=2).fit_transform(X)
log.info(results.shape)


# clusters = DBSCAN(eps=2, min_samples=2).fit(results)
# log.info(clusters.labels_)
# types = clusters.labels_


results = {'x': results[:, 0], 'y': results[:, 1], 'Type': types}

chart = ggplot(DataFrame(results), aes(x='x', y='y', color='Type')) + geom_point(size=50, alpha=1) + ggtitle("Generated models")
chart.show()


