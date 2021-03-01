#HelloWorldResizable.py
import pygame

import imp, events, geo
from enums import Color 

class App:
	WINDOW_SIZE = (640, 400)

	def __init__(self):
		pygame.init()
		self.running = True
		self.size = App.WINDOW_SIZE
		self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)
		self.event_manager = events.EventManager(is_debug=True)
		self.imp = imp.IMP().init(None, self.event_manager, True)
		self.register_objs()
		self.wire_events()

	def register_objs(self):
		self.text = geo.RenderText('Hello World!').center_on(tuple(x // 2 for x in self.size))
		self.rect = geo.Rect(tuple(x // 4 for x in self.size), (20, 20), Color.RED)
		self.imp.register([self.text, self.rect])

	def wire_events(self):
		self.imp.add_listener(events.QuitEvent().create([self.on_quit]))
		self.imp.add_listener(events.VideoResizeEvent().create([self.on_resize]))
		self.imp.add_listener(events.KeyDownEvent().create([self.on_quit]))
		self.imp.add_listener(events.UserEvent(events.UserEvents.UNIT_TEST).create([self.on_unit_test]))
		events.UserEvent(events.UserEvents.UNIT_TEST).post()

	def on_unit_test(self, event):
		pass

	def on_quit(self, event):
		self.running = False

	def on_resize(self, event):
		self.size = (event.w, event.h)
		self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)
		self.text.center_on(tuple(x // 2 for x in self.size))

	def update(self):
		for obj in self.imp.get_objects():
			obj.update()

	def draw(self):
		self.surface.fill(Color.BLACK)
		for obj in self.imp.get_objects():
			obj.draw_to(self.surface)
		pygame.display.flip()

	def free(self):
		pygame.quit()

	def run(self):
		while self.running:
			for event in pygame.event.get():
				self.imp.dispatch(event)
			self.update()
			self.draw()
		self.free()

if __name__=='__main__':
	app = App()
	app.run()