#game.py
import controls
import pygame, time
import events, imp, go, cards
from structs import *

#ToDo:
# 2) Timer.
# 3) Score.
# 5) Only winable hands.
# 6) One list to draw everything.
# 8) At Zero cards text and deck picture disappear
# 9) Debug Print.
#10) Put data in data file.

class Screen:
	def __init__(self, size):
		self.set_size(size)
		self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)

	def wire_events(self):
		imp.IMP().add_delegate(events.WindowResizedEvent().listen(self.on_resize))

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
		self.w, self.h = self.size = imp.IMP().screen.size
		self.elapsed = 1
		self.is_win = False
		self.previous = None
		self.is_paused = True
		self.SEC_PER_FRAME = 1 / 60
		self.center = tuple(x // 2 for x in self.size)
		self.title = imp.IMP().config.try_get('GAME_NAME', 'Default Name')
		self.card_table = cards.CardTable((0, 0), self.size, margins=imp.IMP().config.try_get('CARD_TABLE_MARGINS', (0, 0)))
		self.pause_text = go.RenderText('Paused!', font_info=go.FontInfo(60, Color.BLUE), is_visible=False)
		self.pause_text.center_on(self.center)
		self.create_side_bar()
		self.wire_events()
		self.set_title()	

	def wire_events(self):
		imp.IMP().add_delegate(events.QuitEvent().listen(self.on_quit))
		imp.IMP().add_delegate(events.WindowResizedEvent().listen(self.on_resize))
		imp.IMP().add_delegate(events.KeyDownEvent(pygame.K_ESCAPE).listen(self.on_pause))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.GAME_OVER).listen(self.on_game_over))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.UNDO_STACK_CLEARED).listen(self.on_redo_undo_changed))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.REDO_STACK_CLEARED).listen(self.on_redo_undo_changed))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.UNDO_ENABLED).listen(self.on_redo_undo_changed))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.REDO_ENABLED).listen(self.on_redo_undo_changed))

	def create_side_bar(self):
		buttons = []
		self.restart_btn = controls.Button('Restart', self.restart)
		self.new_game_btn = controls.Button('New Game', self.new_game)
		self.undo_btn = controls.Button('Undo', self.undo)
		self.redo_btn = controls.Button('Redo', self.redo)
		self.pause_btn = controls.Button('Pause', self.on_pause)
		self.restart_btn.set_enabled(False)
		self.undo_btn.set_enabled(False)
		self.redo_btn.set_enabled(False)
		self.pause_btn.set_enabled(False)
		buttons.append(self.restart_btn)
		buttons.append(self.new_game_btn)
		buttons.append(self.undo_btn)
		buttons.append(self.redo_btn)
		buttons.append(self.pause_btn)
		self.side_bar = controls.SideBar(self.h, controls=buttons)

	def new_game(self, event):
		self.un_pause()
		self.card_table.new_deal()
		self.restart_btn.set_enabled(True)
		self.pause_btn.set_enabled(True)

	def restart(self, event):
		self.un_pause()
		self.card_table.restart()

	def undo(self, event):
		imp.IMP().actions.undo()
		self.toggle_undo_redo()

	def redo(self, event):
		imp.IMP().actions.redo()
		self.toggle_undo_redo()
		
	def toggle_undo_redo(self):
		self.toggle_undo()
		self.toggle_redo()

	def toggle_undo(self):
		is_enabled = False
		if imp.IMP().actions.can_undo():
			is_enabled = True
		self.undo_btn.set_enabled(is_enabled)

	def toggle_redo(self):
		is_enabled = False
		if imp.IMP().actions.can_redo():
			is_enabled = True
		self.redo_btn.set_enabled(is_enabled)

	def set_title(self):
		imp.IMP().screen.set_title(self.title)

	def start(self):
		self.is_paused = True
		self.previous = time.time()

	def on_quit(self, event):
		imp.IMP().quit()

	def on_resize(self, event):
		self.center = (event.w // 2, event.h // 2)
		self.pause_text.center_on(self.center)

	def on_pause(self, event):
		self.pause()

	def on_game_over(self, event):
		imp.IMP().actions.clear()
		self.pause_text.set_text('Winner!')
		self.pause_text.center_on(self.center)
		self.pause_btn.set_enabled(False)
		self.pause()

	def on_redo_undo_changed(self, event):
		self.toggle_undo_redo()

	def pause(self):
		events.UserEvent(CustomEvent.PAUSE).post()
		self.is_paused = not self.is_paused
		self.pause_text.set_visibility(self.is_paused)
		if not self.is_paused:
			self.previous = time.time()

	def un_pause(self):
		self.pause_text.set_text('Paused!')
		self.pause_text.center_on(self.center)
		if self.is_paused:
			self.pause()

	def tick(self):
		current = time.time()
		self.elapsed = (current - self.previous)
		if self.SEC_PER_FRAME > self.elapsed:
			time.sleep(self.SEC_PER_FRAME - self.elapsed)
			self.elapsed += self.SEC_PER_FRAME - self.elapsed
		self.previous = current

	def update(self):
		self.card_table.update()
		self.side_bar.update()

	def draw(self):
		screen = imp.IMP().screen 
		screen.fill(Color.TEAL_FELT)
		self.card_table.draw(screen.surface)
		self.pause_text.draw(screen.surface)
		self.side_bar.draw(screen.surface)
		screen.flip()

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
	import acts
	from config import Config 

	actions = acts.UndoActions()
	config = Config('data_file.txt')
	event_dispatcher = events.EventDispatcher()
	screen = Screen(config.try_get('WINDOW_SIZE', (640, 400)))
	debug = config.try_get('DEBUG', False)
	imp.IMP().init(screen, config, event_dispatcher, actions, debug)

	game = Game()
	game.run()
