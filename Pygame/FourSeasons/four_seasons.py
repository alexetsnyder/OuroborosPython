#four_seasons.py
import go, imp, events, trans
import pygame, random, time, sys
from pygame import freetype
from structs import *
from geo import plottable

def pause_events_class(cls):
	class ClassWrapper (cls):
		def __init__(self, *args, **kargs):
			self.is_paused = False
			super().__init__(*args, **kargs)

		def on_pause(self, event):
			self.is_paused = not self.is_paused

		def wire_events(self):
			super().wire_events()
			imp.IMP().add_delegate(events.KeyDownEvent(pygame.K_ESCAPE).listen(self.on_pause))
	return ClassWrapper

def pause_events_method(func):
	def func_wrapper(self, event):
		if not self.is_paused:
			func(self, event)
	return func_wrapper

@pause_events_class
class Card:
	SOURCE_FOLDER = 'Cards'
	CARD_BACK_IMAGE_FILE = 'cardBack_red5.png'
	SUIT_FONT = 'segoeuisymbol'

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
		self.rect = go.Rect((0, 0), (0, 0), is_visible=False)
		self.card_back = pygame.image.load('{0}/{1}'.format(Card.SOURCE_FOLDER, Card.CARD_BACK_IMAGE_FILE)).convert()
		self.card_front = pygame.image.load('{0}/card{1}{2}.png'.format(Card.SOURCE_FOLDER, self.suit_str, self.card_str)).convert()
		self.wire_events()

	def __str__(self):
		return '<{} {}>'.format(self.card_str, self.suit_str)

	def wire_events(self):
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.CARD_MOTION).listen(self.on_card_motion, quell=True))
		imp.IMP().add_delegate(events.MouseLeftButtonUpEvent().listen(self.on_mouse_left_button_up, quell=True))

	@pause_events_method
	def on_card_motion(self, event):
		if self.is_selected:
			new_pos = event.pos 
			v = go.Vector(*new_pos) - go.Vector(*self.mouse_pos)
			self.move(v.v0, v.v1)
			self.mouse_pos = new_pos

	@pause_events_method
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

@pause_events_class
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
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.TILE_CLICKED).listen(self.on_tile_clicked))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.NEW_DEAL).listen(self.on_new_deal))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.RE_DEAL).listen(self.on_redeal))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.DRAW_ONE).listen(self.on_draw_one))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.CARD_TABLE_RESIZED).listen(self.on_card_table_resized))

	@pause_events_method
	def on_draw_one(self, event):
		if len(self.active_cards) < len(self.deck):
			next_index = len(self.active_cards)
			next_card = self.deck[next_index]
			self.active_cards.append(next_index)
			remaining = len(self.deck) - len(self.active_cards)
			event.discard_tile.lay(next_card)
			event.deck_tile.update_text(str(remaining))
			print('Action> Next Card: (#{} {}) and {} Left.'.format(next_index, next_card, remaining))
			undo_args = (next_index, next_card, event.deck_tile, event.discard_tile)
			undo_action = trans.UndoAction(self.undo_draw, self.redo_draw, *undo_args)
			imp.IMP().actions.post(undo_action)

	@pause_events_method
	def on_new_deal(self, event):
		self.new_deal(event.tiles)

	@pause_events_method
	def on_redeal(self, event):
		self.redeal(event.tiles)

	@pause_events_method
	def on_tile_clicked(self, event):
		for i in reverse(self.active_cards):
			card = self.deck[i]
			if card.tile_index == event.tile.index:
				self.active_cards.remove(i)
				self.active_cards.append(i)
				card.select(event.pos)
				break

	def on_card_table_resized(self, event):
		for i in self.active_cards:
			card = self.deck[i]
			tile = event.tiles[card.tile_index]
			tile.lay(card)

	def undo_draw(self, index, card, deck_tile, discard_tile):
		discard_tile.remove(card)
		self.active_cards.remove(index)
		deck_tile.update_text(str(len(self.deck) - len(self.active_cards)))
		print('UndoAction> (#{} {}) {} Left'.format(index, card, len(self.deck) - len(self.active_cards)))

	def redo_draw(self, index, card, deck_tile, discard_tile):
		self.active_cards.append(index)
		discard_tile.lay(card)
		deck_tile.update_text(str(len(self.deck) - len(self.active_cards)))
		print('RedoAction> (#{} {}) {} Left'.format(index, card, len(self.deck) - len(self.active_cards)))

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

	def redeal(self, tiles):
		return self.deal(tiles)

	def new_deal(self, tiles):
		self.shuffle()
		return self.deal(tiles)

	def deal(self, tiles):
		self.reset()
		deck_tile = tiles[DeckTile.INDEX]
		self.draw_card(self.deck[0], tiles[FoundationTile.INDEXES[0]])
		events.UserEvent(CustomEvent.FIRST_CARD).post(card=self.deck[0])
		for i in range(1, Deck.DEALT_CARDS - 1):
			self.draw_card(self.deck[i], tiles[TableueTile.INDEXES[i - 1]])
		self.draw_card(self.deck[Deck.DEALT_CARDS - 1], tiles[DiscardTile.INDEX])
		self.active_cards += [i for i in range(Deck.DEALT_CARDS)]
		deck_tile.update_text(str(len(self.deck) - len(self.active_cards)))
		return self

	def draw_card(self, card, tile):
		tile.lay(card)

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

