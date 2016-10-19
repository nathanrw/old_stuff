from im import Client
import sys


def main():
    client = Client("localhost", 2001)
    client.start()

if __name__ == '__main__':
    try:
        main()
    except:
        print sys.excepthook(*sys.exc_info())
        w = raw_input()
