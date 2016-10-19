#!/usr/bin/python
#filename: jeff.py

jeff = 0
print "Monkeylord!"

while jeff != 1:
	monkeyman = raw_input("Are you the pleb? Answer 'y' or 'n'. ")	

	if monkeyman == "y":
		print "YAHAHAHHAAAHAH"
		jeff = 1
	elif monkeyman == "n":
		print "Good. Do it again."
	else:
		print "I don't understand!"

	if jeff != 1:
		print " "
	else:
		print "Go away now."