@plottable
@pause_events_class
class CardTile:
	def __init__(self, left_top, size, index, is_visible=True, border=2):
		self.cards = []
		self.index = index 
		self.border = border
		self.rect = go.Rect(left_top, size, width=self.border, color=Color.BLACK, is_visible=is_visible)
		self.text = go.RenderText(str(self.index))
		self.set_size(size)
		self.set_position(left_top)

	def __str__(self):
		return '{} ∋ ({})'.format(self.index, ', '.join([str(card) for card in self.cards]))

	def set_size(self, size):
		self.rect.set_size(self.size)

	def set_position(self, left_top):
		self.text.center_on(self.center)
		self.rect.set_position(self.left_top)

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

	def remove(self, card):
		self.cards.remove(card)

	def update(self):
		self.rect.update()

	def draw(self, surface):
		self.rect.draw(surface)
		if imp.IMP().debug:
			self.text.draw(surface)

@pause_events_class
class DeckTile (CardTile):
	INDEX = 0

	def __init__(self, *args, **kargs):
		self.remaining_text = go.RenderText('')
		self.card_back = pygame.image.load('{0}/{1}'.format(Card.SOURCE_FOLDER, Card.CARD_BACK_IMAGE_FILE)).convert()
		super().__init__(*args, **kargs)

	def set_position(self, left_top):
		super().set_position(left_top)
		self.remaining_text.center_on(self.center)

	def update_text(self, cards_remaining):
		self.remaining_text.set_text('{}'.format(cards_remaining))
		self.remaining_text.center_on(self.center)

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
		self.font_size = 30
		self.foundation_text = go.RenderText('', is_visible=False)
		self.suits_list = [Suits.HEARTS, Suits.CLUBS, Suits.SPADES, Suits.DIAMONDS]
		self.foundation_suits = []
		for suit in self.suits_list:
			font_info = go.FontInfo(font_size=self.font_size, font_color=SUITS_COLOR[suit], font_name=Card.SUIT_FONT) 
			self.foundation_suits.append(go.RenderText(SUITS_CHAR[suit], font_info=font_info, is_visible=False))
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.FIRST_CARD).listen(self.on_first_card))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.CARD_TABLE_RESIZED).listen(self.on_card_table_resized))

	@pause_events_method
	def on_first_card(self, event):
		self.first_card = event.card
		self.update_foundation_text()
		self.foundation_text.set_visibility(True)
		for suit_text in self.foundation_suits:
			suit_text.set_visibility(True)

	def on_card_table_resized(self, event):
		self.update_foundation_text()

	def update_foundation_text(self):
		font_info = go.FontInfo(font_size=self.font_size, font_name=Card.SUIT_FONT, font_color=self.first_card.suit_color)
		self.foundation_text.set_font_info(font_info)
		self.foundation_text.set_text(self.first_card.card_str)
		self.foundation_text.center_on((self.x, self.y - 10))
		t_w = 0
		for suit_text in self.foundation_suits[:2]:
			t_w += suit_text.w 
		b_w = 0
		for suit_text in self.foundation_suits[2:]:
			b_w += suit_text.w 
		x, y = self.x - t_w // 4, self.y + self.foundation_text.h - 10
		for suit_text in self.foundation_suits[:2]:
			suit_text.center_on((x, y))
			x += suit_text.w 
		x, y = self.x - b_w // 4, y + self.foundation_suits[0].h + 2
		for i, suit_text in enumerate(self.foundation_suits[2:]):
			if i == 0:
				suit_text.center_on((x, y - 2))
			else:
				suit_text.center_on((x, y))
			x += suit_text.w 

	def can_lay(self, card):
		if any(self.cards):
			prv_card = self.cards[-1]
			if card.suit == prv_card.suit and card.value - 1 == prv_card.value or card.value == 1 and prv_card.value == 13:
				return True
		elif self.first_card.value == card.value:
			return True
		return False

	def is_complete(self):
		return len(self.cards) == Deck.CARD_COUNT

	def draw(self, surface):
		super().draw(surface)
		self.foundation_text.draw(surface)
		for suit_text in self.foundation_suits:
			suit_text.draw(surface)

