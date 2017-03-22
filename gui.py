import os
import math
import pygame
from pygame.locals import *
import joy_conf

def zero_cap(x, e = 0.11):
    if abs(x) <= e: return 0
    else: return x

class Gui:

    controller = None
    joy = None

    def __init__(self, size = [320, 240]):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Nao controller")
        # Initialize the joysticks
        pygame.joystick.init()
        self.lastx = 0
        self.lasttheta = 0
        self.lastheadYaw = 0
        self.lastheadPitch = 0
        self.pose = 0
        self.aware = False

    def connectJoystick(self, joy_id):
        self.joy = pygame.joystick.Joystick(joy_id)
        self.joy.init()

    def showAxes(self):
        print "==>AXES"
        for i in range(self.joy.get_numaxes()):
            print i, ":", self.joy.get_axis(i)
        print "<==AXES"

    def get_axis(self, axis):
        return self.joy.get_axis(joy_conf.axes[axis])

    def applyJoystickAxes(self):
        if self.controller and self.joy:
            x = zero_cap(-self.get_axis('forward'))
            y = zero_cap((self.get_axis('strafe_left') -
                          self.get_axis('strafe_right')) / 2.,
                         0.1)
            a0 = zero_cap(self.get_axis('rotation'))
            theta = -math.copysign(a0 ** 2, a0)
            headYaw = zero_cap(-self.get_axis('head_yaw') * 2)
            headPitch = zero_cap(self.get_axis('head_pitch') * 0.5)
            self.controller.moveToward(x, y, theta)
            if x!= self.lastx or theta != self.lasttheta:
              self.lastx = x
              self.lasttheta = theta
            if headYaw != self.lastheadYaw or headPitch != self.lastheadPitch:
                self.lastheadYaw = headYaw
                self.lastheadPitch = headPitch
                self.controller.setHeadYaw(headYaw)
                self.controller.setHeadPitch(headPitch)

    def setPose(self):
        if self.pose == 0:
            self.controller.sit()
        elif self.pose == 1:
            self.controller.crouch()
        elif self.pose == 2:
            self.controller.stand()

    def onJoystickHatMotion(self):
        if self.joy.get_hat(0)[1] == 1:
            self.pose = min(3, self.pose + 1)
        elif self.joy.get_hat(0)[1] == -1:
            self.pose = max(0, self.pose - 1)
        self.setPose()

    def toggleAwareness(self):
        if self.aware:
            self.controller.stopAwareness()
        else:
            self.controller.startAwareness()
        self.aware = not self.aware
        print "I am aware:", self.aware

    def printButtons(self):
        print "==>BUTTONS"
        for i in range(self.joy.get_numbuttons()):
            print i, ":", self.joy.get_button(i)
        print "<==BUTTONS"

    def get_button(self, button):
        return self.joy.get_button(joy_conf.buttons[button])

    def onJoystickButtonDown(self):
        if self.get_button('hey_btn'):
            self.controller.hey()
#        elif self.joy.get_button(3):
#            self.toggleAwareness()
        elif self.get_button('stop_btn'):
            self.controller.stopMove()
        elif self.get_button('rest_btn'):
            self.controller.rest()
        elif self.get_button('wakeup_btn'):
            self.controller.wakeUp()

    def mainloop(self):
        clock = pygame.time.Clock()
        done = False
        while done == False:
            # Event processing
            #self.printButtons()
            #self.showAxes()
            events = pygame.event.get()
            self.applyJoystickAxes()
            for event in events:
                if event.type == QUIT:
                    done = True
                elif event.type == JOYBUTTONDOWN:
                    self.onJoystickButtonDown()
                elif event.type == JOYHATMOTION:
                    self.onJoystickHatMotion()
            clock.tick(10)
        pygame.quit()

    def registerController(self, controller):
        self.controller = controller

