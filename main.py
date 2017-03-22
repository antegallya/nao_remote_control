import sys
from controller import Controller

from gui import Gui

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print "Usage:", sys.argv[0], "<IP> <joy_id>"
        sys.exit(1)

    ip = sys.argv[1]

    #if (len(sys.argv) > 2):
    #    controller = Controller(ip, int(sys.argv[2]))
    #else:
    controller = Controller(ip)

    gui = Gui()
    gui.registerController(controller)
    gui.connectJoystick(int(sys.argv[2]))
    gui.mainloop()
