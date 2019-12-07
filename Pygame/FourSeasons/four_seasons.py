#four_seasons.py
import go, time
import pygame, random
from pygame import freetype
from structs import *

#To Do:
#1) Font Size Changes do to window size.
#2) Increase margin size.

class Card:
	SOURCE_FOLDER = 'Cards'
	CARD_BACK_IMAGE_FILE = 'cardBack_red5.png'

	def __init__(self, card_val, suit, tile_index, is_showing=False): 
		self.mouse_pos = (0, 0)
		self.is_selected = False
		self.mw, self.mh = (0, 0)
		self.suit = suit
		self.value = card_val
		self.tile_index = tile_index
		self.is_showing = is_showing
		self.card_str = CARD_LETTERS[self.value]
		self.suit_char = SUITS_CHAR[suit]
		self.suit_str = SUITS_STR[suit] 
		self.suit_color = SUITS_COLOR[suit]
		self.front_color = Color.ALICE_BLUE
		self.back_color = Color.DEEP_SKY_BLUE
		self.rect = go.Rect((0, 0), (0, 0), Color.TEAL_FELT)
		self.card_back = pygame.image.load('{0}/{1}'.format(Card.SOURCE_FOLDER, Card.CARD_BACK_IMAGE_FILE)).convert()
		self.card_front = pygame.image.load('{0}/card{1}{2}.png'.format(Card.SOURCE_FOLDER, self.suit_str, self.card_str)).convert()
		
	def on_mouse_left_button_down(self, event):
		self.is_selected = True
		self.mouse_pos = event.pos 

	def on_mouse_left_button_up(self, tile, new_tile_index):
		x, y = tile.top_left
		self.is_selected = False
		self.set_position(x, y, self.rect.w, self.rect.h)
		self.tile_index = new_tile_index

	def on_mouse_right_button_down(self):
		self.is_showing = not self.is_showing

	def on_mouse_move(self, event):
		if self.is_selected:
			new_pos = event.pos 
			v = go.Vector(*new_pos) - go.Vector(*self.mouse_pos)
			self.move(v.v0, v.v1)
			self.mouse_pos = new_pos

	def on_resize(self, tile):
		self.put(tile)

	def put(self, tile):	
		self.set_size(*tile.size)
		self.set_position(*tile.top_left, *tile.size)
		
	def is_within(self, position):
		return self.rect.is_within(position)

	def set_size(self, w, h):
		self.rect.set_size((w - self.mw, h - self.mh))

	def set_tile(self, tile_index):
		self.tile_index = tile_index

	def set_position(self, x, y, w, h):
		self.rect.set_position((x + self.mw // 2, y + self.mh // 2)) 

	def move(self, dx, dy): 
		self.rect.move(dx, dy)

	def update(self):
		self.rect.update()

	def draw(self, surface):
		x, y = self.rect.top_left
		w, h = self.rect.size 
		card_image = None
		if self.is_showing:
			card_image = self.card_front
		else:
			card_image = self.card_back
		surface.blit(pygame.transform.scale(card_image, (int(w), int(h))), (int(x), int(y)))

def reverse(l):
	return [l[j] for j in range(len(l) - 1, -1, -1)]

class Deck:
	SUIT_COUNT  = 4
	CARD_COUNT  = 13
	DEALT_CARDS = 7

	def __init__(self):
		self.seed = -1
		self.top_card = -1
		self.deck = []
		self.active_cards = []
		self.create()

	def shuffle_seed(self):
		self.seed = time.time()
		random.seed(self.seed)

	def on_resize(self, tiles):
		for i in self.active_cards:
			card = self.deck[i]
			card.on_resize(tiles[card.tile_index])

	def on_mouse_left_button_down(self, event):
		for i in reverse(self.active_cards):
			card = self.deck[i]
			if card.is_within(event.pos):
				self.active_cards.remove(i)
				self.active_cards.append(i)
				card.on_mouse_left_button_down(event)
				break

	def on_mouse_right_button_down(self, event):
		for i in reverse(self.active_cards):
			card = self.deck[i]
			if card.is_within(event.pos):
				card.on_mouse_right_button_down()
				break

	def on_mouse_left_button_up(self, tiles):
		selected_card = None
		for i in self.active_cards:
			if self.deck[i].is_selected:
				selected_card = self.deck[i]
				break
		if not selected_card == None:
			max_area = 0
			max_tile = tiles[selected_card.tile_index]
			max_tile_index = selected_card.tile_index
			for i, tile in [(i, tiles[i]) for i in range(len(tiles)) if not i == CardTable.NON_TILE]:
				if selected_card.rect.is_intersecting(tile.rect):
					area = selected_card.rect.intersecting(tile.rect).area()
					if area > max_area:
						max_area = area
						max_tile = tile
						max_tile_index = i 
			selected_card.on_mouse_left_button_up(max_tile, max_tile_index)

	def on_mouse_move(self, event):
		for i in self.active_cards:
			self.deck[i].on_mouse_move(event)

	def create(self):
		for suit in range(Deck.SUIT_COUNT):
			for i in range(1, Deck.CARD_COUNT + 1):
				self.deck.append(Card(i, suit, CardTable.DECK_TILE))

	def shuffle(self):
		self.shuffle_seed()
		self.print_seed()
		random.shuffle(self.deck)

	def deal(self, tiles):
		for i in self.active_cards:
			card = self.deck[i]
			card.put(tiles[card.tile_index])

	def new_deal(self, tiles):
		self.reset()
		self.shuffle()
		self.draw_card(self.deck[0], CardTable.FOUNDATION_TILES[0])
		for i in range(1, Deck.DEALT_CARDS - 1):
			self.draw_card(self.deck[i], CardTable.TABLEAU_TILES[i - 1])
		self.draw_card(self.deck[Deck.DEALT_CARDS - 1], CardTable.DISCARD_TILE)
		self.top_card = Deck.DEALT_CARDS
		self.active_cards += [i for i in range(Deck.DEALT_CARDS + 1)]
		self.deal(tiles)

	def draw_card(self, card, tile_index, is_showing=True):
		card.set_tile(tile_index)
		card.is_showing = is_showing

	def reset(self):
		self.active_cards.clear()
		for card in self.deck:
			card.set_tile(CardTable.DECK_TILE)
			card.is_showing = False

	def top(self):
		return self.deck[self.top_card]

	def flip_cards(self):
		for i in self.active_cards:
			card = self.deck[i]
			card.is_showing = not card.is_showing

	def print_seed(self):
		print('Seed: {0}'.format(self.seed))

	def update(self):
		for i in self.active_cards:
			self.deck[i].draw(surface) 

	def draw(self, surface):
		for i in self.active_cards:
			self.deck[i].draw(surface)

class CardTile:
	def __init__(self, top_left, size):
		self.w, self.h = self.size = size 
		self.left, self.top = self.top_left = top_left
		self.rect = go.Rect(self.top_left, self.size, Color.BLACK, 1)

	def set_position(self, top_left):
		self.left, self.top = self.top_left = top_left
		self.rect.set_position(self.top_left)

	def set_size(self, size):
		self.w, self.h = self.size = size 
		self.rect.set_size(self.size)

	def update(self):
		self.rect.update()

	def draw(self, surface):
		self.rect.draw(surface)

class DeckTile (CardTile):
	INDEX = 0

class DiscardTile (CardTile):
	INDEX = 1

class NonTile:
	INDEX = 2

class TableueTile (CardTile):
	INDEXES = [6, 4, 7, 10, 8]
	def __init__(self, tile_index):
		self.tile_index = tile_index 

class FoundationTile (CardTile):
	INDEXES = [3, 5, 9, 11]
	def __init__(self, tile_index):
		self.tile_index = tile_index 

class CardTable:
	NON_TILE         = 2
	DECK_TILE        = 0
	DISCARD_TILE     = 1
	TABLEAU_TILES    = [6, 4, 7, 10, 8]
	FOUNDATION_TILES = [3, 5, 9, 11] 
	COLUMNS          = 4
	ROWS             = 3 
	CARD_SIZE_RATIO  = 2.5 / 3.5

	def __init__(self, position, size):
		self.mw, self.mh = (15, 15)
		self.card_width, self.card_height = (0, 0)
		self.set_size(size)
		self.set_position(position)
		self.card_tiles = [] 
		self.create()
		self.deck = Deck()
		self.deck.new_deal(self.card_tiles)

	def get(self, index):
		return self.card_tiles[index]

	def set_size(self, size):
		self.w, self.h = self.size = size 
		self.half_w, self.half_h = self.w / 2, self.h / 2 

	def set_position(self, position):
		x, y = position
		self.x, self.y = self.origin = (x + self.w // 2, y + self.h // 2)
		self.left, self.right = self.mw + self.x - self.half_w, self.x + self.half_w - self.mw
		self.top, self.bottom = self.mh + self.y - self.half_h, self.y + self.half_h - self.mh
		self.left_top = (self.left, self.top)
		self.right_top = (self.right, self.top)
		self.left_bottom = (self.left, self.bottom)  
		self.right_bottom = (self.right, self.bottom)

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
		for i in range(CardTable.COLUMNS):
			for j in range(CardTable.ROWS):
				cx = self.left + i * (self.card_width + self.mw)
				cy = self.top + j * (self.card_height + self.mh)
				self.card_tiles.append(CardTile((cx, cy), self.card_size))
		self.recenter()

	def recenter(self):
		extra_w = (self.w - (4 * self.card_width  + 5 * self.mw)) // 2
		extra_h = (self.h - (3 * self.card_height + 4 * self.mh)) // 2 
		for i in range(CardTable.COLUMNS):
			for j in range(CardTable.ROWS):
				card_tile = self.card_tiles[4 * j + i]
				x, y = card_tile.rect.top_left
				card_tile.set_position((x + extra_w, y + extra_h))

	def on_resize(self, position, size):
		self.set_size(size)
		self.set_position(position)
		self.card_tiles.clear()
		self.create()
		self.deck.on_resize(self.card_tiles)

	def on_mouse_left_button_up(self, event):
		self.deck.on_mouse_left_button_up(self.card_tiles)

	def on_mouse_left_button_down(self, event):
		self.deck.on_mouse_left_button_down(event)

	def on_mouse_right_button_down(self, event):
		self.deck.on_mouse_right_button_down(event)

	def on_mouse_move(self, event):
		self.deck.on_mouse_move(event)

	def tiles(self):
		return [self.card_tiles[i] for i in range(len(self.card_tiles)) if not i == CardTable.NON_TILE]

	def flip_cards(self):
		self.deck.flip_cards()

	def new_shuffle(self):
		self.deck.new_deal(self.card_tiles)

	def update(self):
		pass

	def draw(self, surface):
		for tile in self.tiles():
			tile.draw(surface)
		self.deck.draw(surface)
