import pygame; from pygame.locals import *
from math import *

from vector_maths import *

global inv_255
inv_255 = 1/255.0

#Groups points into edges.
def get_edges(polygon):
    counter = 0
    edges = []
    while counter < len(polygon.points):
        edges.append([polygon.points[counter],polygon.points[counter-1]])
        counter += 1
    return edges

#Determines left or right.
#Left is 1.
def side(edge):
    if edge[0][1] > edge[1][1]:
        return 0
    else:
        return 1

#Returns 1 if the edge is
#horizontal and should thus
#be ignored.
def horz(edge):
    if edge[0][1] == edge[1][1]:
        return 1
    else: return 0

#Sorts by depth. Dodgy.
def sort(polygons):
    z = []
    for polygon in polygons:
        if polygon.average[2] not in z:
            z.append(polygon.average[2])
    z.sort(reverse=1)
    newpolies = []
    for z_level in z:
        for polygon in polygons:
            if polygon.average[2] == z_level:
                newpolies.append(polygon)
    return newpolies

def get_limits(polygon, camera_size):
    #Lists of start and end x values.
    left = limits_array(camera_size)
    right = limits_array(camera_size)

    #Group points into edges.
    edges = get_edges(polygon)
    #Max and min y.
    minmax = [edges[0][0][1],edges[0][0][1]]
    
    for edge in edges:

        #Get min and max y values
        #for this polygon.
        if edge[0][1] < minmax[0]:
            minmax[0] = edge[0][1]
        elif edge[0][1] > minmax[1]:
            minmax[1] = edge[0][1]
        if edge[1][1] < minmax[0]:
            minmax[0] = edge[1][1]
        elif edge[1][1] > minmax[1]:
            minmax[1] = edge[1][1]

        #Edge is non horizontal.
        if horz(edge) != 1:
            
            #Left edge.
            if side(edge) == 1:

                #Gradient of the edge.
                change_in_x_per_y = (edge[1][0] - edge[0][0]) / \
                                    (edge[1][1] - edge[0][1])

                #First and last values of y.
                start_y = int(ceil(edge[0][1]))
                end_y = int(ceil(edge[1][1]))

                #Current value of x.
                x = edge[0][0] + (float(start_y) - edge[0][1]) * change_in_x_per_y

                y = start_y
                while y < end_y:
                    left[y] = ceil(x)
                    x += change_in_x_per_y 
                    y += 1
                    
            #Right edge.
            else:
                
                #Gradient of the edge.
                change_in_x_per_y = (edge[0][0] - edge[1][0]) / \
                                    (edge[0][1] - edge[1][1])
                
                #First and last values of y.
                start_y = int(ceil(edge[1][1]))
                end_y = int(ceil(edge[0][1]))
                
                #Current value of x.
                x = edge[1][0] + (float(start_y) - edge[1][1]) * change_in_x_per_y

                y = start_y
                while y < end_y:
                    right[y] = ceil(x)
                    x += change_in_x_per_y 
                    y += 1
                    
        #Horizontal edges are ignored.
        else:
            pass

    #Returns list of left starting points, right ending points
    #and the minumum and maximum values of y.
    return left, right, minmax
                
def limits_array(camera_size):
    lim = []
    for y in range(0,camera_size[1]+1):
        lim.append(0)
    return lim
    
def filler(polygons, camera, surface):
    camera_size = camera.size

    #For all polygons
    for polygon in sort(polygons):

        #Faaaaaaaast
        if polygon.texture is None:

            #Get colour.
            try: colour = polygon.colour
            except:colour = [100,100,100]
            colour[0] = int(colour[0]*polygon.colourmod[0]*inv_255)
            colour[1] = int(colour[1]*polygon.colourmod[1]*inv_255)
            colour[2] = int(colour[2]*polygon.colourmod[2]*inv_255)
            if colour[0]>255:colour[0]=255
            if colour[1]>255:colour[1]=255
            if colour[2]>255:colour[2]=255
            colour = surface.map_rgb(colour)

            #Fill whole polygon.
            pygame.draw.polygon(surface,colour,polygon.points)

        #Sloooooooow
        elif polygon.texture is not None:

            #Scan Conversion.
            left, right, minmax = get_limits(polygon, camera_size)

            P = polygon.P
            M = polygon.M
            N = polygon.N

            A = cross_product_3D(P,N)
            B = cross_product_3D(M,P)
            C = cross_product_3D(N,M)

            xmod = camera.size[0]/2
            ymod = camera.size[1]/2

            S = [0,0,camera.dist]
            #return

            surf = pygame.surfarray.pixels2d(surface)
            tex = pygame.surfarray.pixels2d(polygon.texture.convert_alpha())
            #For each row in the polygon.
            for y in range(minmax[0]+1, minmax[1]+1):
                S[1] = y - ymod
                leftlim = int(left[y])
                rightlim = int(right[y])
                if leftlim < rightlim:
                    row = surf[leftlim:rightlim,y]
                    #For pixel in row
                    for x in range(leftlim,rightlim):
                        S[0] = x - xmod

                        a = dot_product_3D(S,A)
                        b = dot_product_3D(S,B)
                        c = 1.0/dot_product_3D(S,C)

                        u = int((polygon.texture.get_width()-1) * a * c)
                        v = int((polygon.texture.get_height()-1) * b * c)

                        #Get texel from texture, light it, then copy it to
                        #a row to be drawn to the screen.
                        col = surface.unmap_rgb(tex[u,v])
                        col = [int(col[0]*polygon.colourmod[0]*inv_255),
                               int(col[1]*polygon.colourmod[1]*inv_255),
                               int(col[2]*polygon.colourmod[2]*inv_255)]
                        if col[0] > 255: col[0] = 255
                        if col[1] > 255: col[1] = 255
                        if col[2] > 255: col[2] = 255
                        row[x-leftlim] = surface.map_rgb(col)
                    surf[leftlim:rightlim,y] = row
