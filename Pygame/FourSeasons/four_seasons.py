#four_seasons.py
import go, imp, events
import pygame, random, time, sys
from pygame import freetype
from structs import *

#ToDo:
#1) Special cases for A and K.
#2) Tableue laying logic wrong.
#3) Objects have a certain background.
#4) Reshuffle issue with extra cards, and continues decrement.
#5) Extra number or one less card, and missing cards.

def class_pause_events_decorator(cls):
	class ClassWrapper (cls):
		def __init__(self, *args, **kargs):
			self.is_paused = False
			super().__init__(*args, **kargs)

		def on_pause(self, event):
			self.is_paused = not self.is_paused

		def wire_events(self):
			super().wire_events()
			imp.IMP().add_delegate(events.KeyDownEvent(pygame.K_ESCAPE).create(self.on_pause))
	return ClassWrapper

def function_pause_events_decorator(func):
	def func_wrapper(self, event):
		if not self.is_paused:
			func(self, event)
	return func_wrapper

@class_pause_events_decorator
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
		self.rect = go.Rect((0, 0), (0, 0), False)
		self.card_back = pygame.image.load('{0}/{1}'.format(Card.SOURCE_FOLDER, Card.CARD_BACK_IMAGE_FILE)).convert()
		self.card_front = pygame.image.load('{0}/card{1}{2}.png'.format(Card.SOURCE_FOLDER, self.suit_str, self.card_str)).convert()
		self.wire_events()

	def __str__(self):
		return '<{} {}>'.format(self.card_str, self.suit_str)

	def wire_events(self):
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.CARD_MOTION).create(self.on_card_motion, quell=True))
		imp.IMP().add_delegate(events.MouseLeftButtonUpEvent().create(self.on_mouse_left_button_up, quell=True))

	@function_pause_events_decorator
	def on_card_motion(self, event):
		if self.is_selected:
			new_pos = event.pos 
			v = go.Vector(*new_pos) - go.Vector(*self.mouse_pos)
			self.move(v.v0, v.v1)
			self.mouse_pos = new_pos

	@function_pause_events_decorator
	def on_mouse_left_button_up(self, event):
		if self.is_selected:
			events.UserEvent(CustomEvent.CARD_LAYED).post(card=self)

	def select(self, mouse_pos):
		self.is_selected = True
		self.mouse_pos = mouse_pos

	def put(self, tile):
		self.is_selected = False
		self.tile_index = tile.index 	
		self.set_size(*tile.size)
		self.set_position(*tile.left_top, *tile.size)

	def flip(self):
		self.is_showing = not self.is_showing

	def show(self):
		self.is_showing = True

	def equals(self, card):
		return card.suit == self.suit and card.value == self.value
		
	def is_within(self, position):
		return self.rect.is_within(position)

	def set_size(self, w, h):
		self.rect.set_size((w - self.mw, h - self.mh))

	def set_position(self, x, y, w, h):
		self.rect.set_position((x + self.mw // 2, y + self.mh // 2)) 

	def move(self, dx, dy): 
		self.rect.move(dx, dy)

	def update(self):
		self.rect.update()

	def draw(self, surface):
		x, y = self.rect.left_top
		w, h = self.rect.size 
		card_image = None
		if self.is_showing:
			card_image = self.card_front
		else:
			card_image = self.card_back
		surface.blit(pygame.transform.scale(card_image, (int(w), int(h))), (int(x), int(y)))

def reverse(l):
	return [l[j] for j in range(len(l) - 1, -1, -1)]

@class_pause_events_decorator
class Deck:
	SUIT_COUNT  = 4
	DEALT_CARDS = 7
	CARD_COUNT  = 13

	def __init__(self):
		self.seed = -1
		self.deck = []
		self.active_cards = []
		self.create()
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.TILE_CLICKED).create(self.on_tile_clicked))
		imp.IMP().add_delegate(events.MouseRightButtonUpEvent().create(self.on_mouse_right_button_up))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.NEW_DEAL).create(self.on_new_deal))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.DRAW_ONE).create(self.on_draw_one))

	@function_pause_events_decorator
	def on_draw_one(self, event):
		if len(self.active_cards) <= Deck.SUIT_COUNT * Deck.CARD_COUNT:
			next_index = len(self.active_cards)
			self.active_cards.append(next_index)
			next_card = self.deck[next_index]
			event.discard_tile.lay(next_card)

	@function_pause_events_decorator
	def on_new_deal(self, event):
		self.new_deal(event.tiles)

	@function_pause_events_decorator
	def on_mouse_right_button_up(self, event):
		for i in self.active_cards:
			card = self.deck[i]
			if card.is_within(event.pos):
				card.flip()
				break

	@function_pause_events_decorator
	def on_tile_clicked(self, event):
		for i in reverse(self.active_cards):
			card = self.deck[i]
			if card.tile_index == event.tile.index:
				self.active_cards.remove(i)
				self.active_cards.append(i)
				card.select(event.pos)
				break

	def create(self):
		for suit in range(Deck.SUIT_COUNT):
			for i in range(1, Deck.CARD_COUNT + 1):
				self.deck.append(Card(i, suit, DeckTile.INDEX))

	def shuffle_seed(self):
		self.seed = time.time()
		random.seed(self.seed)

	def shuffle(self):
		self.shuffle_seed()
		self.print_seed()
		random.shuffle(self.deck)

	def new_deal(self, tiles):
		self.reset()
		self.shuffle()
		deck_tile = tiles[DeckTile.INDEX]
		deck_tile.reset()
		self.draw_card(self.deck[0], tiles[FoundationTile.INDEXES[0]], deck_tile)
		events.UserEvent(CustomEvent.FIRST_CARD).post(card=self.deck[0])
		for i in range(1, Deck.DEALT_CARDS - 1):
			self.draw_card(self.deck[i], tiles[TableueTile.INDEXES[i - 1]], deck_tile)
		self.draw_card(self.deck[Deck.DEALT_CARDS - 1], tiles[DiscardTile.INDEX], deck_tile)
		self.active_cards += [i for i in range(Deck.DEALT_CARDS + 1)]
		return self

	def draw_card(self, card, tile, deck_tile):
		tile.lay(card)
		deck_tile.decrement()

	def reset(self):
		self.active_cards.clear()
		for card in self.deck:
			card.tile_index = -1
			card.is_showing = False

	def print_seed(self):
		print('Seed: {0}'.format(self.seed))

	def update(self):
		for i in self.active_cards:
			self.deck[i].update()

	def draw(self, surface):
		for i in self.active_cards:
			self.deck[i].draw(surface)

