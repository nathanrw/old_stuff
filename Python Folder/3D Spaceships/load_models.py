#Load Models

from md_ship import vertices as v
from md_ship import faces as f

def lm(f, v):
    return get_faces(f,get_vertices(v))

def get_vertex(v):

    counter0 = 0
    counter1 = 1

    while v[counter1] != " ":
        counter1 += 1

    x = float(v[counter0:counter1])

    counter0 = counter1 + 1
    counter1 = counter0

    while v[counter1] != " ":
        counter1 += 1

    y = float(v[counter0:counter1])

    counter0 = counter1 + 1
    counter1 = counter0

    while counter1 < len(v):
        counter1 += 1

    z = float(v[counter0:counter1])

    return [x,z,y]

def get_vertices(vlist):
    vlist = vlist[1:-1]
    vertices = []

    counter0 = 0
    counter1 = 0
    end = 0

    a = len(vlist)-1

    counter1 += 2
    counter0 = counter1

    while not end:
        
        while vlist[counter1] != "v" and counter1 < a:
            counter1 += 1
        vertices.append(get_vertex(vlist[counter0:counter1]))
        counter1 += 2
        counter0 = counter1
        if counter0 >= a:
            end = 1

    return vertices

def get_face(f, vertices):
    f = f[:-1]

    counter0 = 0
    counter1 = 0
    end = 0
    a = len(f)-1

    v = []
    
    while not end and counter1 < a:

        while f[counter1] != "/":
            counter1 += 1
        v.append(vertices[int(f[counter0:counter1])-1])
        counter1 += 3
        counter0 = counter1

    return v

def get_faces(flist, vertices):
    flist = flist[1:] + " "
    polygons = []

    counter0 = 0
    counter1 = 0
    end = 0
    a = len(flist)-1

    counter1 += 2
    counter0 = counter1

    while not end:
        newpoly = []
        while flist[counter1] != "f" and counter1 < a:
            counter1 += 1
        polygons.append(get_face(flist[counter0:counter1],vertices))
        counter1 += 2
        counter0 = counter1
        if counter0 >= a:
            end = 1

    return polygons
