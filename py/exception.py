class ExceptionConnection(Exception):
	def __init__(self,value):
		super(ExceptionConnection,self).__init__(value)
		self.value = value

	def __str__(self):
		return self.value

class EOF(ExceptionConnection):
	'''Raised when EOF is read from a child.
	This usually means the child has exited.'''


class TIMEOUT(ExceptionConnection):
	'''Raised when a read time exceeds the timeout. '''

class PatternError(Exception):
	# def __init__(self,ErrorInfo):
	#	 self.errorinfo=ErrorInfo
	def __str__(self):
		return "pattern only support str and list"