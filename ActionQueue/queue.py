import Queue
import time
import qi


session = qi.Session()
session.connect("tcp://{}:{}".format("192.168.1.102", 9559))

tts = session.service("ALTextToSpeech")
tts.setLanguage("Polish")

class Action:
	def __init__(self, type, command, text=''):
		self.type = type
		self.command = command
		self.text = text

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
			print("moving right")
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
