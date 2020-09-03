#imp.py
import style, events

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
		self.render_objects = []
		self.styles = style.Styles()

	def init(self, screen, config, event_dispatcher, debug=False):
		self.debug = debug
		self.screen = screen
		self.config = config
		self.event_dispatcher = event_dispatcher
		self.wire_events()

	def wire_events(self):
		self.screen.wire_events()
		self.event_dispatcher += events.QuitEvent().create(self.on_quit)

	def on_quit(self, event):
		self.running = False

	def register(self, obj):
		self.render_objects.append(obj)

	def add_listener(self, delegate):
		self.event_dispatcher += delegate

	def remove_listener(self, delegate):
		self.event_dispatcher -= delegate

	def dispatch(self, event):
		self.event_dispatcher.invoke(event)

	def update(self):
		for obj in self.render_objects:
			obj.update()

	def draw(self):
		for obj in self.render_objects:
			obj.draw(self.screen.surface)

if __name__=='__main__':
	pass