#imp.py
import pygame

def singleton_decorator(cls):	
	class SingletonWrapper (cls):
		def __init__(self):
			self.cls = cls
			self.instance = None

		def __call__(self, *args, **kargs):
			if self.instance == None:
				self.instance = self.cls(*args, **kargs)
			return self.instance
	return SingletonWrapper()

@singleton_decorator
class IMP:
	def __init__(self, debug=False):
		self.running = True
		self.debug = debug
		self.config = None
		self.screen = None
		self.event_dispatcher = None

	def init(self, screen, config, event_dispatcher):
		self.screen = screen
		self.config = config
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