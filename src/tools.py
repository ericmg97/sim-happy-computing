from random import random
import math

def inverse_method(f):
    u = random()
    x = 0
    acum = 0
    for y, p in f:
        acum += p
        if u < acum:
            x = y
            break
    return x

def exponential(lamb):
    u = random()
    x = - (1 / lamb) * math.log(u)
    return x

def normal(mean, var):
    x = 0
    while True:
        y = exponential(1)
        u = random()
        c = math.exp((-(y - 1)**2) / 2)
        if u <= c:
            x = mean + var*y
            break 
    return x

def daytime(minutes):
        time = divmod(minutes, 60)
        return "%02d:%02d"%((time[0] + 8, time[1]))