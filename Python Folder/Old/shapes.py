class polygon():
    def init(self, coordinates):
        self.coordinates = coordinates
    def add(self):
        rounded_coordinates = []
        coords = []
        for coordinates in self.coordinates:
            coord = []
            for coordinate in coordinates:
                coord.append(int(coordinate))
            rounded_coordinates.append(coord)
        return rounded_coordinates

def CreateCube(size,pos):
    Cube = []
    #           Face            X           Y               Z
    Cube.append(polygon([(-1*size+pos[0],1*size+pos[1],-1*size+pos[2]),
                         (-1*size+pos[0],-1*size+pos[1],-1*size+pos[2]),
                         (1*size+pos[0],-1*size+pos[1],-1*size+pos[2]),
                         (1*size+pos[0],1*size+pos[1],-1*size+pos[2])
                         ]
                        )
                )
    Cube.append(polygon([(-1*size+pos[0],1*size+pos[1],-1*size+pos[2]),
                         (-1*size+pos[0],-1*size+pos[1],-1*size+pos[2]),
                         (-1*size+pos[0],-1*size+pos[1],1*size+pos[2]),
                         (-1*size+pos[0],1*size+pos[1],1*size+pos[2])
                         ]
                        )
                )
    Cube.append(polygon([(-1*size+pos[0],1*size+pos[1],-1*size+pos[2]),
                         (1*size+pos[0],1*size+pos[1],-1*size+pos[2]),
                         (1*size+pos[0],1*size+pos[1],1*size+pos[2]),
                         (-1*size+pos[0],1*size+pos[-1],1*size+pos[2])
                         ]
                        )
                )
    Cube.append(polygon([(1*size+pos[0],-1*size+pos[1],1*size+pos[2]),
                         (1*size+pos[0],1*size+pos[1],1*size+pos[2]),
                         (-1*size+pos[0],1*size+pos[1],1*size+pos[2]),
                         (-1*size+pos[0],-1*size+pos[1],1*size+pos[2])
                         ]
                        )
                )
    Cube.append(polygon([(1*size+pos[0],-1*size+pos[1],1*size+pos[2]),
                         (-1*size+pos[0],-1*size+pos[1],1*size+pos[2]),
                         (-1*size+pos[0],-1*size+pos[1],-1*size+pos[2]),
                         (1*size+pos[0],-1*size+pos[1],-1*size+pos[2])
                         ]
                        )
                )
    Cube.append(polygon([(1*size+pos[0],1*size+pos[1],1*size+pos[2]),
                         (1*size+pos[0],-1*size+pos[1],1*size+pos[2]),
                         (1*size+pos[0],-1*size+pos[1],-1*size+pos[2]),
                         (1*size+pos[0],1*size+pos[1],-1*size+pos[2])
                         ]
                        )
                )
    return Cube
