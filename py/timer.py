import time

class Timer(object):
	def __init__(self,times):
		# self.times = times
		self.start_time = time.time()
		self.end_time = self.start_time + times

	def __bool__(self):
		# not overtime
		if self.end_time > time.time():
			return False
		else:
			# overtime
			return True


if __name__ == '__main__':
	timer = Timer(5)
	print(timer)
	while not timer:
		time.sleep(1)
