#HelloWorldResizable.py
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

class Vector:
	def __init__(self, *args):
		self.values = {self.get(i) : args[i] for i in range(len(args))}

	def get(self, index):
		return 'v{0}'.format(index)

	def add_range(self, *args):
		for i in range(len(kargs)):
			self.values[self.get(i)] = args[i]

	def length_sqr(self):
		return sum([self.values[key] ** 2 for key in self.values])

	def __str__(self):
		return '({0})'.format(', '.join(['{0}: {1}'.format(key, self.values[key]) for key in self.values]))

	def __getattr__(self, key):
		return self.values[key]

	def __getitem__(self, index):
		return self.values[self.get(index)]

	def __setitem__(self, index, item):
		self.values[self.get(index)] = item

	def __sub__(self, other):
		new_vector = Vector()
		for key in self.values:
			new_vector.values[key] = self.values[key] - other.values[key]
		return new_vector

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
		self.w, self.h = self.size = self.font.get_rect(self.text_str).size 

	def set_position(self, position):
		self.x, self.y = self.position = position

	def set_text(self, text_str):
		self.text_str = text_str
		return self.get_size()

	def get_size(self):
		self.w, self.h = self.size = self.font.get_rect(self.text_str).size 
		return self.size

	def draw_to(self, surface):
		self.font.render_to(surface, (self.x - self.w / 2, self.y - self.h / 2), self.text_str, self.font_info.font_color)

class Suits:
	DIAMONDS = 0
	HEARTS   = 1
	SPADES   = 2
	CLUBS    = 3

# CARD_VALUES = {
# 	 1,
# 	 2,
# 	 3,
# 	 4,
# 	 5,
# 	 6,
# 	 7,
# 	 8,
# 	 9,
# 	10,
# 	11,
# 	12,
# 	13
# }

class Shape:
	def __init__(self, center, size,  color, width=0):
		self.color = color
		self.width = width 
		self.w, self.h = self.size = size
		self.h, self.k = self.center = center  

	def set_center(self, center):
		self.h, self.k = self.center = center  

	def set_size(self, size):
		self.w, self.h = self.size = size 

	def set_color(self, color):
		self.color = color

	def update(self):
		pass

	def draw(self, surface):
		pass

class Rect (Shape):
	def __init__(self, top_left, size, color, width=0):
		w, h = size 
		self.x, self.y = self.top_left = top_left
		super().__init__((self.x - w // 2, self.y - h // 2), size, color, width)

	def is_within(self, position):
		v = Vector(*position) - Vector(*self.center)
		return v.v0 <= self.w and v.v1 <= self.h 

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, pygame.Rect(self.top_left, self.size), self.width)

class Card:
	def __init__(self, value, suit):
		self.suit = suit 
		self.value = value

	def update(self):
		pass

	def draw(self, surface):
		pass

class Deck:
	def __init__(self):
		pass

	def shuffle(self):
		pass

	def top(self):
		pass

	def update(self):
		pass

	def draw(self, surface):
		pass

class CardSlot:
	def __init__(self, position, size):
		self.rect = Rect(position, size, Color.RED, 1)

	def set_position(self, position):
		self.rect.set_center(position)

	def update(self):
		self.rect.update()

	def draw(self, surface):
		self.rect.draw(surface)

class Pair:
	def __init__(self, x, y):
		self.x = x 
		self.y = y

class CardTable:
	CARD_SIZE_RATIO = 2.5 / 3.5

	def __init__(self, position, size):
		x, y = position
		self.w, self.h = self.size = size 
		self.mw, self.mh = (5, 5)
		self.card_width, self.card_height = (0, 0)
		self.x, self.y = self.origin = (x + self.w // 2, y + self.h // 2)
		self.half_w, self.half_h = self.w / 2, self.h / 2 
		self.left_x, self.right_x = self.mw + self.x - self.half_w, self.x + self.half_w - self.mw
		self.top_y, self.bottom_y = self.mh + self.y - self.half_h, self.y + self.half_h - self.mh
		self.left_top = Pair(self.left_x, self.top_y)
		self.right_top = Pair(self.right_x, self.top_y)
		self.left_bottom = Pair(self.left_x, self.bottom_y)  
		self.right_bottom = Pair(self.right_x, self.bottom_y)
		self.card_slots = [] 
		self.create()

	def set_size(self, size):
		self.w, self.h = self.size = size 
		self.half_w, self.half_h = self.w / 2, self.h / 2 

	def set_position(self, position):
		x, y = position
		self.x, self.y = self.origin = (x + self.w // 2, y + self.h // 2)

	def assay(self):
		self.card_height = 2 * (self.half_h - 2 * self.mh) / 3
		temp_cw = self.card_height * CardTable.CARD_SIZE_RATIO
		min_width = (2 * self.half_w - 5 * self.mw) / 4
		total_width = 4 * temp_cw + 5 * self.mw
		while  total_width > self.w and not total_width <= min_width:
			print('In while loop...')
			self.card_height -= 10
			temp_cw = self.card_height * CardTable.CARD_SIZE_RATIO
			total_width = 4 * temp_cw + 5 * self.mw
		self.card_width = temp_cw
		self.card_size = (self.card_width, self.card_height)
		
	def create(self):
		self.assay()
		for i in range(4):
			for j in range(3):
				cx = self.left_x + i * (self.card_width + self.mw)
				cy = self.top_y + j * (self.card_height + self.mh)
				self.card_slots.append(CardSlot((cx, cy), self.card_size))
		self.recenter()

	def recenter(self):
		extra_w = (self.w - (4 * self.card_width  + 5 * self.mw)) / 2
		print(extra_w)
		for i in range(4):
			for j in range(3):
				card_slot = self.card_slots[4 * j + i]
				x, y = card_slot.rect.center
				card_slot.set_position((x + extra_w, y))

	def on_resize(self, position, size):
		print(size)
		self.set_size(size)
		self.set_position(position)
		self.card_slots.clear()
		self.create()

	def update(self):
		pass

	def draw(self, surface):
		for card_slot in self.card_slots:
			card_slot.draw(surface)

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
		elif event.type == pygame.VIDEORESIZE:
			self.size = (event.w, event.h)
			self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)
			self.card_table.on_resize((0, 0), self.size)

	def update(self):
		pass

	def draw(self):
		self.surface.fill(Color.BLACK)
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