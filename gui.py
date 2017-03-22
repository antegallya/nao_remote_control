import os
import math
import pygame
from pygame.locals import *
import joy_conf

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
        for i in range(15):
            print i, ":", self.joy.get_axis(i)
        print "<==AXES"

    def applyJoystickAxes(self):
        if self.controller and self.joy:
            #self.showAxes()
            x = -self.joy.get_axis(joy_conf.forward)
            y = (self.joy.get_axis(joy_conf.strafe_left) -
                 self.joy.get_axis(joy_conf.strafe_right)) / 2.
            #y = 0
            a0 = self.joy.get_axis(joy_conf.rotation)
            theta = -math.copysign(a0 ** 2, a0)
            headYaw = -self.joy.get_axis(joy_conf.head_yaw) * 2
            headPitch = self.joy.get_axis(joy_conf.head_pitch) * 0.5
            #if x != self.lastx or theta != self.lasttheta:
            self.lastx = x
            self.controller.moveToward(x, y, theta)
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
        for i in range(11):
            print i, ":", self.joy.get_button(i)
        print "<==BUTTONS"

    def onJoystickButtonDown(self):
        self.printButtons()
        if self.joy.get_button(joy_conf.hey_btn):
            self.controller.hey()
#        elif self.joy.get_button(3):
#            self.toggleAwareness()
        elif self.joy.get_button(joy_conf.stop_btn):
            self.controller.stopMove()
        elif self.joy.get_button(joy_conf.rest_btn):
            self.controller.rest()
        elif self.joy.get_button(joy_conf.wakeup_btn):
            self.controller.wakeUp()

    def mainloop(self):
        clock = pygame.time.Clock()
        done = False
        while done == False:
            # Event processing
            #self.printButtons()
            events = pygame.event.get()
            self.applyJoystickAxes()
            for event in events:
                if event.type == QUIT:
                    done = True
                #elif event.type == JOYAXISMOTION:
                elif event.type == JOYBUTTONDOWN:
                    self.onJoystickButtonDown()
                elif event.type == JOYHATMOTION:
                    self.onJoystickHatMotion()
            clock.tick(10)
        pygame.quit()

    def registerController(self, controller):
        self.controller = controller

