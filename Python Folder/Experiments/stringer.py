lines = []
lol = " Hello, I am awesome and am rather awesome <ENDLINE> awesomecool, hoohar <ENDLINE> awesomeawesomecooooool.<ENDLINE>"

counter = 0
last = 0
while counter < len(lol):
	if lol[counter:counter+len("<ENDLINE>")] == "<ENDLINE>":
		line = lol[last:counter]
		last = counter+len("<ENDLINE>")
	counter += 1
print lines