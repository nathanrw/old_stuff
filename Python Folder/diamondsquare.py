#Diamond_Square.py
#Makes a random heightmap.

from random import randrange

byterange = range(0,256)


def mapgen(size):

    heightmap = []
    for x in range(0,size+1):
        heightmap.append([])
        for y in range(0,size+1):
            heightmap[x].append(0)

    d = randrange(0,10001)/10000.0

    A = [0,0]; B = [size,0]
    C = [0,size]; D = [size,size]

    step = size

    heightmap[0][0]         = randrange(byterange)
    heightmap[0][size]      = randrange(byterange)
    heightmap[size][0]      = randrange(byterange)
    heightmap[size][size]   = randrange(byterange)

    

    
