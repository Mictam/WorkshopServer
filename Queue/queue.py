from queue import Queue
import time


class __Queue:

	q = Queue()

	def __init__(self):
		self.q = Queue()

	def add_to_queue(self, move):
		self.q.put(move)
		return self.q

	def get_queue(self):
		return list(self.q.queue)

	def queue_listener(self):
		while True:
			print('tasks in queue: ')
			print(self.q.qsize())
			print('currently processed request: ')
			print(self.q.get())
			time.sleep(3)