from random import random
from math import log

def next_exp(lmbda):
    U = random()
    lmbda = 1/lmbda
    return -log(1.0 - U)/lmbda
