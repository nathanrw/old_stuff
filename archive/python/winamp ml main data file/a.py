def bytesToDec(bytes):
	num = 0
	for leftness, byte in enumerate(bytes):
		num += ord(byte) * 16 ** (len(bytes)-leftness)
	return num

def read(filename):
	
	file = open(filename, "rb")
	
	file.read(8)
	
	numRecords = bytesToDec(file.read(4))

def main():
	read("main.dat")

if __name__ == '__main__':
	main()