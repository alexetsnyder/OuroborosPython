#game.py
import pygame, time
import events, imp, go
import four_seasons as fs
from config import Config
from structs import *

class Screen:
	def __init__(self, size):
		self.set_size(size)
		self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)

	def wire_events(self):
		imp.IMP().add_delegate(events.WindowResizeEvent().create(self.on_resize))

	def on_resize(self, event):
		self.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

	def set_size(self, size):
		self.w, self.h = self.size = size 

	def fill(self, color=Color.BLACK):
		self.surface.fill(color)

	def flip(self):
		pygame.display.flip()

class Game:
	def __init__(self):
		pygame.init()
		self.elapsed = 1
		self.previous = None
		self.is_paused = False
		self.SEC_PER_FRAME = 1 / 60
		self.card_table = fs.CardTable((0, 0), imp.IMP().screen.size)
		self.frame_rate_func = lambda n : '{:.2f}'.format(n)
		self.frame_rate_text = go.RenderText(self.frame_rate_func(0.00))
		self.pause_text = go.RenderText('Paused', False, (0, 0), go.FontInfo(60, Color.BLUE))
		self.pause_text.center_on(tuple(x // 2 for x in imp.IMP().screen.size))
		self.wire_events()	

	def wire_events(self):
		imp.IMP().add_delegate(events.QuitEvent().create(self.on_quit))
		imp.IMP().add_delegate(events.WindowResizeEvent().create(self.on_resize))
		imp.IMP().add_delegate(events.KeyDownEvent(pygame.K_ESCAPE).create(self.on_pause))

	def start(self):
		self.is_paused = False
		self.previous = time.time()

	def on_quit(self, event):
		imp.IMP().quit()

	def on_resize(self, event):
		self.pause_text.center_on((event.w // 2, event.h // 2))

	def on_pause(self, event):
		self.is_paused = not self.is_paused
		self.pause_text.set_visibility(self.is_paused)
		self.frame_rate_text.set_visibility(not self.is_paused)
		if not self.is_paused:
			self.previous = time.time()

	def tick(self):
		current = time.time()
		self.elapsed = (current - self.previous)
		if self.SEC_PER_FRAME > self.elapsed:
			time.sleep(self.SEC_PER_FRAME - self.elapsed)
			self.elapsed += self.SEC_PER_FRAME - self.elapsed
		self.previous = current
		
	def update(self):
		frame_rate_str = self.frame_rate_func(1 / self.elapsed)
		self.frame_rate_text.set_text(frame_rate_str)
		self.frame_rate_text.update()
		self.card_table.update()

	def draw(self):
		imp.IMP().screen.fill(Color.TEAL_FELT)
		self.frame_rate_text.draw(imp.IMP().screen.surface)
		self.card_table.draw(imp.IMP().screen.surface)
		self.pause_text.draw(imp.IMP().screen.surface)
		imp.IMP().screen.flip()

	def free(self):
		pygame.quit()

	def round_up(self, n):
		int_n = int(n)
		mod_10 = int_n % 10
		if not mod_10 == 0:
			int_n += (10 - mod_10)
		return int_n

	def run(self):
		self.start()
		while imp.IMP().running:
			for event in pygame.event.get():
				imp.IMP().on_event(event)
			self.game()
			self.draw()
		self.free()

	def game(self):
		if not self.is_paused:
			self.update()
			self.tick()	

if __name__=='__main__':
	config = Config('data_file.txt')
	event_dispatcher = events.EventDispatcher()
	screen = Screen(config.try_get('WINDOW_SIZE', (640, 400)))
	debug = config.try_get('DEBUG', False)
	imp.IMP().init(screen, config, event_dispatcher, debug)
	game = Game()
	game.run()
