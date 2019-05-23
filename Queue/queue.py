from queue import Queue


class __Queue:

	q = Queue()

	def __init__(self):
		self.q = Queue()

	def add_to_queue(self, move):
		self.q.put(move)
		return self.q

	def get_queue(self):
		return list(self.q.queue)