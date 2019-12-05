#four_seasons.py
import pygame, random
from datetime import datetime
from pygame import freetype

#To Do:
#1) Font Size Changes do to window size.

class Color:
	WHITE  		  = (255, 255, 255)
	BLACK  		  = (  0,   0,   0)
	RED           = (255,   0,   0)
	GREEN  		  = (  0, 255,   0)
	SEA_GREEN     = ( 46, 139,  87)
	FOREST_GREEN  = ( 13,  55,  13)
	TEAL_FELT     = ( 20, 118,  98)
	BLUE   		  = (  0,   0, 255)
	ALICE_BLUE    = (240, 248, 255)
	DEEP_SKY_BLUE = (  0, 191, 255)
	YELLOW 		  = (255, 255,   0)
	SAND          = ( 76,  70,  50)
	SILVER 		  = (192, 192, 192)

def debug_print(**kargs):
	print(', '.join(['{0}: {1}'.format(key, value) for key, value in kargs.items()]))

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
	def __init__(self, text_str, position=(0, 0), font_info=FontInfo()):
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

	def move(self, dx, dy):
		self.set_position((self.x + dx, self.y + dy))

	def draw_at(self, surface, position):
		x, y = position
		self.font.render_to(surface, (int(x - self.w // 2), int(y - self.h // 2)), self.text_str, self.font_info.font_color)

	def draw(self, surface):
		self.font.render_to(surface, (int(self.x - self.w // 2), int(self.y - self.h // 2)), self.text_str, self.font_info.font_color)

class Rect:
	def __init__(self, top_left, size, color=Color.SILVER, width=0):
		self.width = width
		self.color = color 
		self.w, self.h = self.size = size 
		self.left, self.top = top_left
		self.right, self.bottom = (self.left + self.w, self.top + self.h)
		self.center = self.left + self.w // 2, self.top + self.h // 2
		self.top_left = Pair(*top_left)
		self.top_right = Pair(self.right, self.top)
		self.bottom_left = Pair(self.left, self.bottom)
		self.bottom_right = Pair(self.right, self.bottom) 

	def set_position(self, top_left):
		self.left, self.top = top_left
		self.right, self.bottom = (self.left + self.w, self.top + self.h)
		self.center = self.left + self.w // 2, self.top + self.h // 2
		self.top_left = Pair(*top_left)
		self.top_right = Pair(self.right, self.top)
		self.bottom_left = Pair(self.left, self.bottom)
		self.bottom_right = Pair(self.right, self.bottom)

	def set_color(self, color):
		self.color = color

	def set_size(self, size):
		self.w, self.h = self.size = size 

	def area(self):
		return (self.right - self.left) * (self.bottom - self.top)

	def is_intersecting(self, r2):
		left = max(self.left, r2.left)
		right = min(self.right, r2.right)
		bottom = min(self.bottom, r2.bottom)
		top = max(self.top, r2.top)
		return left < right and top < bottom

	def intersecting(self, r2):
		left = max(self.left, r2.left)
		right = min(self.right, r2.right)
		bottom = min(self.bottom, r2.bottom)
		top = max(self.top, r2.top)
		return Rect((left, top), (right - left, bottom - top))

	def is_within(self, position):
		x1, y1 = position
		x2, y2 = self.center
		return (x2 - x1) ** 2 <= (self.w // 2) ** 2 and (y2 - y1) ** 2 <= (self.h // 2) ** 2 

	def move(self, dx, dy):
		self.set_position((self.left + dx, self.top + dy))

	def draw_at(self, surface, position):
		x, y = position
		pygame.draw.rect(surface, self.color, pygame.Rect((int(x), int(y)), (int(self.w), int(self.h))), self.width)

	def draw(self, surface):
		x, y = self.top_left.pair
		pygame.draw.rect(surface, self.color, pygame.Rect((int(x), int(y)), (int(self.w), int(self.h))), self.width)

class Suits:
	DIAMONDS = 0
	HEARTS   = 1
	SPADES   = 2
	CLUBS    = 3

SUITS_CHAR = {
 	Suits.DIAMONDS : '♢',
 	Suits.HEARTS   : '♡',
 	Suits.SPADES   : '♤',
	Suits.CLUBS    : '♧' 
}

SUITS_STR = {
 	Suits.DIAMONDS : 'Diamonds',
 	Suits.HEARTS   : 'Hearts',
 	Suits.SPADES   : 'Spades',
	Suits.CLUBS    : 'Clubs' 
}

SUITS_COLOR = {
 	Suits.DIAMONDS : Color.RED,
 	Suits.HEARTS   : Color.RED,
 	Suits.SPADES   : Color.BLACK,
 	Suits.CLUBS    : Color.BLACK 
}

CARD_VALUES = {
	'A' :    1,
	'2' :    2,
	'3' :    3,
	'4' :    4,
	'5' :    5,
	'6' :    6,
	'7' :    7,
	'8' :    8,
	'9' :    9,
   '10' :   10,
	'J' :   11,
	'Q' :   12,
	'K' :   13
}

CARD_LETTERS = {
	 1  :  'A',
	 2  :  '2',
	 3  :  '3',
	 4  :  '4',
	 5  :  '5',
	 6  :  '6',
	 7  :  '7',
	 8  :  '8',
	 9  :  '9',
	10  : '10',
	11  :  'J',
	12  :  'Q',
	13  :  'K',
}

class Card:
	SOURCE_FOLDER = 'Cards'
	CARD_BACK_IMAGE_FILE = 'cardBack_red5.png'

	def __init__(self, card_val, suit, slot_index, is_showing=False): 
		self.mw, self.mh = (5, 5)
		self.is_selected = False
		self.mouse_pos = (0, 0)
		self.suit = suit
		self.value = card_val
		self.slot_index = slot_index
		self.card_str = CARD_LETTERS[self.value]
		self.suit_char = SUITS_CHAR[suit]
		self.suit_str = SUITS_STR[suit] 
		self.suit_color = SUITS_COLOR[suit]
		self.front_color = Color.ALICE_BLUE
		self.back_color = Color.DEEP_SKY_BLUE
		self.is_showing = is_showing
		self.rect = Rect((0, 0), (0, 0), Color.TEAL_FELT)
		self.card_back = pygame.image.load('{0}/{1}'.format(Card.SOURCE_FOLDER, Card.CARD_BACK_IMAGE_FILE)).convert()
		self.card_front = pygame.image.load('{0}/card{1}{2}.png'.format(Card.SOURCE_FOLDER, self.suit_str, self.card_str)).convert() 	
		# self.card_font_info = FontInfo(font_size=40, font_color=self.suit_color)
		# self.suit_font_info = FontInfo(font_size=20, font_color=self.suit_color, font_name='segoeuiemoji')
		# self.card_text = RenderText(self.card_str, font_info=self.card_font_info)
		# self.suit_text = RenderText(self.suit_str, font_info=self.suit_font_info)
		# self.border = Rect((0, 0), (0, 0), Color.BLACK, 2)
		
	def on_click(self, event):
		if self.is_within(event.pos):
			self.is_selected = True
			self.mouse_pos = event.pos 

	def on_mouse_button_up(self, x, y, new_slot_index):
		self.is_selected = False
		self.set_position(x, y, self.rect.w, self.rect.h)
		self.slot_index = new_slot_index

	def on_move(self, event):
		if self.is_selected:
			new_pos = event.pos 
			v = Vector(*new_pos) - Vector(*self.mouse_pos)
			self.move(v.v0, v.v1)
			self.mouse_pos = new_pos

	def on_resize(self, slot):
		x, y = slot.top_left
		w, h = slot.size 	
		self.set_size(w, h)
		self.set_position(x, y, w, h)
		
	def is_within(self, position):
		return self.rect.is_within(position)

	def set_size(self, w, h):
		self.rect.set_size((w - self.mw, h - self.mh))
		# self.border.set_size((w - self.mw, h - self.mh))

	def set_slot(self, slot_index):
		self.slot_index = slot_index

	def set_position(self, x, y, w, h):
		self.rect.set_position((x + self.mw // 2, y + self.mh // 2)) 
		# cx, cy = (x + w // 2,  y + h // 2)
		# self.card_text.set_position((cx, cy))
		# self.suit_text.set_position((cx, cy + self.card_text.h))
		# self.border.set_position((x + self.mw // 2, y + self.mh // 2))

	def move(self, dx, dy): 
		self.rect.move(dx, dy)
		#self.border.move(dx, dy)
		# self.card_text.move(dx, dy)
		# self.suit_text.move(dx, dy)

	def update(self):
		self.rect.update()
		# self.card_text.update()
		# self.suit_text.update()
		# self.border.update()

	def draw(self, surface):
		x, y = self.rect.top_left.pair 
		w, h = self.rect.size 
		card_image = None
		if self.is_showing:
			card_image = self.card_front
		else:
			card_image = self.card_back
		surface.blit(pygame.transform.scale(card_image, (int(w), int(h))), (int(x), int(y)))
		# self.rect.draw(surface)
		# self.border.draw(surface)
		# if self.is_showing:
		# 	self.card_text.draw(surface)
		# 	self.suit_text.draw(surface)

class Deck:
	def __init__(self):
		self.seed = datetime.now()
		random.seed(self.seed)
		self.deck = []
		self.active_cards = []
		self.top_card = -1
		self.create()

	def on_resize(self, slots):
		for i in self.active_cards:
			self.deck[i].on_resize(slots[self.deck[i].slot_index])

	def create(self):
		for suit in range(4):
			for i in range(1, 14):
				self.deck.append(Card(i, suit, CardTable.DECK_TILE))

	def shuffle(self):
		random.shuffle(self.deck)

	def new_deal(self):
		self.deck[0].set_slot(CardTable.FOUNDATION_TILES[0])
		self.deck[0].is_showing = True
		for i in range(1, 6):
			self.deck[i].set_slot(CardTable.TABLEAU_TILES[i - 1])
			self.deck[i].is_showing = True
		self.deck[6].set_slot(CardTable.DISCARD_TILE)
		self.deck[6].is_showing = True
		self.top_card = 7
		self.active_cards += [i for i in range(8)]

	def top(self):
		return self.deck[self.top_card]

	def update(self):
		for i in self.active_cards:
			self.deck[i].draw(surface) 

	def draw(self, surface):
		for i in self.active_cards:
			self.deck[i].draw(surface)

class CardTile:
	def __init__(self, top_left, size):
		self.x, self.y = self.top_left = top_left
		self.w, self.h = self.size = size 
		self.rect = Rect(self.top_left, self.size, Color.BLACK, 1)

	def set_position(self, top_left):
		self.x, self.y = self.top_left = top_left
		self.rect.set_position(self.top_left)

	def set_size(self, size):
		self.w, self.h = self.size = size 
		self.rect.set_size(self.size)

	def update(self):
		self.rect.update()

	def draw(self, surface):
		self.rect.draw(surface)

class TableueTile (CardTile):
	pass

class DeckTile (CardTile):
	pass

class DiscardTile (CardTile):
	pass

class FoundationTile (CardTile):
	pass

class Pair:
	def __init__(self, x, y):
		self.x = x 
		self.y = y
		self.pair = (x, y)

class CardTable:
	NON_TILE         = 2
	DECK_TILE        = 0
	DISCARD_TILE     = 1
	TABLEAU_TILES    = [6, 4, 7, 10, 8]
	FOUNDATION_TILES = [3, 5, 9, 11] 
	CARD_SIZE_RATIO  = 2.5 / 3.5

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
		self.deck = Deck()
		print('Seed: {0}'.format(self.deck.seed))
		self.deck.shuffle()
		self.deck.new_deal()
		#self.card = Card('A', Suits.DIAMONDS, CardTable.DECK_TILE, False)

	def get(self, index):
		return self.card_slots[index]

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
				self.card_slots.append(CardTile((cx, cy), self.card_size))
		self.recenter()

	def recenter(self):
		extra_w = (self.w - (4 * self.card_width  + 5 * self.mw)) // 2
		extra_h = (self.h - (3 * self.card_height + 4 * self.mh)) // 2 
		for i in range(4):
			for j in range(3):
				card_slot = self.card_slots[4 * j + i]
				x, y = card_slot.rect.top_left.pair
				card_slot.set_position((x + extra_w, y + extra_h))

	def on_resize(self, position, size):
		self.set_size(size)
		self.set_position(position)
		self.card_slots.clear()
		self.create()
		self.deck.on_resize(self.card_slots)
		#self.card.on_resize(*self.get(self.card.slot_index).top_left, *self.get(self.card.slot_index).size)

	def on_mouse_button_up(self, event):
		pass
		# max_area = 0
		# max_index = self.card.slot_index
		# for i, slot in self.slot_gen():
		# 	if self.card.rect.is_intersecting(slot.rect):
		# 		area = self.card.rect.intersecting(slot.rect).area()
		# 		if area > max_area:
		# 			max_area = area 
		# 			max_index = i  		
		#self.card.on_mouse_button_up(*self.get(max_index).top_left, max_index)

	def on_mouse_button_down(self, event):
		pass
		#self.card.on_click(event)

	def on_mouse_move(self, event):
		pass
		#self.card.on_move(event)

	def slot_gen(self):
		return ((i, self.card_slots[i]) for i in range(len(self.card_slots)) if not i == CardTable.NON_TILE)

	def update(self):
		pass

	def draw(self, surface):
		for i, slot in self.slot_gen():
			slot.draw(surface)
		self.deck.draw(surface)
		#self.card.draw(surface)

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
				self.card_table.card.is_showing = not self.card_table.card.is_showing
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