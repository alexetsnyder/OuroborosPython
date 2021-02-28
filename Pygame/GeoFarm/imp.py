#imp.py

def singleton(cls):	
	class SingletonWrapper (cls):
		def __init__(self):
			self.cls = cls
			self.instance = None

		def __call__(self, *args, **kargs):
			if self.instance == None:
				self.instance = self.cls(*args, **kargs)
			return self.instance
	return SingletonWrapper()

@singleton
class IMP:
	def __init__(self):
		self.debug = False
		self.config = None
		self.event_dispatcher = None
		self.render_objects = []

	def init(self, config, event_dispatcher, debug=False):
		self.debug = debug
		self.config = config
		self.event_dispatcher = event_dispatcher
		return self

	def register(self, objs):
		for obj in objs:
			self.render_objects.append(obj)

	def get_objects(self):
		return self.render_objects

	def add_listener(self, delegate):
		self.event_dispatcher.add_listener(delegate)

	def dispatch(self, event):
		self.event_dispatcher.dispatch(event)

if __name__=='__main__':
	pass