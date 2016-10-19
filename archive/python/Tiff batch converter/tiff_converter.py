import pygame, os

def process_tiff(name):
	if name[-4:] == ".tif" or name[-4:] == ".TIF":
		end = -4
	elif name[-5:] == ".tiff" or name[-5:] == ".TIFF":
		end = -5
	else:
		return
	print ""
	print "Loading %s" % name
	img = pygame.image.load(name)
	print "Image Loaded."
	out = "output/" + name[:end] + ".jpg"
	print "Saving file to %s" % out
	pygame.image.save(img, out)
	print "Image Saved."
	print ""

def main():
	print "Will convert all TIFF files into JPEG files."
	pygame.init()
	files = os.listdir("./")
	try: os.mkdir("output")
	except: pass
	counter = 0
	for file in files:
		process_tiff(file)
	pygame.display.quit()
	print "Done."

if __name__ == '__main__':main()