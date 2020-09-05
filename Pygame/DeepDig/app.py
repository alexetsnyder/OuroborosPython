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
		imp.IMP().event_dispatcher = events.EventDispatcher();
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_listener(events.QuitEvent().create(self.on_quit))
		imp.IMP().add_listener(events.VideoResizeEvent().create(self.on_resize)) 

	def on_quit(self, event):
		self.running = False

	def on_resize(self, event):
		self.size = (event.w, event.h)
		self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)
		self.text.center_on(tuple(x // 2 for x in self.size))

	def on_event(self, event):
		imp.IMP().dispatch(event);

	def update(self):
		pass

	def draw(self):
		self.surface.fill(Color.BLACK)
		self.text.draw_to(self.surface)
		self.rect.draw_to(self.surface);
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