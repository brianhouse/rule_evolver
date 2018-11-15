import random, json, math, copy, time
import numpy as np
from pprint import pformat, pprint
from util import config, log, save
from collections import deque

PAIRS = 400

RULES = {   '++': {'++': .5, '+-': .2, '-+': .1, '--': .2},    # Merton pages 40 and 55
            '+-': {'++': .3, '+-': .2, '-+': .0, '--': .5},
            '-+': {'++': .5, '+-': .0, '-+': .4, '--': .1},
            '--': {'++': .2, '+-': .1, '-+': .0, '--': .7}
            }
STATES = tuple(RULES.keys())

MAGIC = 133, 57, 24, 186


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

    def show(self):
        # print("ID\t", model.id)
        print("  \t++\t+-\t-+\t--")
        print("++\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(self.rules["++"].values()))
        print("+-\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(self.rules["+-"].values()))
        print("-+\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(self.rules["-+"].values()))
        print("--\t%2.2f\t%2.2f\t%2.2f\t%2.2f" % tuple(self.rules["--"].values()))
        if self.score != None:
            print("\t\t\t\t\t%2.2f, %2.2f, %2.2f, %2.2f (%.4f)" % (*self.distribution(), self.score))
        print()        

    def __init__(self, rules=None, pairs=PAIRS):
        self.id = Model.n
        Model.n += 1
        self.verbose = False        
        self.pairs = [Pair() for p in range(pairs)]
        self.score = 500
        if rules:
            self.rules = copy.copy(rules)
        else:
            self.rules = {state: dict(zip(STATES, tuple(np.random.dirichlet(np.ones(4),size=1)[0]))) for state in STATES}

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

    def distance(self, d1, d2):
        return float(np.linalg.norm(np.array(d1) - np.array(d2)))

    def distribution(self):
        dist = {'++': 0, '+-': 0, '-+': 0, '--': 0}
        for pair in self.pairs:
            dist[pair.state] += 1
        return tuple(dist.values())

    def run(self):
        self.reset()
        step = 0
        previous_distribution = (0, 0, 0, 0)
        deltas = []
        if self.verbose:
            print("--------------------------------------------------")        
            pprint(self.rules)
            print()
        while True:

            # update the model and get the number of pairs in each state
            self.update()            
            current_distribution = self.distribution()

            # find the change in the number of pairs for each state
            delta = np.array(current_distribution) - np.array(previous_distribution)
            if self.verbose:
                print("%d\t%d\t%d\t%d\t%s" % (*current_distribution, delta))
            deltas.append(delta)

            # if the changes sum over n steps, we're oscillating and should stop
            stop = False
            for n in range(1, len(deltas)):
                s = sum(abs(sum(np.array(deltas)[-n:,])))
                if s == 0:
                    if self.verbose:                    
                        print()
                        if n == 1:
                            print("EQUILIBRIUM")
                        else:
                            print("OSCILLATING WITH PERIOD %d" % n)
                    stop = True
                    break
            if stop:
                break

            # keep track for next round    
            previous_distribution = current_distribution
            step += 1

        # calculate euclidean distance from the magic distribution
        self.score = self.distance(current_distribution, MAGIC)

        if self.verbose:   
            print("(", step + 1, ")")
            print()
            print(("%d\t%d\t%d\t%d" % tuple(current_distribution)))
            print(self.score)


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


