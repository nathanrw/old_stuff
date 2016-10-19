# Gas Mark <-> Farenheiht

from math import log

kf = 275.0

def Tf_to_Tg(Tf):
	if Tf < kf:
		return 2.0**((Tf - kf)/25.0)
	elif Tf >= kf:
		return (Tf - kf)/25.0 + 1

def Tg_to_Tf(Tg):
	if Tg < 1:
		return 25*log(Tg,2) + kf
	elif Tg >= 1:
		return 25*(Tg - 1) + kf

def main():
	print "Gas Mark <-> Farenheit Converter"
	
	print "Type 1 for Farenheit -> Gas Mark."
	print "Type 2 for Gas Mark -> Farenheit."
	
	type = input("Number: ")
	
	T = input("Temperature: ")
	
	if type == 1:
		print "Temperature in gas mark = ", Tf_to_Tg(T)
	elif type == 2:
		print "Temperatyre in farenheit = ", Tg_to_Tf(T)

if __name__ == '__main__':main()