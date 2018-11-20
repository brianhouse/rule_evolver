#!/usr/bin/env python3

import os, time, sys
import numpy as np
from util import load, save, log
from collections import OrderedDict
from model import Model, RULES, STATES

if len(sys.argv) < 3:
    exit("[path] [n]")
path = sys.argv[1]
n = int(sys.argv[2])

baseline, models = load(path)

# model = models[n]
# model.show()

def get_max(model, state):
    max_value = 0
    max_key = None
    for key, value in model.rules[state].items():
        if value > max_value:
            max_value = value
            max_key = key
    return max_key


print(len(models))

# # baseline
# for model in models[:]:
#     if get_max(model, '++') != get_max(baseline, '++'):
#         models.remove(model)
#     elif get_max(model, '+-') != get_max(baseline, '+-'):
#         models.remove(model)
#     elif get_max(model, '-+') != get_max(baseline, '-+'):
#         models.remove(model)
#     elif get_max(model, '--') != get_max(baseline, '--'):
#         models.remove(model)


# # inverse
# for model in models[:]:
#     if get_max(model, '++') == get_max(baseline, '++'):
#         models.remove(model)
#     elif get_max(model, '+-') == get_max(baseline, '+-'):
#         models.remove(model)
#     elif get_max(model, '-+') == get_max(baseline, '-+'):
#         models.remove(model)
#     elif get_max(model, '--') == get_max(baseline, '--'):
#         models.remove(model)


# proposed:
for model in models[:]:

    if get_max(model, '++') not in ('+-', '-+'):
        models.remove(model)

    elif get_max(model, '+-') not in ('++', '+-'):
        models.remove(model)

    elif get_max(model, '-+') not in ('-+', '--'):
        models.remove(model)

    # elif get_max(model, '--') not in ('++', '+-'):
    #     models.remove(model)

print(len(models))


baseline.show()
print('//////')
for model in models:
    model.show()
