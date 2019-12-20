#game.py
import pygame, time
import events, imp, go, trans
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

	def set_title(self, title):
		pygame.display.set_caption(title)

	def fill(self, color=Color.BLACK):
		self.surface.fill(color)

	def flip(self):
		pygame.display.flip()

class Game:
	def __init__(self):
		pygame.init()
		self.size = imp.IMP().screen.size
		self.elapsed = 1
		self.is_win = False
		self.previous = None
		self.is_paused = False
		self.SEC_PER_FRAME = 1 / 60
		self.center = tuple(x // 2 for x in self.size)
		self.title = imp.IMP().config.try_get('GAME_NAME', 'Default Name')
		self.card_table = fs.CardTable((0, 0), self.size, margins=imp.IMP().config.try_get('CARD_TABLE_MARGINS', (0, 0)))
		self.pause_text = go.RenderText('Paused!', font_info=go.FontInfo(60, Color.BLUE), is_visible=False)
		self.pause_text.center_on(self.center)
		self.wire_events()
		self.set_title()	

	def wire_events(self):
		imp.IMP().add_delegate(events.QuitEvent().create(self.on_quit))
		imp.IMP().add_delegate(events.WindowResizeEvent().create(self.on_resize))
		imp.IMP().add_delegate(events.KeyDownEvent(pygame.K_ESCAPE).create(self.on_pause))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.GAME_OVER).create(self.on_game_over))
		imp.IMP().add_delegate(events.KeyDownEvent(pygame.K_TAB).create(self.on_undo))
		imp.IMP().add_delegate(events.KeyDownEvent(pygame.K_BACKSPACE).create(self.on_redo))

	def set_title(self):
		imp.IMP().screen.set_title(self.title)

	def start(self):
		self.is_paused = False
		self.previous = time.time()

	def on_quit(self, event):
		imp.IMP().quit()

	def on_resize(self, event):
		self.center = (event.w // 2, event.h // 2)
		self.pause_text.center_on(self.center)

	def on_pause(self, event):
		if self.is_paused and self.is_win:
			self.is_win = False
			self.pause_text.set_text('Paused!')
			self.pause_text.center_on(self.center)
			self.card_table.new_deal()
		self.pause()

	def on_game_over(self, event):
		self.is_win = True
		imp.IMP().actions.clear()
		self.pause_text.set_text('Winner!')
		self.pause_text.center_on(self.center)
		events.KeyDownEvent(pygame.K_ESCAPE).post()

	def on_undo(self, event):
		imp.IMP().actions.undo()

	def on_redo(self, event):
		imp.IMP().actions.redo()

	def pause(self):
		self.is_paused = not self.is_paused
		self.pause_text.set_visibility(self.is_paused)
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
		self.card_table.update()

	def draw(self):
		imp.IMP().screen.fill(Color.TEAL_FELT)
		self.card_table.draw(imp.IMP().screen.surface)
		self.pause_text.draw(imp.IMP().screen.surface)
		imp.IMP().screen.flip()

	def free(self):
		pygame.quit()

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
	actions = trans.UndoActions()
	config = Config('data_file.txt')
	event_dispatcher = events.EventDispatcher()
	screen = Screen(config.try_get('WINDOW_SIZE', (640, 400)))
	debug = config.try_get('DEBUG', False)
	imp.IMP().init(screen, config, event_dispatcher, actions, debug)
	game = Game()
	game.run()
