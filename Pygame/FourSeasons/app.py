#app.py
import pygame
from four_seasons import *

def debug_print(**kargs):
	print(', '.join(['{0}: {1}'.format(key, value) for key, value in kargs.items()]))

class App:
	WINDOW_SIZE = (640, 400)

	def __init__(self):
		pygame.init()
		self.running = True
		self.size = App.WINDOW_SIZE
		self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)
		self.card_table = CardTable((0, 0), self.size)

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self.running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.running = False
			elif event.key == pygame.K_f:
				self.card_table.flip_cards()
			elif event.key == pygame.K_r:
				self.card_table.new_shuffle()
		elif event.type == pygame.VIDEORESIZE:
			self.size = (event.w, event.h)
			self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)
			self.card_table.on_resize((0, 0), self.size)
		elif event.type == pygame.MOUSEBUTTONUP:
			self.card_table.on_mouse_button_up(event)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.card_table.on_mouse_button_down(event)
		elif event.type == pygame.MOUSEMOTION:
			self.card_table.on_mouse_move(event)

	def update(self):
		self.card_table.update()

	def draw(self):
		self.surface.fill(Color.TEAL_FELT)
		self.card_table.draw(self.surface)
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