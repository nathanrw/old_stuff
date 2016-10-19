try:
    import psyco
    psyco.full()
except:
    print "Failed to import psyco."
    
from game import Game

def main():
    Game().mainLoop()

if __name__ == "__main__": main()