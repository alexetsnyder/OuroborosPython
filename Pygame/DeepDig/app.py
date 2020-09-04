#app.py
import geo 
import pygame
from general import Color
from pygame import freetype

class App:
	WINDOW_SIZE = (640, 400)

	def __init__(self):
		pygame.init()
		self.running = True
		self.size = App.WINDOW_SIZE
		self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)
		self.text = geo.RenderText('Hello World!')
		self.rect = geo.Rect((10, 10), (20, 20), Color.RED)

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self.running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.running = False
		elif event.type == pygame.VIDEORESIZE:
			self.size = (event.w, event.h)
			self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)
			self.text.center_on(tuple(x // 2 for x in self.size))

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