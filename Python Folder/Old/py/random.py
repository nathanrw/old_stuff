import random
from random import *

control = 1
number = randrange(0,20,1)

question = open("question.txt", "r").read()

print "I am thinking of a number between 0 and 20."

while control == 1:
    
    guess = input(question)

    if guess == number:
        print "yay"
        control = 0
    elif guess > 20:
        print "The number is between 0 and 20."
    else:
            if guess > number:
                print "Too high!"
            elif guess < number:
                print "Too low!"
