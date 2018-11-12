#!/usr/bin/env python3

import os
from util import load
from model import Model, Pair

DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "results"))

models = []

for filename in os.listdir(DIRECTORY):
    if filename[0] == ".":
        continue
    path = os.path.join(DIRECTORY, filename)
    model = load(path)
    models.append(model)

print()
for model in models:
    model.run()
    # print("ID\t", model.id)
    print("  \t++\t+-\t-+\t--")
    print("++\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(model.rules["++"].values()))
    print("+-\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(model.rules["+-"].values()))
    print("-+\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(model.rules["-+"].values()))
    print("--\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(model.rules["--"].values()))
    print("\t\t\t\t\t%d, %d, %d, %d (%2.2f)" % (*model.stats(), model.score))
    print()
