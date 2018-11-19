#!/usr/bin/env python3

import os, time
import numpy as np
from util import load, save
from model import Model, RULES, STATES, MAGIC

DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "results"))

print()
print("EVOLVED TRANSITION RULES")
print()
print("Target distribution\t\t\t%d, %d, %d, %d (0.00)" % MAGIC)
print()
print()
print("Merton's table")

baseline = Model(RULES)
baseline.run()
baseline.show()

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
    model.show()
    models.append(model)
    os.remove(path)

save(os.path.join(DIRECTORY, "%s_models.pkl" % int(time.time())), (baseline, models))

def linearize(model):
    point = []
    for state_1 in STATES:
        for state_2 in STATES:
            point.append(model.rules[state_1][state_2])
    return point

baseline = linearize(baseline)
points = np.array(list(map(linearize, models)))

save(os.path.join(DIRECTORY, "%s_points.pkl" % int(time.time())), (baseline, points))

print("COLLATED %d MODELS" % len(models))

