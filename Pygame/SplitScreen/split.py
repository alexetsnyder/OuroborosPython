#split.py
import pygame
from pygame import freetype

class Color:
	WHITE  		  = (255, 255, 255)
	BLACK  		  = (  0,   0,   0)
	RED           = (255,   0,   0)
	GREEN  		  = (  0, 255,   0)
	SEA_GREEN     = ( 46, 139,  87)
	FOREST_GREEN  = ( 13,  55,  13)
	BLUE   		  = (  0,   0, 255)
	DEEP_SKY_BLUE = (  0, 191, 255)
	YELLOW 		  = (255, 255,   0)
	SAND          = ( 76,  70,  50)
	SILVER 		  = (192, 192, 192)

class WinOr:
	VERTICAL   = 0
	HORIZONTAL = 1

class FontInfo:
	def __init__(self, font_size=20, font_color=Color.SILVER, font_name='lucidaconsole'):
		self.font_name = font_name
		self.font_size = font_size
		self.font_color = font_color

class RenderText:
	def __init__(self, text_str, position=(0,0), font_info=FontInfo()):
		self.text_str = text_str
		self.font_info = font_info
		self.x, self.y = self.position = position
		self.font = freetype.SysFont(self.font_info.font_name, self.font_info.font_size)
		self.w, self.h = self.size = self.text_size(self.text_str)

	def set_position(self, position):
		self.x, self.y = self.position = position

	def set_text(self, text_str):
		self.text_str = text_str
		return self.get_size()

	def is_selected(self, position):
		x1, y1 = position
		return ((self.w / 2) ** 2 >= (self.x - x1) ** 2) and ((self.h / 2) ** 2 >= (self.y - y1) ** 2)

	def get_size(self):
		self.w, self.h = self.size = self.text_size(self.text_str)
		return self.size

	def text_size(self, text_str):
		return self.font.get_rect(text_str).size 

	def get_corner_pos(self):
		return (self.x - self.w / 2, self.y - self.h / 2)

	def adjustment_value(self):
		if self.x < 0:
			return self.w + self.x
		return 0

	def clip_text(self):
		adj = self.adjustment_value()
		print('adj', adj)
		if adj > 0:
			temp_str_list = [c for c in self.text_str]
			while self.text_size(''.join(temp_str_list))[0] > adj:
				temp_str_list.pop(0)
			print(''.join(temp_str_list))
			return ''.join(temp_str_list)
		return self.text_str

	def draw_to(self, surface):
		self.font.render_to(surface, self.get_corner_pos(), self.clip_text(), self.font_info.font_color)

def post_event(**kargs):
	event = pygame.event.Event(pygame.USEREVENT, **kargs)
	pygame.event.post(event)

class Surface:
	ID = 0

	def __init__(self, surface, corner_pos):
		self.id = Surface.ID
		self.surface = surface
		self.x, self.y = self.corner_pos = corner_pos
		self.w, self.h = self.size = self.surface.get_size()
		Surface.ID += 1

	def is_selected(self, position):
		x1, y1 = position
		x2, y2 = self.get_center()
		return ((self.w / 2) ** 2 >= (x2 - x1) ** 2) and ((self.h / 2) ** 2 >= (y2 - y1) ** 2)

	def surface_to_screen_pos(self, position):
		x, y = position
		return (x + self.x, y + self.y)

	def screen_to_surface_pos(self, position):
		x, y = position
		return (x - self.x, y - self.y)

	def reset(val):
		Surface.ID = val

	def set_size(self, size):
		self.w, self.h = self.size = size 

	def set_corner_pos(self, corner_pos):
		self.x, self.y = self.corner_pos = corner_pos

	def get_center(self):
		return (self.x + self.w / 2, self.y + self.h / 2)

	def clear(self, color=Color.BLACK):
		self.surface.fill(color)

	def blit(self, surface):
		surface.blit(self.surface, self.corner_pos)

class Screen (Surface):
	def __init__(self, size):
		surface = pygame.display.set_mode(size, pygame.RESIZABLE)
		super().__init__(surface, (0, 0))

	def flip(self):
		pygame.display.flip()

class Pane (Surface):
	def __init__(self, corner_pos, size):
		super().__init__(pygame.Surface(size), corner_pos)

class UserEvents:
	WINDOW_RESIZE       = 0
	ACTIVE_PANE_CHANGED = 1

