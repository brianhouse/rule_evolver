#!/usr/bin/env python3

import random, json, math, copy
import numpy as np
from util import config, log

log.info("START")


PAIRS = 400

RULES = {   '++': {'++': .5, '+-': .2, '-+': .1, '--': .2},    # Merton pages 40 and 55
            '+-': {'++': .3, '+-': .2, '-+': .0, '--': .5},
            '-+': {'++': .5, '+-': .0, '-+': .4, '--': .1},
            '--': {'++': .2, '+-': .1, '-+': .0, '--': .7}
            }
STATES = list(RULES.keys())


class Pair:

    def __init__(self):
        self.state = None
        self.changed = False


class Model:

    def __init__(self, rules):
        self.rules = copy.copy(rules)

    def mutate(self):
        key = random.choice(tuple(self.rules.keys()))
        self.rules[key] = dict(zip(['++', '+-', '-+', '--'], list(np.random.dirichlet(np.ones(4),size=1)[0])))

    def stats(self):
        stats = {'++': 0, '+-': 0, '-+': 0, '--': 0}
        for pair in self.pairs:
            stats[pair.state] += 1
        return tuple(stats.values())

    def reset(self):
        self.pairs = [Pair() for p in range(PAIRS)]
        n = int(len(self.pairs) / len(STATES))
        chunks = [self.pairs[i:i + n] for i in range(0, len(self.pairs), n)]
        if len(chunks) > len(STATES):
            chunks[-2] = chunks[-2] + chunks[-1]
            del chunks[-1]
        for c, chunk in enumerate(chunks):
            for pair in chunk:
                pair.state = STATES[c]

    def run(self):
        self.reset()
        T = 0
        previous = (0, 0, 0, 0)
        previous_difference = float('Inf')
        log.info("--------------------------------------------------")        
        log.info(self.stats())
        while True:
            current = self.stats()
            difference = sum([abs(current[i] - previous[i]) for i in range(len(current))])
            if difference >= previous_difference:
                log.info(difference)
                log.info("T%s" % (T-1))
                log.info(previous)
                break
            previous = current
            previous_difference = difference
            T += 1
            self.update()            

    def update(self):
        for pair in self.pairs:
            pair.changed = False
        for state_1, rules in self.rules.items():
            population = sum([1 for pair in self.pairs if pair.state == state_1 and not pair.changed])
            rules = {state: int(round(percent * population)) for (state, percent) in rules.items()}
            for state_2, num in rules.items():
                p = 0
                for n in range(num):
                    while p < len(self.pairs) and (self.pairs[p].changed or self.pairs[p].state != state_1):
                        p += 1
                    if p == len(self.pairs):
                        break
                    self.pairs[p].state = state_2
                    self.pairs[p].changed = True



model = Model(RULES)
model.run()

model.mutate()
model.run()

