#Checks for repeated patterns in a string

running = 1

while running == 1:
    password = str(raw_input("Password: "))

    iteration = int(len(password)/2)
    counter = 0
    check = 0

    while iteration > 0:
        while counter < len(password)/iteration:
            print counter,  " ",  iteration
            
            counterIt = counter + iteration
            counterItTwo = counter + iteration*2
            
            if password[counter:counterIt] == password[counterIt:counterItTwo]:
                check = 1
                
            counter = counter + 1
            
        counter = 0
        iteration = iteration - 1

    if check == 0:
        print "ACCEPTED"
    elif check == 1:
        print "REJECTED"
    else:
        print "ERROR"
        
    if raw_input("Again? Y/N: ") == "N":
        running = 0
    
