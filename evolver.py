#!/usr/bin/env python3

import random, json, math, copy, time
import numpy as np
from pprint import pformat
from util import config, log, save
from model import Model


POPULATION = 100
SURVIVAL = .5
TOURNAMENT = .1
MUTATION = .2
MATE = .2

THRESHOLD = 5


while True:
    log.info("//////////////////////////////////////////////////")    
    models = [Model(constrained=True) for i in range(POPULATION)]
    best = None
    best_score = 500
    generation = 0
    while True:   
        log.info("GENERATION %d" % generation) 
        for model in models:
            model.run()
        models.sort(key=lambda m: (m.score, m.id))
        log.info("--> %s" % models[0])

        if best == None or models[0].score < best.score:
            best = models[0]            
            log.info("==> new best: %s" % best.id)

        if best.score < THRESHOLD or generation == 50:
            break

        s = math.floor(POPULATION * SURVIVAL)   
        parents = [best]
        while len(parents) < s - 1:
            tournament = [random.choice(models) for i in range(round(TOURNAMENT * POPULATION))]
            tournament.sort(key=lambda m: m.score)
            parents.append(tournament[0])            
            models.remove(tournament[0])
        # log.info("selected parents")

        kids = []
        while len(kids) < POPULATION - len(parents):
            kids.append(random.choice(parents).breed(random.choice(parents)))
        # log.info("made kids")   

        models = parents + kids
        random.shuffle(models)
        for m in range(round(MUTATION * POPULATION)):
            if models[m] == best:
                continue
            models[m].mutate()
        # log.info("mutated") 

        generation += 1

    if best.score < THRESHOLD:
        best.verbose = True
        best.run()
        best.verbose = False

        save("results/%s.pkl" % int(time.time()), best)    

