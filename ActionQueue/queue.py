import Queue
import time
import qi


session = qi.Session()
session.connect("tcp://{}:{}".format("192.168.1.102", 9559))

tts = session.service("ALTextToSpeech")
tts.setLanguage("Polish")

class Action:
	def __init__(self, type, command, text='', volume = '', speed = ''):
		self.type = type
		self.command = command
		self.text = text
		self.speed = speed
		self.volume = volume

	def get_type(self):
		return self.type

	def get_command(self):
		return self.command

	def get_text(self):
		return self.text

	def process_action(self):
		if( self.type == 'generic' ):
			self.process_generic()
		if( self.type == 'animation' ):
			self.process_animation()
		if( self.type == 'speech'):
			self.process_speech()

	def process_generic(self):
		if( self.command == 'turn_right'):
			posture_service = session.service("ALRobotPosture")
			motion_service = session.service("ALMotion")

			print("moving right")
			"""navigation_service = session.service("ALNavigation")
			motion_service = session.service("ALMotion")
			navigationProxy = session.service("ALNavigationProxy")
			motion_service.wakeUp()
			posture_service.goToPosture("StandInit", 1.0)
			x = 0.2
			y = 0.2
			theta = 0.0
			motion_service.moveTo(x, y, theta)
			navigationProxy.navigateTo(0.2, 0.0)"""
			posture_service.goToPosture("Stand", 0.5)
			rounds = float(0.5)
			turns = rounds * 1.0 * 3.14
			time = rounds * 8.0
			motion_service.moveTo(0.0, 0.0, 1, 4)

		if (self.command == 'turn_left'):
			print("moving left")
		if (self.command == 'move_forward'):
			print("moving forward")
		if (self.command == 'move_back'):
			print("moving backward")

	def process_animation(self):
		print("animating")

	def process_speech(self):
		print("saying: ")
		print(self.text)
		tts.setVoice("naoenu")
		tts.setLanguage("Polish")
		tts.setVolume(self.volume)
		tts.setParameter("speed", self.speed)
		tts.say(self.text)


class __Queue:

	def __init__(self):
		self.q = Queue.Queue()

	def add_to_queue(self,  action):
		self.q.put(action)
		return self.q

	def get_queue(self):
		for elem in list(self.q.queue):
			print(elem.get_command())

	def queue_listener(self):
		while True:
			time.sleep(1)
			print('tasks in queue: ')
			print(self.q.qsize())
			print('currently processed request: ')
			self.get_queue()
			item = self.q.get()
			item.process_action()
			self.q.task_done()
			print("action end")