class SplitPane:
	def __init__(self, docks, win_or, size, spans=[]):
		self.panes = []
		self.docks = docks 
		self.spans = spans
		self.win_or = win_or
		self.screen = Screen(size)
		self.w, self.h = self.size = size
		self.create_panes() 
		self.look_up_panes = {pane.id : pane for pane in self.panes}

	def in_pane(self, position):
		for pane in self.panes:
			x, y = pane.corner_pos
			right_corner_pos = (x + pane.w, y)
			print('corner_pos:', pane.corner_pos, 'right_corner_pos:', right_corner_pos)
			print('position:', position)
			#pane_pos = pane.surface_to_screen_pos(position)
			pane_pos = position
			print('pane_pos:', pane_pos)
			if pane.is_selected(pane_pos):
				print('pane.id:', pane.id)
				return pane.id
		return -1

	def screen_to_surface_pos(self, id, position):
		if id > 0 and id <= len(self.panes):
			return self.look_up_panes[id].screen_to_surface_pos(position)
		return position

	def get_pane_size(self, id = 1):
		if id > 0 and id <= len(self.panes):
			return self.panes[id-1].size
		return self.panes[0].size

	def set_size(self, size):
		self.w, self.h = self.size = size 

	def get_ids(self):
		return [pane.id for pane in self.panes]

	def on_resize(self, event):
		self.set_size((event.w, event.h))
		self.screen = Screen(self.size)
		self.refill()
		print((event.w, event.h), self.get_pane_size())
		post_event(name=UserEvents.WINDOW_RESIZE)

	def toggle_or(self):
		if self.win_or == WinOr.VERTICAL:
			self.win_or = WinOr.HORIZONTAL
		else:
			self.win_or = WinOr.VERTICAL
		self.refill()

	def increment(self):
		if any(self.spans):
			self.spans.append(1)
		self.docks += 1
		self.refill()

	def decrement(self):
		if self.docks > 1:
			if any(self.spans):
				n = self.spans.pop()
				if n > 1:
					n -= 1
					self.spans.append(n)
			self.docks -= 1
			self.refill()

	def refill(self):
		Surface.reset(1)
		self.panes = []
		self.create_panes()
		self.look_up_panes = {pane.id : pane for pane in self.panes}
		post_event(name=UserEvents.WINDOW_RESIZE)

	def create_panes(self):
		x, y = (0, 0)
		w, h = self.init_size()
		if any(self.spans):
			for span in self.spans:
				self.panes.append(Pane((x, y), self.span_size(w, h, span)))
				for i in range(span):
					x, y = self.next_corner(x, y, w, h)
		else:
			for i in range(self.docks):	
				self.panes.append(Pane((x, y), (w, h)))
				x, y = self.next_corner(x, y, w, h)

	def init_size(self):
		if self.win_or == WinOr.VERTICAL:
			return (self.w / self.docks, self.h)
		else:
			return (self.w, self.h / self.docks)

	def next_corner(self, x, y, w, h):
		if self.win_or == WinOr.VERTICAL:
			return (x + w, y)
		else:
			return (x, y + h)

	def span_size(self, w, h, span):
		if self.win_or == WinOr.VERTICAL:
			return (span * w, h)
		else:
			return (w, span * h)

	def clear_panes(self, color=Color.BLACK):
		for pane in self.panes:
			pane.clear(color)

	def draw_to(self, id, object):
		if id in self.look_up_panes:
			object.draw_to(self.look_up_panes[id].surface)

	def draw(self):
		self.screen.clear()
		for pane in self.panes:
			pane.blit(self.screen.surface)
			pygame.draw.rect(self.screen.surface, Color.RED, pygame.Rect(pane.corner_pos, pane.size), 1)
		self.clear_panes()
		self.screen.flip()

class App:
	WINDOW_SIZE = (640, 400)
	NUMBER_KEYS_TO_NUMBER = {
		pygame.K_1 : 1,
		pygame.K_2 : 2,
		pygame.K_3 : 3,
		pygame.K_4 : 4,
		pygame.K_5 : 5,
		pygame.K_6 : 6,
		pygame.K_7 : 7,
		pygame.K_8 : 8,
		pygame.K_9 : 9,
		pygame.K_0 : 0
	}

	def __init__(self):
		pygame.init()
		self.running = True
		self.size = App.WINDOW_SIZE
		self.split_pane = SplitPane(3, WinOr.VERTICAL, self.size, [1, 2])
		self.text = RenderText('Hello World!')
		self.is_dragging = False
		self.id = 1

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self.running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.running = False
			elif event.key == pygame.K_EQUALS:
				self.split_pane.increment()
			elif event.key == pygame.K_MINUS:
				self.split_pane.decrement()
			elif event.key == pygame.K_t:
				self.split_pane.toggle_or()
			else:
				if event.key in App.NUMBER_KEYS_TO_NUMBER:
					self.id = App.NUMBER_KEYS_TO_NUMBER[event.key]
					post_event(name=UserEvents.ACTIVE_PANE_CHANGED)
					print('id: {0}, pane size: {1}'.format(self.id, self.split_pane.get_pane_size(self.id)))
		elif event.type == pygame.VIDEORESIZE:
			self.size = (event.w, event.h)
			self.split_pane.on_resize(event)
			#self.text.set_position(tuple(x // 2 for x in self.split_pane.get_pane_size()))
		elif event.type == pygame.MOUSEMOTION:
			if self.is_dragging:
				pane_pos = self.split_pane.screen_to_surface_pos(self.id, event.pos)
				self.text.set_position(pane_pos)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pane_pos = self.split_pane.screen_to_surface_pos(self.id, event.pos)
			if self.text.is_selected(pane_pos):
				self.is_dragging = True
		elif event.type == pygame.MOUSEBUTTONUP:
			self.is_dragging = False
			temp_id = self.split_pane.in_pane(event.pos)
			if temp_id > 0:
				self.id = temp_id
				#post_event(name=UserEvents.ACTIVE_PANE_CHANGED)
			self.text.set_position(self.split_pane.screen_to_surface_pos(self.id, event.pos))
		elif event.type == pygame.USEREVENT:
			if event.name in [UserEvents.WINDOW_RESIZE, UserEvents.ACTIVE_PANE_CHANGED]:
				#self.text.set_position(tuple(x // 2 for x in event.pane_size))
				#print('id: {0}, pane size: {1}'.format(self.id, self.split_pane.get_pane_size(self.id)))
				self.text.set_position(tuple(x // 2 for x in self.split_pane.get_pane_size(self.id)))

	def update(self):
		pass

	def draw(self):
		self.split_pane.draw_to(self.id, self.text)
		self.split_pane.draw()

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