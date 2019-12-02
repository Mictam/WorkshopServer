import Queue
import time
import qi


'''session = qi.Session()
session.connect("tcp://{}:{}".format("192.168.1.102", 9559))

tts = session.service("ALTextToSpeech")
tts.setLanguage("Polish")'''

class Action:
	def __init__(self, type, command, text='', volume = '', speed = '', language = ''):
		self.type = type
		self.command = command
		self.text = text
		self.speed = speed
		self.volume = volume
		self.language = language

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
			'''posture_service = session.service("ALRobotPosture")
			motion_service = session.service("ALMotion")'''

			print("moving right")
			#posture_service.goToPosture("Stand", 0.5)
			rounds = float(0.5)
			turns = rounds * 0.5 * 3.14
			time = rounds * 2.0
		'''	motion_service.moveTo(0.0, 0.0, -turns, time)'''

		if (self.command == 'turn_left'):
			'''posture_service = session.service("ALRobotPosture")
			motion_service = session.service("ALMotion")'''
			print("moving left")
			# posture_service.goToPosture("Stand", 0.5)
			rounds = float(0.5)
			turns = rounds * 0.5 * 3.14
			time = rounds * 2.0
			'''motion_service.moveTo(0.0, 0.0, turns, time)'''

		if (self.command == 'move_forward'):
			'''posture_service = session.service("ALRobotPosture")
			motion_service = session.service("ALMotion")'''
		   	print("moving forward")
     			'''posture_service.goToPosture("Stand", 0.5)'''
			rounds = float(0.5)
			turns = rounds * 0.5 * 3.14
			time = rounds * 2.0
			'''		motion_service.moveTo(1.0, 0, 0, time)'''

		"""tabletService = session.service("ALTabletService")
				 tabletService.showImage("https://drive.google.com/file/d/0BzOaFM8N-iwkQzBidXNJWjVEOHc/view?fbclid=IwAR0RxdKm42SLZ_WRzSd9xiZz9kAq_tnIHo0i-ZRDDrex8Wuww8oYr1dZwfk")
				 tabletService.hideImage()
				 time.sleep(5)"""
		if (self.command == 'move_back'):
			'''posture_service = session.service("ALRobotPosture")
			motion_service = session.service("ALMotion")'''
			print("moving backward")
			'''posture_service.goToPosture("Stand", 0.5)'''
			rounds = float(0.5)
			turns = rounds * 0.5 * 3.14
			time = rounds * 2.0
			'''motion_service.moveTo(-1.0, 0, 0, time)'''


	def process_animation(self):
		print("animating")


	def process_speech(self):
		print("saying: ")
		'''tts.setVoice("naoenu")
		tts.setLanguage(self.language)
		tts.setVolume(self.volume)
		tts.setParameter("speed", self.speed)
		tts.say(self.text)'''
		print("end")


class __Queue:

	def __init__(self):
		self.q = Queue.Queue()

	def add_to_queue(self,  action):
		self.q.put(action)
		return self.q

	def get_queue(self):
		for elem in list(self.q.queue):
			print(elem.get_command())

	def clear_queue(self):
		with self.q.mutex:
			self.q.queue.clear()

	def is_empty(self):
		if(self.q.empty()):
			return True
		else:
			return False

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
