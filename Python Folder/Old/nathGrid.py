def nathGrid(sideone, sidetwo):
    topside = range(sideone)
    leftside = range(sidetwo)

    grid = [topside, leftside]

    return grid

number = nathGrid(20,20)

print number[0]
print number[1]
