on = 1

while on == 1:

        numtimes = input("How many times shall I say Ni?")
	
        while numtimes > 0:
                numtimes = numtimes-1
                print "Ni!"

        ifon = raw_input("Again? Y/N ")

        if ifon == "Y":
                on = 1
        elif ifon != "Y":
                on = 0
