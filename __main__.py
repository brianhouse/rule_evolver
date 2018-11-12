#!/usr/bin/env python3

import random, json, math, copy
import numpy as np
from pprint import pformat
from util import config, log

log.info("START")


PAIRS = 400

RULES = {   '++': {'++': .5, '+-': .2, '-+': .1, '--': .2},    # Merton pages 40 and 55
            '+-': {'++': .3, '+-': .2, '-+': .0, '--': .5},
            '-+': {'++': .5, '+-': .0, '-+': .4, '--': .1},
            '--': {'++': .2, '+-': .1, '-+': .0, '--': .7}
            }
STATES = tuple(RULES.keys())

MAGIC = 133, 57, 24, 186


def distance(d1, d2):
    return np.linalg.norm(np.array(d1) - np.array(d2))


class Pair:

    def __init__(self):
        self.reset()

    def reset(self):
        self.state = None
        self.changed = False


class Model:

    def __init__(self, rules=None):
        self.verbose = False        
        self.pairs = [Pair() for p in range(PAIRS)]                
        if rules:
            self.rules = copy.copy(rules)
        else:
            self.rules = {state: dict(zip(STATES, list(np.random.dirichlet(np.ones(4),size=1)[0]))) for state in STATES}

    def mutate(self):
        # swap whole rule set
        self.rules[random.choice(STATES)] = dict(zip(STATES, list(np.random.dirichlet(np.ones(4),size=1)[0])))

        # swap individual
        # s1 = random.choice(STATES)
        # s2 = random.choice([state for state in states if state != s1])
        # self.rules[random.choice(STATES)][s1] = 

    def breed(self, model):
        return Model({key: (self.rules[key] if random.random() > .5 else model.rules[key]) for key in STATES})

    def stats(self):
        stats = {'++': 0, '+-': 0, '-+': 0, '--': 0}
        for pair in self.pairs:
            stats[pair.state] += 1
        return tuple(stats.values())

    def reset(self):
        for pair in self.pairs:
            pair.reset()
        self.score = None
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
        previous_dis = float('Inf')
        if self.verbose:
            log.info("--------------------------------------------------")        
            log.info("\n" + pformat(self.rules))
        while True:
            current = self.stats()
            dis = distance(current, previous)
            if dis >= previous_dis:
                break
            previous = current
            previous_dis = dis
            T += 1
            self.update()            
        self.score = distance(previous, MAGIC)
        if self.verbose:                
            log.info(dis)
            log.info("T%s" % (T-1))
            log.info(previous)
            log.info(self.score)

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



POPULATION = 100
SURVIVAL = .5
MUTATION = .1
MATE = .2

models = [Model() for i in range(POPULATION)]

best = None

generation = 0

while True:   
    try:        
        log.info("GENERATION %d" % generation) 
        generation += 1
        for model in models:
            model.run()
        models.sort(key=lambda m: m.score)
        log.info("--> %s" % models[0].score)

        if best == None or models[0].score < best.score:
            best = Model(models[0].rules)

        s = math.floor(POPULATION * SURVIVAL)    
        models = models[:s]

        random.shuffle(models)
        for m in range(int(MUTATION * len(models))):
            models[m].mutate()

        random.shuffle(models)        
        for m in range(int(MATE * len(models))):
            models[m] = models[m].breed(models[m + 1])

        models = models + [Model() for i in range(POPULATION - s - 1)] + [best]
    except KeyboardInterrupt:
        best.verbose = True
        best.run()
        best.verbose = False
        input()
        

"""

Need a gradient in the mutation so that it can converge

also need to understand why best changes

"""
