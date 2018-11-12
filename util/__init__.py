import pickle
import numpy as np
from .log import log
from .config import config
   

def save(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)   