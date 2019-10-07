from queue import Queue
import time


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




class __Queue:

	q = Queue()

	def __init__(self):
		self.q = Queue()

	def add_to_queue(self,  action):
		self.q.put(action)
		return self.q

	def get_queue(self):
		return list(self.q.queue)

	def queue_listener(self):
		while True:
			print('tasks in queue: ')
			print(self.q.qsize())
			print('currently processed request: ')
			self.q.get().process_action()
			print("action end")

			print(self.q.get().get_type())

			time.sleep(3)