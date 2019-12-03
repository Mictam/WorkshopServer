import os
import qi
import time
import sys
import json

sys.path.insert(1, '/res/img')

global session
global text_service
global posture_service
global motion_service
global tabletService
global NAO_IP
global NAO_PORT

NAO_IP = '192.168.1.104'
NAO_PORT = '9559'

def establish_connection():
    session = qi.Session()
    session.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
    text_service = session.service("ALTextToSpeech")
    posture_service = session.service("ALRobotPosture")
    motion_service = session.service("ALMotion")
    tabletService = session.service("ALTabletService")
    print("Connection with robot established")

class Action:
    def process_action(self):
        print("No such action is supported")
#----------------------------------------------------------------------------------------------------------------------#
class Speech(Action):
    def __init__(self, text, volume, speech_speed, language):
        self.text = text
        self.volume = volume
        self.speech_speed = speech_speed
        self.language = language

    def process_action(self):
        print("saying: ")
        session1 = qi.Session()
        session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
        tts = session1.service("ALTextToSpeech")
        tts.setVoice("naoenu")
        tts.setLanguage(self.language)
        tts.setVolume(self.volume)
        tts.setParameter("speed", self.speech_speed)
        tts.say(self.text)
        print("end")
        return "Success", 200

    #Pepper API calls go here
# ----------------------------------------------------------------------------------------------------------------------#
class Movement(Action):
    def __init__(self, distance):
        self.distance = distance

    def process_action(self):
        #Pepper API calls go here
        session1 = qi.Session()
        session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
        print("Move forward process action")
        print(self.distance)
        posture_service1 = session1.service("ALRobotPosture")
        motion_service1 = session1.service("ALMotion")
        posture_service1.goToPosture("Stand", 0.5)
        rounds = float(0.5)
        turns = rounds * 0.5 * 3.14
        time = rounds * 2.0
        motion_service1.moveTo(float(self.distance), 0, 0, time)
        return "Success", 200
# ----------------------------------------------------------------------------------------------------------------------#
class Turn(Action):
    def __init__(self, angle):
        self.angle = angle

    def process_action(self):
        #Pepper API calls go here
        session1 = qi.Session()
        session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
        posture_service1 = session1.service("ALRobotPosture")
        motion_service1 = session1.service("ALMotion")
        print("moving left")
        posture_service1.goToPosture("Stand", 0.5)
        rounds = float(0.5)
        turns = rounds * 0.5 * 3.14
        time = rounds * 2.0
        motion_service1.moveTo(0.0, 0.0, float(self.angle), time)
        return "Success", 200
# ----------------------------------------------------------------------------------------------------------------------#
class Sequence(Action):
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def process_action(self):
        session1 = qi.Session()
        session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
        return "Success", 200
        #Pepper API calls go here
# ----------------------------------------------------------------------------------------------------------------------#
class MediaDisplay(Action):
	def __init__(self, name, file_type):
		self.name = name
		self.file_type = file_type

	def process_action(self):
		print("Media Display")
		session1 = qi.Session()
		session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
		tabletService = session1.service("ALTabletService")

		if (str(self.file_type) == 'jpg'):
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			json_url = os.path.join(SITE_ROOT, 'static', 'images.json')
			data = json.load(open(json_url))
			url = str(data[str(self.name)])
		else:
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			json_url = os.path.join(SITE_ROOT, 'static', 'videos.json')
			data = json.load(open(json_url))
			url = str(data[str(self.name)])

		print(url)
		if (str(self.file_type) == 'jpg'):
			tabletService.showImage(url)
		else:
			tabletService.playVideo(url)
		return "Success", 200
# Pepper API calls go here
# ----------------------------------------------------------------------------------------------------------------------#