#app.py
import pygame
import geo, imp, events 
from general import Color

class App:
	WINDOW_SIZE = (640, 400)

	def __init__(self):
		pygame.init()
		self.running = True
		self.size = App.WINDOW_SIZE
		self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)
		self.text = geo.RenderText('Hello World!')
		self.rect = geo.Rect((10, 10), (20, 20), Color.RED)
		imp.IMP().register(self.text)
		imp.IMP().register(self.rect)
		imp.IMP().event_dispatcher = events.EventDispatcher()
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_listener(events.QuitEvent().create(self.on_quit))
		imp.IMP().add_listener(events.VideoResizeEvent().create(self.on_resize)) 
		imp.IMP().add_listener(events.VideoResizeEvent().create(lambda event : self.text.center_on((event.w / 2, event.h / 2))))

	def on_quit(self, event):
		self.running = False

	def on_resize(self, event):
		self.size = (event.w, event.h)
		self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)

	def on_event(self, event):
		imp.IMP().dispatch(event);

	def update(self):
		pass

	def draw(self):
		self.surface.fill(Color.BLACK)
		for obj in imp.IMP().get_objects():
			obj.draw_to(self.surface)
		pygame.display.flip()

	def free(self):
		pygame.quit()

	def run(self):
		while self.running:
			for event in pygame.event.get():
				self.on_event(event)
			self.update()
			self.draw()
		self.free()

if __name__=='__main__':
	app = App()
	app.run()