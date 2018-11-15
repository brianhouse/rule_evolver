#!/usr/bin/env python3

import os, time
from util import load, save
from model import Model, Pair, RULES, STATES

DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "results"))


OSC = {'++': {'++': 0.051114711003092395,
        '+-': 0.6591129505716349,
        '-+': 0.25165885010328753,
        '--': 0.03811348832198512},
 '+-': {'++': 0.601656751634339,
        '+-': 0.05678985976484729,
        '-+': 0.04455935933774642,
        '--': 0.29699402926306734},
 '-+': {'++': 0.032827221750750875,
        '+-': 0.2644069822431973,
        '-+': 0.28231521678935967,
        '--': 0.42045057921669216},
 '--': {'++': 0.20319675590754216,
        '+-': 0.5421944883195703,
        '-+': 0.040637702961412725,
        '--': 0.21397105281147477}}

LONG = {'++': {'++': 0.026286865182543605,
        '+-': 0.39834957897602824,
        '-+': 0.20805296700040998,
        '--': 0.36731058884101814},
 '+-': {'++': 0.3156478646655827,
        '+-': 0.5047659862178565,
        '-+': 0.17423186168884394,
        '--': 0.005354287427716961},
 '-+': {'++': 0.003131233256842903,
        '+-': 0.003696661026185481,
        '-+': 0.9507677401796908,
        '--': 0.042404365537280844},
 '--': {'++': 0.3853021685751117,
        '+-': 0.27640723793567074,
        '-+': 0.025686252595463862,
        '--': 0.31260434089375366}}        


# model = Model(RULES)
# model = Model(OSC, 400)
model = Model()
model.verbose = True
model.run()
# baseline.show()




"""

Oscillation just depends on the number of pairs

if the percentages have to be scaled to current number of pairs of that state, as that translates to a whole number it change shift

so you might get oscillation periods of any length -- you could keep the deltas in a deque, and if they equal 1 at various periods, it's oscillating

but that seems like too much


dude, this is totally a constrained digital emergence problem

would be cool to know -- what's the longest oscillation we could get? could we actually produce a chaotic system?


what's the significance of equilibrium in this context?


"""