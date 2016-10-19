################################################################################
#  YOHOHO THIS PROGRAM     WILD BILL APPROVES OF IT    AND NATHAN MADE
# DOES MY MATHS HOMEWORK         END OF STORY                IT
################################################################################

import math

failed = 0

def quadraticsolver(a, b, c):
    try:
        squareroot = math.sqrt((b*b)-4*a*c)
    except:
        global failed
        failed = 1
        return

    print " "
    answer = (-b + squareroot)/(2*a)
    print "x = " + str(answer),
    answer = (-b - squareroot)/(2*a)
    print "or " + str(answer)

def main():
    print "Arrange the equation into the form ax^2 + bx + c then input a, c and b"
    print "The progtam will then output both roots of x."
    print " "

    quadraticsolver(input("Input a in the form of a number "),
                    input("Input b in the form of a number "),
                    input("Input c in the form of a number "))

    if failed == 1:
        print "x has no real roots."

    while 1:
        running = 1
main()
    
