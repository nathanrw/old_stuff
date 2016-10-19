#Random
from math import *
from time import time

def f(x):
    return sin(exp(x))

def g(x):
    x = x/1000
    if x > 40:
        return (((x/40)+1)*40) - (x/40)
    elif x < 40:
        return 5

def x():
    x = str(time()/100000)
    counter = len(x)-1
    new = []
    while counter > len(x)-6:
        new.append(x[counter])
        counter -= 1
    x = str(new[0]) + str(new[1]) + str(new[2]) + \
        str(new[3]) + str(new[4])
    return int(x)

def random(multiplier):
    return f(x()/1000) * multiplier

print random(1000)
