from im import Server
import sys

def main():
    server = Server()
    server.start()

if __name__ == '__main__':
    try:
        main()
    except:
        print sys.excepthook(*sys.exc_info())
        w = raw_input()