@class_pause_events_decorator
class CardTile:
	def __init__(self, left_top, size, index, is_visible=True, border=2):
		self.cards = []
		self.index = index 
		self.border = border
		self._set_size(size)
		self._set_position(left_top)
		self.rect = go.Rect(self.left_top, self.size, is_visible, Color.BLACK, self.border)
		self.text = go.RenderText(str(self.index)).center_on(self.center)

	def __str__(self):
		return 'i : {} -> [{}]'.format(self.index, ','.join([str(card) for card in self.cards]))

	def _set_size(self, size):
		self.w, self.h = self.size = size

	def _set_position(self, left_top):
		self.left, self.top = self.left_top = left_top
		self.right, self.bottom =  self.right_bottom = (self.left + self.w, self.top + self.h)
		self.left_bottom = (self.left, self.bottom)
		self.right_top = (self.right, self.top)
		self.x, self.y = self.center = (self.left + self.w // 2, self.top + self.h // 2)

	def set_position(self, left_top):
		self._set_position(left_top)
		self.text.center_on(self.center)
		self.rect.set_position(self.left_top)

	def set_size(self, size):
		self._set_size(size)
		self.rect.set_size(self.size)

	def is_within(self, position):
		return self.rect.is_within(position)

	def can_lay(self, card):
		return False

	def pop(self):
		return self.cards.pop()

	def lay(self, card):
		self.cards.append(card)
		card.put(self)
		card.show()

	def update(self):
		self.rect.update()

	def draw(self, surface):
		self.rect.draw(surface)
		if imp.IMP().debug:
			self.text.draw(surface)

@class_pause_events_decorator
class DeckTile (CardTile):
	INDEX = 0

	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
		self.card_back = pygame.image.load('{0}/{1}'.format(Card.SOURCE_FOLDER, Card.CARD_BACK_IMAGE_FILE)).convert()
		self.deck_count = 52
		self.remaining_text = go.RenderText('{}'.format(self.deck_count)).center_on(self.center)
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.DRAW_ONE).create(self.on_draw_one))

	@function_pause_events_decorator
	def on_draw_one(self, event):
		self.decrement()

	def set_position(self, left_top):
		super().set_position(left_top)
		self.remaining_text.center_on(self.center)

	def update_text(self):
		self.remaining_text.set_text('{}'.format(self.deck_count))

	def reset(self):
		self.deck_count = 52
		self.update_text()

	def decrement(self):
		if self.deck_count > 0:
			self.deck_count -= 1
			self.update_text()

	def draw(self, surface):
		super().draw(surface)
		surface.blit(pygame.transform.scale(self.card_back, (int(self.w), int(self.h))), (int(self.left), int(self.top)))
		self.remaining_text.draw(surface)

