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
		self.running = True
		self.debug = False
		self.config = None
		self.screen = None
		self.actions = None
		self.event_dispatcher = None

	def init(self, screen, config, event_dispatcher, actions, debug=False):
		self.debug = debug
		self.screen = screen
		self.config = config
		self.actions = actions
		self.event_dispatcher = event_dispatcher
		self.wire_events()

	def wire_events(self):
		self.screen.wire_events()

	def add_delegate(self, delegate):
		self.event_dispatcher += delegate

	def remove_delegate(self, delegate):
		self.event_dispatcher -= delegate

	def on_event(self, event):
		self.event_dispatcher.invoke(event)

	def quit(self):
		self.running = False

if __name__=='__main__':
	pass