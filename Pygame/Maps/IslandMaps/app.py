#app.py
import pygame, maps
import imp, go, events, config
from pygame import freetype
from structs import *

class Screen:
	def __init__(self, size):
		self.set_size(size)
		self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)

	def wire_events(self):
		imp.IMP().add_listener(events.WindowResizedEvent().create(self.on_resize))

	def on_resize(self, event):
		self.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

	def set_size(self, size):
		self.w, self.h = self.size = size 

	def set_title(self, title):
		pygame.display.set_caption(title)

	def fill(self, color=Color.BLACK):
		self.surface.fill(color)

	def flip(self):
		pygame.display.flip()

class App:
	def __init__(self):
		pygame.init()
		size = imp.IMP().screen.size 
		self.island = maps.IslandMap((0, 0), size, 300, (10, 10))
		self.line_map = maps.LineMap((0, 0), size, 300)
		self.register([self.island, self.line_map])
		self.wire_events()

	def register(self, objects):
		for obj in objects:
			imp.IMP().register(obj)

	def wire_events(self):
		imp.IMP().add_listener(events.WindowResizedEvent().create(self.on_resize))

	def on_resize(self, event):
		size = event.w, event.h
		self.island.refresh(size)
		self.line_map.refresh(size)

	def update(self):
		pass

	def draw(self):
		imp.IMP().screen.fill(Color.BLUE)
		imp.IMP().draw()
		imp.IMP().screen.flip()

	def free(self):
		pygame.quit()

	def run(self):
		while imp.IMP().running:
			for event in pygame.event.get():
				imp.IMP().dispatch(event)
			self.update()
			self.draw()
		self.free()

if __name__=='__main__':
	data = config.Config('data/config_data.txt')
	screen = Screen((1280, 800))
	event_dispatcher = events.EventDispatcher()
	imp.IMP().init(screen, data, event_dispatcher, data.try_get('DEBUG', False))
	app = App()
	app.run()