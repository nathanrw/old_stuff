f = open('./workfile.txt', 'r')

for line in f:
    print line,

print " "
print " "
print " "
print " "

jeff = "0"
monkeylord = raw_input("Kill Program? Type anything but Z to do so. ")

while jeff != 1:
    if monkeylord != "Z":
        jeff = 1
