import qi

global session
global text_service
global posture_service
global motion_service
global tabletService

NAO_IP = '192.168.1.102'
NAO_PORT = '9559'

def establish_connection():
    session = qi.Session()
    session.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
    text_service = session.service("ALTextToSpeech")
    posture_service = session.service("ALRobotPosture")
    motion_service = session.service("ALMotion")
    tabletService = session.service("ALTabletService")

class Action:
    def process_action(self):
        print("No such action is supported")
#----------------------------------------------------------------------------------------------------------------------#
class Speech(Action):
    def __init__(self, distance):
        self.distance = distance

    def process_action(self):
        return 1
    #Pepper API calls go here
# ----------------------------------------------------------------------------------------------------------------------#
class Movement(Action):
    def __init__(self, distance):
        self.distance = distance

    def process_action(self):
        return 1
        #Pepper API calls go here
# ----------------------------------------------------------------------------------------------------------------------#
class Turn(Action):
    def __init__(self, angle):
        self.angle = angle

    def process_action(self):
        return 1
        #Pepper API calls go here
# ----------------------------------------------------------------------------------------------------------------------#
class Sequence(Action):
    def __init__(self, angle):
        self.angle = angle

    def process_action(self):
        return 1
        #Pepper API calls go here
# ----------------------------------------------------------------------------------------------------------------------#
class MediaDisplay(Action):
    def __init__(self, angle):
        self.angle = angle

    def process_action(self):
        return 1
        #Pepper API calls go here
# ----------------------------------------------------------------------------------------------------------------------#