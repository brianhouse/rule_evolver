import random, json, math, copy, time
import numpy as np
from pprint import pformat, pprint
from util import config, log, save


RULES = {   '++': {'++': .5, '+-': .2, '-+': .1, '--': .2},    # Merton pages 40 and 55
            '+-': {'++': .3, '+-': .2, '-+': .0, '--': .5},
            '-+': {'++': .5, '+-': .0, '-+': .4, '--': .1},
            '--': {'++': .2, '+-': .1, '-+': .0, '--': .7}
            }
STATES = tuple(RULES.keys())

MAGIC = 133, 57, 24, 186


class Model:

    n = 0

    def __repr__(self):
        return "%s (%d)" % (self.score, self.id)

    def show(self):
        # print("ID\t", model.id)
        print("  \t++\t+-\t-+\t--")
        print("++\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(self.rules["++"].values()))
        print("+-\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(self.rules["+-"].values()))
        print("-+\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(self.rules["-+"].values()))
        print("--\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(self.rules["--"].values()))
        if self.score != None:
            print("\t\t\t\t\t%d, %d, %d, %d (%.4f)" % (*self.counts, self.score))
        print()        

    def __init__(self, rules=None, constrained=False):
        self.id = Model.n
        Model.n += 1
        self.verbose = False    
        self.score = None    
        if rules:
            self.rules = copy.copy(rules)
        elif constrained == False:
            self.rules = {state: dict(zip(STATES, tuple(np.random.dirichlet(np.ones(4),size=1)[0]))) for state in STATES}
        else:
            self.rules = {'++': {}, '+-': {}, '-+': {}, '--': {}}
            self.rules['++'] = dict(zip(STATES, tuple(np.random.dirichlet(np.ones(4),size=1)[0])))
            l = list(np.random.dirichlet(np.ones(3),size=1)[0])
            l.insert(2, 0)
            self.rules['+-'] = dict(zip(STATES, l))
            l = list(np.random.dirichlet(np.ones(3),size=1)[0])
            l.insert(1, 0)
            self.rules['-+'] = dict(zip(STATES, l))
            l = list(np.random.dirichlet(np.ones(3),size=1)[0])
            l.insert(2, 0)
            self.rules['--'] = dict(zip(STATES, l))

    def mutate(self):
        # redo whole rule set
        # self.rules[random.choice(STATES)] = dict(zip(STATES, tuple(np.random.dirichlet(np.ones(4),size=1)[0])))

        # swap individual rules
        rule = random.choice(STATES)
        s1 = random.choice(STATES)
        s2 = random.choice([state for state in STATES if state != s1])
        v = self.rules[rule][s1]
        self.rules[rule][s1] = self.rules[rule][s2]
        self.rules[rule][s2] = v

    def breed(self, model):
        return Model({key: (copy.copy(self.rules[key]) if random.random() > .5 else copy.copy(model.rules[key])) for key in STATES})

    def reset(self):
        self.score = float('Inf')
        self.distribution = {state: 0.25 for state in STATES}

    def distance(self, d1, d2):
        return float(np.linalg.norm(np.array(d1) - np.array(d2)))

    def update(self):
        new_distribution = {state: 0.0 for state in STATES}
        for state_1 in STATES:
            for state_2 in STATES:
                new_distribution[state_2] += self.distribution[state_1] * self.rules[state_1][state_2]
        self.distribution = new_distribution        

    def run(self):
        self.reset()
        step = 0
        previous_distribution = self.distribution
        deltas = []
        if self.verbose:
            print("--------------------------------------------------")        
            pprint(self.rules)
            print()
        while True:
            self.update()            
            delta = np.array(list(self.distribution.values())) - np.array(list(previous_distribution.values()))
            if sum(abs(delta)) < 0.000001:
                break
            previous_distribution = self.distribution
            step += 1

        # calculate euclidean distance from the magic distribution
        self.counts = tuple(np.array(list(self.distribution.values())) * 400)
        self.score = self.distance(self.counts, MAGIC)

        if self.verbose:   
            print("(", step + 1, ")")
            print()
            print("%d\t%d\t%d\t%d" % self.counts)
            print(self.score)




