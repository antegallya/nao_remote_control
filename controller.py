from naoqi import ALProxy

class Controller:
    """ Control the robot and manage the proxies """

    def __init__(self, ip, port = 9559):
        self.ip = ip
        self.port = port
        self.connect_proxies()

    def connect_proxies(self):
        self.ttsp = ALProxy("ALTextToSpeech", self.ip, self.port)
        self.memp = ALProxy("ALMemory", self.ip, self.port)
        self.behp = ALProxy("ALBehaviorManager", self.ip, self.port)
        self.motp = ALProxy("ALMotion", self.ip, self.port)
        self.posp = ALProxy("ALRobotPosture", self.ip, self.port)
        self.resp = ALProxy("ALResourceManager", self.ip, self.port)
        try:
            self.awap = ALProxy('ALBasicAwareness', self.ip, self.port)
        except:
            self.awap = None

    def moveToward(self, x, y, theta):
        self.motp.moveToward(x, y, theta)

    def setHeadYaw(self, angle, fractionMaxSpeed = 0.2):
        self.motp.setAngles("HeadYaw", angle,
                fractionMaxSpeed)

    def setHeadPitch(self, angle, fractionMaxSpeed = 0.2):
        self.motp.setAngles("HeadPitch", angle,
                fractionMaxSpeed)

    def stopMove(self):
        self.motp.stopMove()

    def startBehavior(self, beh):
        if self.behp.getRunningBehaviors() == []:
            self.behp.startBehavior(beh)
        else:
            print "SOME BEHAVIOR ALREADY RUNNING"

    def hey(self):
        self.startBehavior('animations/Stand/Gestures/Hey_1')

    def say(self, message):
        self.ttsp.say(message)

    def isAwarenessRunning(self):
        self.awap.isAwarenessRunning()
    def startAwareness(self):
        self.awap.startAwareness()
    def stopAwareness(self):
        self.awap.stopAwareness()

    def wakeUp(self):
        self.motp.wakeUp()

    def rest(self):
        self.motp.rest()

    def crouch(self, speed=1.0):
        print "CROUCH"
        #self.startBehavior('dialog_posture/bhv_crouch')
        self.posp.goToPosture("Crouch", speed)
    def lieBack(self, speed=1.0):
        print "LIE DOWN BACK"
        self.startBehavior('dialog_posture/bhv_lie_down_back')
        #self.posp.goToPosture("LyingBack", speed)
    def lieBelly(self, speed=1.0):
        print "LIE DOWN BELLY"
        self.startBehavior('dialog_posture/bhv_lie_down_belly')
        #self.posp.goToPosture("LyingBelly", speed)
    def sit(self, speed=1.0):
        print "SIT"
        #self.startBehavior('dialog_posture/bhv_sit_down')
        self.posp.goToPosture("Sit", speed)
    def stand(self, speed=0.8):
        print "STAND UP"
        #self.startBehavior('dialog_posture/bhv_stand_up')
        self.posp.goToPosture("Stand", speed)