@pause_events_class
class CardTiles:
	def __init__(self, left_top, table_size, margins):
		self.rows = imp.IMP().config.try_get('GRID_ROWS', 0)
		self.cols = imp.IMP().config.try_get('GRID_COLS', 0)
		self.card_size_ratio = imp.IMP().config.try_get('CARD_SIZE_RATIO', 0.0).solution
		self.tile_info = {}
		self.card_tiles = [] 
		self.parse_tiles()
		self.mw, self.mh = margins
		self.tile_width, self.tile_height = self.card_size = (0, 0)
		self.fill(*left_top, *table_size)
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_delegate(events.MouseLeftButtonDownEvent().listen(self.on_mouse_left_button_down))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.CARD_LAYED).listen(self.on_card_layed))

	@pause_events_method
	def on_mouse_left_button_down(self, event):
		for tile in self.find_all(lambda x : not x == BlankTile.INDEX and not x == DeckTile.INDEX):
			if tile.is_within(event.pos):
				events.UserEvent(CustomEvent.TILE_CLICKED).post(tile=tile, pos=event.pos)
				break
		else:
			deck_tile = self.get_deck_tile()
			if deck_tile.is_within(event.pos):
				discard_tile = self.get_discard_tile()
				events.UserEvent(CustomEvent.DRAW_ONE).post(deck_tile=deck_tile, discard_tile=discard_tile)

	@pause_events_method
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
			if selected_tile.can_lay(selected_card):
				print('Action> {} -> {} -> {}'.format(original_tile.index, selected_card, selected_tile))
				selected_tile.lay(selected_card)
				undo_args = (original_tile, selected_tile, selected_card)
				undo_action = trans.UndoAction(self.undo_card_layed, self.redo_card_layed, *undo_args)
				imp.IMP().actions.post(undo_action)
			else:
				print('Action> {} <- {}'.format(original_tile, selected_card))
				original_tile.lay(selected_card)
			if self.check_win():
				events.UserEvent(CustomEvent.GAME_OVER).post()

	def undo_card_layed(self, source_tile, dest_tile, card):
		print('UndoAction> {} <- {} <- {}'.format(source_tile, card, dest_tile.index))
		dest_tile.remove(card)
		source_tile.lay(card)

	def redo_card_layed(self, source_tile, dest_tile, card):
		print('RedoAction> {} -> {} -> {}'.format(source_tile.index, card, dest_tile))
		source_tile.remove(card)
		dest_tile.lay(card)

	def check_win(self):
		win = True
		for i in FoundationTile.INDEXES:
			if not self.card_tiles[i].is_complete():
				win = False
		return win 

	def get_discard_tile(self):
		return self.card_tiles[DiscardTile.INDEX]

	def get_deck_tile(self):
		return self.card_tiles[DeckTile.INDEX]

	def parse_tiles(self):
		tile_dict = imp.IMP().config.try_get('CARD_TILES', {})
		for tup, tile in tile_dict.items():
			for i in tup:
				self.tile_info[i] = tile 

	def assay(self, half_w, half_h):
		self.tile_height = 2 * (half_h - 2 * self.mh) / 3
		temp_cw = self.tile_height * self.card_size_ratio
		min_width = (2 * half_w - 5 * self.mw) / 4
		total_width = 4 * temp_cw + 5 * self.mw
		while  total_width > (2 * half_w) and not total_width <= min_width:
			self.tile_height -= 10
			temp_cw = self.tile_height * self.card_size_ratio
			total_width = 4 * temp_cw + 5 * self.mw
		self.tile_width = temp_cw
		self.card_size = (self.tile_width, self.tile_height)

	def recenter(self, w, h):
		extra_w = (w - (4 * self.tile_width  + 5 * self.mw)) // 2
		extra_h = (h - (3 * self.tile_height + 4 * self.mh)) // 2 
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
				cx = left + i * (self.tile_width + self.mw)
				cy = top + j * (self.tile_height + self.mh)
				tile = self.tile_info[tile_index]
				module = sys.modules[__name__]
				self.card_tiles.append(tile.instance(module, (cx, cy), self.card_size, tile_index))
				tile_index += 1
		self.recenter(w, h)

	def refill(self, left_top, new_size):
		self.card_tiles.clear()
		self.fill(*left_top, *new_size)

	def resize(self, left, top, w, h):
		self.assay(w // 2, h // 2)
		tile_index = 0
		for i in range(self.cols):
			for j in range(self.rows):
				tile = self.card_tiles[tile_index]
				cx = left + i * (self.tile_width + self.mw)
				cy = top + j * (self.tile_height + self.mh)
				tile.cards.clear()
				tile.set_size(self.card_size)
				tile.set_position((cx, cy))	
				tile_index += 1
		self.recenter(w, h)

	def reset(self):
		for tile in self.card_tiles:
			tile.cards.clear()

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

@plottable
@pause_events_class
class CardTable:
	def __init__(self, left_top, size):
		self.card_tiles = CardTiles(left_top, size, (self.m_w, self.m_h)) 
		self.deck = Deck()
		self.set_size(size)
		self.set_position(left_top)
		self.wire_events()	

	def set_size(self, size):
		pass

	def set_position(self, left_top):
		pass

	def wire_events(self):
		imp.IMP().add_delegate(events.WindowResizedEvent().listen(self.on_resize))
		imp.IMP().add_delegate(events.MouseMotionEvent().listen(self.on_mouse_motion, quell=True))
		
	def on_resize(self, event):
		new_size = (event.w, event.h)
		self.set_size(new_size)
		self.set_position(self.origin)
		self.card_tiles.resize(*self.origin, *new_size)
		events.UserEvent(CustomEvent.CARD_TABLE_RESIZED).post(tiles=self.card_tiles.find_all())

	@pause_events_method
	def on_mouse_motion(self, event):
		events.UserEvent(CustomEvent.CARD_MOTION).post(pos=event.pos)

	def redeal(self):
		self.card_tiles.reset()
		imp.IMP().actions.clear()
		events.UserEvent(CustomEvent.RE_DEAL).post(tiles=self.card_tiles.find_all())

	def new_deal(self):
		imp.IMP().actions.clear()
		self.card_tiles.reset()
		events.UserEvent(CustomEvent.NEW_DEAL).post(tiles=self.card_tiles.find_all())

	def update(self):
		self.card_tiles.update()
		self.deck.update()

	def draw(self, surface):
		self.card_tiles.draw(surface)
		self.deck.draw(surface)

if __name__=='__main__':
	pass
