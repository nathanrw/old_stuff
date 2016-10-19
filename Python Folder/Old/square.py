def nathSquare(number):
    square = number*number
    return square

on = 1

while on == 1:

    enterednumber = input("What number do you wish to square? ")

    print nathSquare(enterednumber)

    ifon = raw_input("Again? Y/N ")

    if ifon == "Y":
        on = 1
    elif ifon == "N":
        on = 0
    else:
        on = 0
        print "Unrecognised answer. This will be interpreted as a no"
