#!/usr/bin/env python3

import os, time
from util import load, save
from model import Model, Pair, RULES, STATES

DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "results"))

def output(model):
    # print("ID\t", model.id)
    print("  \t++\t+-\t-+\t--")
    print("++\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(model.rules["++"].values()))
    print("+-\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(model.rules["+-"].values()))
    print("-+\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(model.rules["-+"].values()))
    print("--\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(model.rules["--"].values()))
    print("\t\t\t\t\t%2.2f, %2.2f, %2.2f, %2.2f (%.4f)" % (*model.distribution(), model.score))
    print()


print()
print("EVOLVED TRANSITION RULES")
print()
print("Target distribution\t\t\t%2.2f, %2.2f, %2.2f, %2.2f (0.00)" % tuple([x/400 for x in (133, 57, 24, 186)]))
print()
print()
print("Merton's table")

baseline = Model(RULES)
baseline.run()
output(baseline)

print()
print()
print("Alternative tables")
print()

models = []
for filename in os.listdir(DIRECTORY):
    if filename[-4:] != ".pkl":
        continue
    path = os.path.join(DIRECTORY, filename)
    model = load(path)
    model.run()
    if model.score <= 0.004:
        output(model)
        models.append(model)

save("models.pkl", (baseline, models))
