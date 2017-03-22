import sys
from controller import Controller

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print "Usage:", sys.argv[0], "<IP> [port]"
        sys.exit(1)

    ip = sys.argv[1]

    if (len(sys.argv) > 2):
        controller = Controller(ip, int(sys.argv[2]))
    else:
        controller = Controller(ip)

    while True:
        controller.say(sys.stdin.readline())