class DiscardTile (CardTile):
	INDEX = 1

class BlankTile (CardTile):
	INDEX = 2

	def __init__(self, *args, **kargs):
		super().__init__(*args, is_visible=False, **kargs)

class TableueTile (CardTile):
	INDEXES = [6, 4, 7, 10, 8]

	def can_lay(self, card):
		if any(self.cards):
			prv_card = self.cards[-1]
			if not card.value + 1 == prv_card.value and not (card.value == 13 and prv_card.value == 1):
				return False
		return True

class FoundationTile (CardTile):
	INDEXES = [3, 5, 9, 11]
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs) 
		self.first_card = None
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.FIRST_CARD).create(self.on_first_card))

	@function_pause_events_decorator
	def on_first_card(self, event):
		self.first_card = event.card

	def can_lay(self, card):
		if any(self.cards):
			prv_card = self.cards[-1]
			if card.suit == prv_card.suit and card.value - 1 == prv_card.value or card.value == 1 and prv_card.value == 13:
				return True
		elif self.first_card.value == card.value:
			return True
		return False

	def complete(self):
		return len(self.cards) == Deck.CARD_COUNT

@class_pause_events_decorator
class CardTiles:
	def __init__(self, left_top, table_size, margins):
		self.rows = imp.IMP().config.try_get('GRID_ROWS', 0)
		self.cols = imp.IMP().config.try_get('GRID_COLS', 0)
		self.card_size_ratio = imp.IMP().config.try_get('CARD_SIZE_RATIO', 0.0).solution
		self.tile_info = {}
		self.card_tiles = [] 
		self.parse_tiles()
		self.mw, self.mh = margins
		self.card_width, self.card_height = (0, 0)
		self.fill(*left_top, *table_size)
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_delegate(events.MouseLeftButtonDownEvent().create(self.on_mouse_left_button_down))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.CARD_LAYED).create(self.on_card_layed))

	@function_pause_events_decorator
	def on_mouse_left_button_down(self, event):
		for tile in self.find_all(lambda x : not x == BlankTile.INDEX and not x == DeckTile.INDEX):
			if tile.is_within(event.pos):
				events.UserEvent(CustomEvent.TILE_CLICKED).post(tile=tile, pos=event.pos)
				break
		else:
			deck_tile = self.card_tiles[DeckTile.INDEX]
			if deck_tile.is_within(event.pos):
				events.UserEvent(CustomEvent.DRAW_ONE).post(discard_tile=self.card_tiles[DiscardTile.INDEX])

	@function_pause_events_decorator
	def on_card_layed(self, event):
		selected_card = event.card
		if not selected_card == None:
			max_area = 0
			original_tile = selected_tile = self.card_tiles[selected_card.tile_index]
			for tile in self.find_all(lambda x : not x == BlankTile.INDEX):
				if selected_card.rect.is_intersecting(tile.rect):
					area = selected_card.rect.intersecting(tile.rect).get_area()
					if area > max_area:
						max_area = area
						selected_tile = tile
			original_tile.pop()
			print(selected_tile)
			if selected_tile.can_lay(selected_card):
				selected_tile.lay(selected_card)
			else:
				original_tile.lay(selected_card)

	@function_pause_events_decorator
	def on_resize(self, event):
		pass

	def parse_tiles(self):
		tile_dict = imp.IMP().config.try_get('CARD_TILES', {})
		for tup, tile in tile_dict.items():
			for i in tup:
				self.tile_info[i] = tile 

	def assay(self, half_w, half_h):
		self.card_height = 2 * (half_h - 2 * self.mh) / 3
		temp_cw = self.card_height * self.card_size_ratio
		min_width = (2 * half_w - 5 * self.mw) / 4
		total_width = 4 * temp_cw + 5 * self.mw
		while  total_width > (2 * half_w) and not total_width <= min_width:
			self.card_height -= 10
			temp_cw = self.card_height * self.card_size_ratio
			total_width = 4 * temp_cw + 5 * self.mw
		self.card_width = temp_cw
		self.card_size = (self.card_width, self.card_height)

	def recenter(self, w, h):
		extra_w = (w - (4 * self.card_width  + 5 * self.mw)) // 2
		extra_h = (h - (3 * self.card_height + 4 * self.mh)) // 2 
		for i in range(self.cols):
			for j in range(self.rows):
				card_tile = self.card_tiles[4 * j + i]
				x, y = card_tile.left_top
				card_tile.set_position((x + extra_w, y + extra_h))

	def fill(self, left, top, w, h):
		self.assay(w // 2, h // 2)
		tile_index = 0
		for i in range(self.cols):
			for j in range(self.rows):
				cx = left + i * (self.card_width + self.mw)
				cy = top + j * (self.card_height + self.mh)
				tile = self.tile_info[tile_index]
				module = sys.modules[__name__]
				self.card_tiles.append(tile.instance(module, (cx, cy), self.card_size, tile_index))
				tile_index += 1
		self.recenter(w, h)

	def refill(self, left_top, new_size):
		self.card_tiles.clear()
		self.fill(*left_top, *new_size)

	def find(self, index):
		return self.card_tiles[index]

	def find_all(self, filter=(lambda x : True)):
		return [tile for i, tile in enumerate(self.card_tiles) if filter(i)]

	def update(self):
		for tile in self.card_tiles:
			tile.update()

	def draw(self, surface):
		for tile in self.card_tiles:
			tile.draw(surface)

@class_pause_events_decorator
class CardTable:
	def __init__(self, position, size):
		self.mw, self.mh = imp.IMP().config.try_get('CARD_TABLE_MARGINS', (0, 0))
		self.set_size(size)
		self.set_position(position)
		self.card_tiles = CardTiles(self.left_top, self.size, (self.mw, self.mh)) 
		self.deck = Deck().new_deal(self.card_tiles.find_all())
		self.wire_events()

	def set_size(self, size):
		self.w, self.h = self.size = size 
		self.half_w, self.half_h = self.w / 2, self.h / 2 

	def set_position(self, position):
		x, y = position
		self.origin = position
		self.x, self.y = self.center = (x + self.half_w, y +  self.half_h)
		self.left, self.right = self.mw + x, x + self.w - self.mw
		self.top, self.bottom = self.mh + y, y + self.h - self.mh
		self.left_top = (self.left, self.top)
		self.right_top = (self.right, self.top)
		self.left_bottom = (self.left, self.bottom)  
		self.right_bottom = (self.right, self.bottom)

	def wire_events(self):
		imp.IMP().add_delegate(events.WindowResizeEvent().create(self.on_resize))
		imp.IMP().add_delegate(events.MouseMotion().create(self.on_mouse_motion, quell=True))
		imp.IMP().add_delegate(events.KeyDownEvent(pygame.K_r).create(self.on_new_deal))
		
	@function_pause_events_decorator
	def on_resize(self, event):
		self.set_size((event.w, event.h))
		self.set_position(self.origin)
		self.card_tiles.refill(self.left_top, self.size)
		events.UserEvent(CustomEvent.CARD_TABLE_RESIZE).post(tiles=self.card_tiles.find_all())

	@function_pause_events_decorator
	def on_new_deal(self, event):
		events.UserEvent(CustomEvent.NEW_DEAL).post(tiles=self.card_tiles.find_all())

	@function_pause_events_decorator
	def on_mouse_motion(self, event):
		events.UserEvent(CustomEvent.CARD_MOTION).post(pos=event.pos)

	def update(self):
		self.card_tiles.update()
		self.deck.update()

	def draw(self, surface):
		self.card_tiles.draw(surface)
		self.deck.draw(surface)

if __name__=='__main__':
	pass
