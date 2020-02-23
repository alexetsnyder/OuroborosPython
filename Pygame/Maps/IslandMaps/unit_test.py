#unit_test.py
import pygame
import traceback
import imp, events
from structs import *
from pygame import freetype

WINDOW_SIZE = (640, 400)

class Screen:
	def __init__(self, size):
		self.w, self.h = self.size = size
		self.surface = pygame.display.set_mode(size, pygame.RESIZABLE)
		pygame.display.set_caption('Unit Test')

	def wire_events(self):
		imp.IMP().add_listener(events.WindowResizedEvent().listen(self.on_resize))

	def on_resize(self, event):
		self.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

	def fill(self, color=Color.BLACK):
		self.surface.fill(color)

	def flip(self):
		pygame.display.flip()

class UnitTest:
	def __init__(self, window_size=WINDOW_SIZE):
		pygame.init()
		self.success = True
		imp.IMP().init(Screen(window_size), None, events.EventDispatcher(), True)

	def register(self, objects):
		for obj in objects:
			imp.IMP().register(obj)

	def update(self):
		imp.IMP().update()

	def draw(self):
		imp.IMP().screen.fill(Color.TEAL_FELT)
		imp.IMP().draw()
		imp.IMP().screen.flip()

	def run(self):
		try:
			while imp.IMP().running:
				for event in pygame.event.get():
					imp.IMP().dispatch(event)
				self.update()
				self.draw()
		except Exception as ex:
			self.success = False
			print('Exception: {}'.format(ex))
			traceback.print_exc()
		finally:
			self.free()

	def free(self):
		pygame.quit()

if __name__=='__main__':
	pass