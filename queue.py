import Queue
import time

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
