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
    print("\t\t\t\t\t%d, %d, %d, %d (%2.2f)" % (*model.stats(), model.score))
    print()


print()
print("EVOLVED TRANSITION RULES")
print()
print("Target distribution\t\t\t133, 57, 24, 186 (0.00)")
print()
print()
print("Merton's table")

models = []

for filename in os.listdir(DIRECTORY):
    if filename[0] == ".":
        continue
    path = os.path.join(DIRECTORY, filename)
    model = load(path)
    models.append(model)

baseline = Model(RULES)
baseline.run()
output(baseline)

save("models.pkl", (baseline, models))

print()
print()
print("Alternative tables")
print()

diffs = []
for m, model in enumerate(models):
    model.run()
    output(model)

    diff = 0
#     for state_1 in STATES:
#         for state_2 in STATES:
#             diff += abs(model.rules[state_1][state_2] - baseline.rules[state_1][state_2])
#     diffs.append(diff)



# d = list(zip(diffs, models))
# d.sort(key=lambda p: p[0], reverse=True)

# d = d[:10]

# for m in d:
#     model = m[1]
#     output(model)


