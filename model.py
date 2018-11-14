import random, json, math, copy, time
import numpy as np
from pprint import pformat
from util import config, log, save

PAIRS = 400

RULES = {   '++': {'++': .5, '+-': .2, '-+': .1, '--': .2},    # Merton pages 40 and 55
            '+-': {'++': .3, '+-': .2, '-+': .0, '--': .5},
            '-+': {'++': .5, '+-': .0, '-+': .4, '--': .1},
            '--': {'++': .2, '+-': .1, '-+': .0, '--': .7}
            }
STATES = tuple(RULES.keys())

MAGIC = [x / 400 for x in [133, 57, 24, 186]]


class Pair:

    def __init__(self):
        self.reset()

    def reset(self):
        self.state = None
        self.changed = False


class Model:

    n = 0

    def __repr__(self):
        return "%s (%d)" % (self.score, self.id)

    def __init__(self, rules=None):
        self.id = Model.n
        Model.n += 1
        self.verbose = False        
        self.pairs = [Pair() for p in range(PAIRS)]
        self.score = 500
        if rules:
            self.rules = copy.copy(rules)
        else:
            self.rules = {state: dict(zip(STATES, list(np.random.dirichlet(np.ones(4),size=1)[0]))) for state in STATES}

    def mutate(self):
        # redo whole rule set
        # self.rules[random.choice(STATES)] = dict(zip(STATES, list(np.random.dirichlet(np.ones(4),size=1)[0])))

        # swap individual rules
        rule = random.choice(STATES)
        s1 = random.choice(STATES)
        s2 = random.choice([state for state in STATES if state != s1])
        v = self.rules[rule][s1]
        self.rules[rule][s1] = self.rules[rule][s2]
        self.rules[rule][s2] = v

    def breed(self, model):
        return Model({key: (copy.copy(self.rules[key]) if random.random() > .5 else copy.copy(model.rules[key])) for key in STATES})

    def distribution(self):
        stats = {'++': 0, '+-': 0, '-+': 0, '--': 0}
        for pair in self.pairs:
            stats[pair.state] += 1
        return [x / PAIRS for x in tuple(stats.values())]

    def distance(self, d1, d2):
        return np.linalg.norm(np.array(d1) - np.array(d2))        

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
            current = self.distribution()
            dis = self.distance(current, previous)
            if dis >= previous_dis:
                break
            previous = current
            previous_dis = dis
            T += 1
            self.update()            
        self.score = self.distance(previous, MAGIC)
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


