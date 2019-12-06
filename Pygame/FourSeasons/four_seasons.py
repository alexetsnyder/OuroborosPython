#four_seasons.py
import go
import pygame, random
from datetime import datetime
from pygame import freetype
from structs import *

#To Do:
#1) Font Size Changes do to window size.
#2) Sort cards so, that you the correct show first, and are selected first.

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
		self.rect = go.Rect((0, 0), (0, 0), Color.TEAL_FELT)
		self.card_back = pygame.image.load('{0}/{1}'.format(Card.SOURCE_FOLDER, Card.CARD_BACK_IMAGE_FILE)).convert()
		self.card_front = pygame.image.load('{0}/card{1}{2}.png'.format(Card.SOURCE_FOLDER, self.suit_str, self.card_str)).convert() 	
		# self.card_font_info = FontInfo(font_size=40, font_color=self.suit_color)
		# self.suit_font_info = FontInfo(font_size=20, font_color=self.suit_color, font_name='segoeuiemoji')
		# self.card_text = RenderText(self.card_str, font_info=self.card_font_info)
		# self.suit_text = RenderText(self.suit_str, font_info=self.suit_font_info)
		# self.border = Rect((0, 0), (0, 0), Color.BLACK, 2)
		
	def on_click(self, event):
		self.is_selected = True
		self.mouse_pos = event.pos 

	def on_mouse_button_up(self, slot, new_slot_index):
		x, y = slot.top_left
		self.is_selected = False
		self.set_position(x, y, self.rect.w, self.rect.h)
		self.slot_index = new_slot_index

	def on_move(self, event):
		if self.is_selected:
			new_pos = event.pos 
			v = go.Vector(*new_pos) - go.Vector(*self.mouse_pos)
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
		x, y = self.rect.top_left
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

def reverse(l):
	return [l[j] for j in range(len(l) - 1, -1, -1)]

class Deck:
	def __init__(self):
		self.seed = datetime.now()
		random.seed(self.seed)
		self.deck = []
		self.active_cards = []
		self.top_card = -1
		self.create()

	def on_resize(self, tiles):
		for i in self.active_cards:
			self.deck[i].on_resize(tiles[self.deck[i].slot_index])

	def on_click(self, event):
		for i in reverse(self.active_cards):
			if self.deck[i].is_within(event.pos):
				self.active_cards.remove(i)
				self.active_cards.append(i)
				print(self.active_cards)
				self.deck[i].on_click(event)
				break

	def on_mouse_button_up(self, tiles):
		selected_card = None
		for i in self.active_cards:
			if self.deck[i].is_selected:
				selected_card = self.deck[i]
				break
		if not selected_card == None:
			max_area = 0
			max_tile = None
			max_index = self.deck[i].slot_index
			for i, tile in tiles:
				if selected_card.rect.is_intersecting(tile.rect):
					area = selected_card.rect.intersecting(tile.rect).area()
					if area > max_area:
						max_area = area
						max_tile = tile
						max_index = i 
			selected_card.on_mouse_button_up(max_tile, max_index)

	def on_mouse_move(self, event):
		for i in self.active_cards:
			self.deck[i].on_move(event)

	def create(self):
		for suit in range(4):
			for i in range(1, 14):
				self.deck.append(Card(i, suit, CardTable.DECK_TILE))

	def shuffle(self):
		random.shuffle(self.deck)

	def new_deal(self):
		self.reset()
		self.deck[0].set_slot(CardTable.FOUNDATION_TILES[0])
		self.deck[0].is_showing = True
		for i in range(1, 6):
			self.deck[i].set_slot(CardTable.TABLEAU_TILES[i - 1])
			self.deck[i].is_showing = True
		self.deck[6].set_slot(CardTable.DISCARD_TILE)
		self.deck[6].is_showing = True
		self.top_card = 7
		self.active_cards += [i for i in range(8)]

	def reset(self):
		self.active_cards.clear()
		for card in self.deck:
			card.set_slot(CardTable.DECK_TILE)

	def top(self):
		return self.deck[self.top_card]

	def flip_cards(self):
		for i in self.active_cards:
			self.deck[i].is_showing = not self.deck[i].is_showing

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
		self.rect = go.Rect(self.top_left, self.size, Color.BLACK, 1)

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
		self.left_top = (self.left_x, self.top_y)
		self.right_top = (self.right_x, self.top_y)
		self.left_bottom = (self.left_x, self.bottom_y)  
		self.right_bottom = (self.right_x, self.bottom_y)
		self.card_tiles = [] 
		self.create()
		self.deck = Deck()
		print('Seed: {0}'.format(self.deck.seed))
		self.deck.shuffle()
		self.deck.new_deal()

	def get(self, index):
		return self.card_tiles[index]

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
				self.card_tiles.append(CardTile((cx, cy), self.card_size))
		self.recenter()

	def recenter(self):
		extra_w = (self.w - (4 * self.card_width  + 5 * self.mw)) // 2
		extra_h = (self.h - (3 * self.card_height + 4 * self.mh)) // 2 
		for i in range(4):
			for j in range(3):
				card_tile = self.card_tiles[4 * j + i]
				x, y = card_tile.rect.top_left
				card_tile.set_position((x + extra_w, y + extra_h))

	def on_resize(self, position, size):
		self.set_size(size)
		self.set_position(position)
		self.card_tiles.clear()
		self.create()
		self.deck.on_resize(self.card_tiles)

	def on_mouse_button_up(self, event):
		self.deck.on_mouse_button_up(self.tiles())
		# max_area = 0
		# max_index = self.card.slot_index
		# for i, slot in self.tiles():
		# 	if self.card.rect.is_intersecting(slot.rect):
		# 		area = self.card.rect.intersecting(slot.rect).area()
		# 		if area > max_area:
		# 			max_area = area 
		# 			max_index = i  		
		#self.card.on_mouse_button_up(*self.get(max_index).top_left, max_index)

	def on_mouse_button_down(self, event):
		self.deck.on_click(event)
		#self.card.on_click(event)

	def on_mouse_move(self, event):
		self.deck.on_mouse_move(event)
		#self.card.on_move(event)

	def tiles(self):
		return ((i, self.card_tiles[i]) for i in range(len(self.card_tiles)) if not i == CardTable.NON_TILE)

	def flip_cards(self):
		self.deck.flip_cards()

	def new_shuffle(self):
		self.deck.shuffle()
		self.deck.new_deal()

	def update(self):
		pass

	def draw(self, surface):
		for i, slot in self.tiles():
			slot.draw(surface)
		self.deck.draw(surface)
		#self.card.draw(surface)