#The Amazing Generator Of Words
#Made By Nathan

import random

nounlist = ["chips", "spam", "dog", "Sparta", "ninja", "choo choo", "poo"]
verblist = ["Run", "Jump", "said"]
adjlist = ["big", "small", "large", "madness", "blasphemy", "1337"]
conctlist = ["was", "there", "the", "it", "also", "and"]

def title(nounlist):

    print nounlist[random.randrange(0,len(nounlist))]
    print " "

def verse(nounlist, verblist, adjlist, conctlist):
    
    numlines = random.randrange(4,12)
    wordcounter = 0
    linecounter = 0
    
    while linecounter != numlines:
        linelength = random.randrange(6, 10)
        linecounter = linecounter + 1
        wordcounter = 0
        checker = 0
        
        while wordcounter != linelength:
            
            wordcounter = wordcounter + 1
            wordtype = random.randrange(1,3)
            
            if wordtype == 1:
                
                if checker == 1:
                    print verblist[random.randrange(0,len(verblist))],
                else:
                    print nounlist[random.randrange(0,len(nounlist))],
                    
            elif wordtype == 2:

                if checker == 0:
                    print nounlist[random.randrange(0,len(nounlist))],
                elif checker == 2:
                    print adjlist[random.randrange(0,len(adjlist))],
                else:
                    print verblist[random.randrange(0,len(verblist))],
                    
            elif wordtype == 3:

                if checker == 0:
                    print nounlist[random.randrange(0,len(nounlist))],
                else:
                    print adjlist[random.randrange(0,len(adjlist))],

            checker = wordtype

        print " "
        
    print " "

def chorus(nounlist, verblist, adjlist, conctlist):
    wordcounter = 0
    linecounter = 0
    chorus = []
    numlines = random.randrange(4,6)

    while linecounter != numlines:
        linelength = 6
        linecounter = linecounter + 1
        wordcounter = 0
        
        while wordcounter != linelength:
            
            wordcounter = wordcounter + 1
            wordtype = random.randrange(1,4)
            
            if wordtype == 1:
                chorus.append(nounlist[random.randrange(0,3)])
            elif wordtype == 2:
                chorus.append(verblist[random.randrange(0,3)])
            elif wordtype == 3:
                chorus.append(adjlist[random.randrange(0,3)])

            checker = wordtype

    return chorus

def printlist(thelist):
    
    counter = 0
    linebreaker = 6

    while counter != len(thelist):
        print thelist[counter],
        counter = counter + 1
        if counter == linebreaker:
            print " "
            linebreaker = linebreaker + 6
    print " "

def main():

    chor = chorus(nounlist, verblist, adjlist, conctlist)

    title(nounlist)
    verse(nounlist, verblist, adjlist, conctlist)
    printlist(chor)
    verse(nounlist, verblist, adjlist, conctlist)
    verse(nounlist, verblist, adjlist, conctlist)
    printlist(chor)

main()
