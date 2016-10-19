from math import sin, cos, radians

sintable = {}
fract_parts = 10.0
for x in range(0,2000):
	counter = 0.0
	while counter < fract_parts:
		num = x+(counter*1/fract_parts)
		sintable[str(num)] = sin(radians(num))
		counter+=1
		
costable = {}
fract_parts = 10.0
for x in range(0,2000):
	counter = 0
	while counter < fract_parts:
		num = x+(counter*1/fract_parts)
		costable[str(num)] = cos(radians(num))
		counter+=1
		
def sine(x):
	x = int(x)
	if x < 0:
		x = 360 - x
	num = str(x) + ".0"
	return sintable[num]

def cosine(x):
	x = int(x)
	if x < 0:
		x = 360 - x
	num = str(x) + ".0"
	return costable[num]

print sine(30.83465346)