#four_seasons.py
import go, imp, events, acts, fs
import pygame, random, time, sys
from pygame import freetype
from structs import *
from geo import plottable, Vector

@events.pause_events_class
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
		self.card_str = CARD_VAL_TO_STR[self.value]
		self.suit_char = SUIT_TO_CHAR[suit]
		self.suit_str = SUIT_TO_STR[suit] 
		self.suit_color = SUIT_TO_COLOR[suit]
		self.rect = go.Rect((0, 0), (0, 0), is_visible=False)
		self.card_back = pygame.image.load('{0}/{1}'.format(Card.SOURCE_FOLDER, Card.CARD_BACK_IMAGE_FILE)).convert()
		self.card_front = pygame.image.load('{0}/card{1}{2}.png'.format(Card.SOURCE_FOLDER, self.suit_str, self.card_str)).convert()
		self.wire_events()

	def __str__(self):
		return '<{} {}>'.format(self.card_str, self.suit_str)

	def wire_events(self):
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.CARD_MOTION).listen(self.on_card_motion, quell=True))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.CARD_DROPPED).listen(self.on_card_dropped))

	@events.pause_events_method
	def on_card_motion(self, event):
		if self.is_selected:
			new_pos = event.pos 
			v = Vector(*new_pos) - Vector(*self.mouse_pos)
			self.move(v.v0, v.v1)
			self.mouse_pos = new_pos

	@events.pause_events_method
	def on_card_dropped(self, event):
		if self.is_selected:
			events.UserEvent(CustomEvent.CARD_LAYED).post(card=self)
			self.is_selected = False

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

@events.pause_events_class
class Deck:
	def __init__(self):
		self.seed = -1
		self.deck = []
		self.active_cards = []
		self.shuffler = fs.Shuffler()
		self.winnable_hands = False
		self.deal_order = imp.IMP().config.try_get('NEW_DEAL', [])
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.TILE_CLICKED).listen(self.on_tile_clicked))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.TILE_DBL_CLICKED).listen(self.on_tile_dbl_clicked))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.NEW_DEAL).listen(self.on_new_deal))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.RESTART).listen(self.on_restart))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.DRAW_ONE).listen(self.on_draw_one))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.CARD_TABLE_RESIZED).listen(self.on_card_table_resized))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.WINNABLE_HANDS).listen(self.on_winnable_hands))

	def on_winnable_hands(self, event):
		self.winnable_hands = event.winnable_hands

	@events.pause_events_method
	def on_draw_one(self, event):
		if len(self.active_cards) < len(self.deck):
			next_index = len(self.active_cards)
			next_card = self.deck[next_index]
			self.active_cards.append(next_index)
			event.discard_tile.lay(next_card)
			self.update_remaining(event.deck_tile)
			events.UserEvent(CustomEvent.UPDATE_SCORE).post(inc=-1)
			print('Action> Next Card: (#{} {})'.format(next_index, next_card))
			undo_args = (next_index, next_card, event.deck_tile, event.discard_tile)
			undo_action = acts.UndoAction(self.undo_draw, self.redo_draw, *undo_args)
			imp.IMP().actions.post(undo_action)

	def on_new_deal(self, event):
		self.new_deal(event.tiles)
		self.update_remaining(event.deck_tile)

	def on_restart(self, event):
		self.restart(event.tiles)
		self.update_remaining(event.deck_tile)

	@events.pause_events_method
	def on_tile_clicked(self, event):
		for i in reverse(self.active_cards):
			card = self.deck[i]
			if card.tile_index == event.tile.index:
				self.active_cards.remove(i)
				self.active_cards.append(i)
				card.select(event.pos)
				break

	@events.pause_events_method
	def on_tile_dbl_clicked(self, event):
		for i in reverse(self.active_cards):
			card = self.deck[i]
			if card.tile_index == event.tile.index:
				self.active_cards.remove(i)
				self.active_cards.append(i)
				events.UserEvent(CustomEvent.QUICK_LAY).post(card=card)
				break

	def on_card_table_resized(self, event):
		for i in self.active_cards:
			card = self.deck[i]
			tile = event.tiles[card.tile_index]
			tile.lay(card)

	def undo_draw(self, index, card, deck_tile, discard_tile):
		discard_tile.remove(card)
		events.UserEvent(CustomEvent.UPDATE_SCORE).post(inc=-1)
		self.active_cards.remove(index)
		deck_tile.update_text(str(len(self.deck) - len(self.active_cards)))
		print('UndoAction> (#{} {}) {} Left'.format(index, card, len(self.deck) - len(self.active_cards)))

	def redo_draw(self, index, card, deck_tile, discard_tile):
		self.active_cards.append(index)
		events.UserEvent(CustomEvent.UPDATE_SCORE).post(inc=-1)
		discard_tile.lay(card)
		deck_tile.update_text(str(len(self.deck) - len(self.active_cards)))
		print('RedoAction> (#{} {}) {} Left'.format(index, card, len(self.deck) - len(self.active_cards)))

	def update_remaining(self, deck_tile):
		remaining = len(self.deck) - len(self.active_cards)
		deck_tile.update_text(str(remaining))

	def shuffle(self):
		shuffle_state = None
		if self.winnable_hands:
			shuffle_state = self.shuffler.winnable_hand() 
		else: 
			shuffle_state = self.shuffler.random_hand()
		self.deck = shuffle_state.convert(Card, -1)
		for card in self.deck:
			card.is_paused = False

	def restart(self, tiles):
		return self.deal(tiles)

	def new_deal(self, tiles):
		self.shuffle()
		return self.deal(tiles)

	def deal(self, tiles):
		self.reset()
		for i in range(len(self.deal_order)):
			index = self.deal_order[i]
			tiles[index].lay(self.deck[i])
			self.active_cards.append(i)
		return self

	def reset(self):
		self.active_cards.clear()
		for card in self.deck:
			card.tile_index = -1
			card.is_showing = False

	def update(self):
		for i in self.active_cards:
			self.deck[i].update()

	def draw(self, surface):
		for i in self.active_cards:
			self.deck[i].draw(surface)

@plottable
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

	def set_index(self, index):
		self.index = index
		self.text.set_text(str(self.index))

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

	def reset(self):
		self.cards.clear()

	def update(self):
		self.rect.update()

	def draw(self, surface):
		self.rect.draw(surface)
		if imp.IMP().debug:
			self.text.draw(surface)

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
		self.foundation_suit_texts = []
		super().__init__(*args, **kargs) 
		self.first_card = None
		self.font_size = 30
		font_info = go.FontInfo(font_size=self.font_size, font_name=Card.SUIT_FONT, font_color=Color.BLACK)
		self.card_value_text_top = go.RenderText('', is_visible=False, font_info=font_info)
		self.card_value_text_bottom = go.RenderText('', is_visible=False, font_info=font_info) 
		self.creat_suit_emblem()
		self.wire_events()

	def set_position(self, left_top):
		super().set_position(left_top)
		self.postion_suit_emblem()

	def creat_suit_emblem(self):
		for suit in SUITS:
			font_info = go.FontInfo(font_size=self.font_size, font_color=SUIT_TO_COLOR[suit], font_name=Card.SUIT_FONT) 
			self.foundation_suit_texts.append(go.RenderText(SUIT_TO_CHAR[suit], font_info=font_info))

	def postion_suit_emblem(self):
		center_signs = ((-1, -1), (1, -1), (-1, 1), (1, 1))
		for i, suit_text in enumerate(self.foundation_suit_texts):
			sign_x, sign_y = center_signs[i]
			cx, cy = (self.x + sign_x * suit_text.w // 2, self.y + sign_y * suit_text.h // 2)
			if i == 2:
				cy += 2
			elif i == 3:
				cx, cy = (cx + 3, cy + 4)
			suit_text.center_on((cx, cy))

	def wire_events(self):
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.FIRST_CARD).listen(self.on_first_card))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.CARD_TABLE_RESIZED).listen(self.on_card_table_resized))

	def on_first_card(self, event):
		self.first_card = event.card
		self.update_foundation_text()
		self.card_value_text_top.set_visibility(True)
		self.card_value_text_bottom.set_visibility(True)

	def on_card_table_resized(self, event):
		if not self.first_card == None:
			self.update_foundation_text()

	def update_foundation_text(self):
		card_str = self.first_card.card_str
		self.card_value_text_top.set_text(card_str)
		self.card_value_text_top.set_position((self.left + 3, self.top + 3))
		self.card_value_text_bottom.set_text(card_str)
		w, h = self.card_value_text_bottom.size
		self.card_value_text_bottom.set_position((self.right - w - 3, self.bottom - h - 3))

	def can_lay(self, card):
		if any(self.cards):
			prv_card = self.cards[-1]
			if card.suit == prv_card.suit:
				if card.value - 1 == prv_card.value or card.value == 1 and prv_card.value == 13:
					return True
		elif self.first_card.value == card.value:
			return True
		return False

	def lay(self, card):
		if self.first_card == None:
			events.UserEvent(CustomEvent.FIRST_CARD).post(card=card)
		super().lay(card)

	def is_complete(self):
		return len(self.cards) == fs.Shuffler.CARDS_PER_SUIT

	def reset(self):
		super().reset()
		self.first_card = None

	def draw(self, surface):
		super().draw(surface)
		self.card_value_text_top.draw(surface)
		self.card_value_text_bottom.draw(surface)
		for suit_text in self.foundation_suit_texts:
			suit_text.draw(surface)

@plottable
@events.pause_events_class
class CardTable:
	def __init__(self, left_top, size):
		self.click_time = 0
		self.tile_info = {}
		self.card_tiles = [] 
		self.mouse_clicks = []
		self.mouse_unclicks = []
		self.mw, self.mh = self.margins
		self.tile_width, self.tile_height = self.tile_size = (0, 0)
		self.rows = imp.IMP().config.try_get('GRID_ROWS', 0)
		self.cols = imp.IMP().config.try_get('GRID_COLS', 0)
		self.card_size_ratio = imp.IMP().config.try_get('CARD_SIZE_RATIO', 0.0).solution
		self.deck = Deck()			
		self.parse_tiles()	
		self.fill(*left_top, *size)	
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
		imp.IMP().add_delegate(events.MouseLeftButtonDownEvent().listen(self.on_mouse_left_button_down))
		imp.IMP().add_delegate(events.MouseLeftButtonUpEvent().listen(self.on_mouse_left_button_up))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.QUICK_LAY).listen(self.on_quick_lay))
		imp.IMP().add_delegate(events.UserEvent(CustomEvent.CARD_LAYED).listen(self.on_card_layed))

	def on_resize(self, event):
		new_size = (event.w, event.h)
		self.set_size(new_size)
		self.set_position(self.origin)
		self.resize(*self.origin, *new_size)
		events.UserEvent(CustomEvent.CARD_TABLE_RESIZED).post(tiles=self.find_all())

	@events.pause_events_method
	def on_mouse_motion(self, event):
		events.UserEvent(CustomEvent.CARD_MOTION).post(pos=event.pos)

	@events.pause_events_method
	def on_mouse_left_button_down(self, event):
		self.click_time = time.time()
		self.mouse_clicks.append(event.pos)

	@events.pause_events_method
	def on_mouse_left_button_up(self, event):
		self.mouse_unclicks.append(event.pos)

	def process_click(self):
		delta_time = time.time() - self.click_time	
		if len(self.mouse_clicks) > 1:
			self.mouse_unclicks.clear()
			mouse_pos = self.mouse_clicks.pop()
			self.mouse_clicks.pop()
			self.post_tile_dbl_clicked(mouse_pos)
		elif delta_time > 0.30 and any(self.mouse_clicks):
			mouse_pos = self.mouse_clicks.pop()
			self.post_tile_clicked(mouse_pos)

	def process_unclick(self):
		if not any(self.mouse_clicks) and any(self.mouse_unclicks):
			mouse_pos = self.mouse_unclicks.pop()
			events.UserEvent(CustomEvent.CARD_DROPPED).post(pos=mouse_pos)

	def post_tile_dbl_clicked(self, mouse_pos):
		tile = self.get_clicked_tile(mouse_pos)
		if not tile == None and not tile.index == DeckTile.INDEX:
			events.UserEvent(CustomEvent.TILE_DBL_CLICKED).post(tile=tile)

	def post_tile_clicked(self, mouse_pos):
		tile = self.get_clicked_tile(mouse_pos)
		if not tile == None:
			if tile.index == DeckTile.INDEX:
				discard_tile = self.get_discard_tile()
				events.UserEvent(CustomEvent.DRAW_ONE).post(deck_tile=tile, discard_tile=discard_tile)
			else:
				events.UserEvent(CustomEvent.TILE_CLICKED).post(tile=tile, pos=mouse_pos)

	def get_clicked_tile(self, mouse_pos):
		for tile in self.find_all(lambda x : not x == BlankTile.INDEX):
			if tile.is_within(mouse_pos):
				return tile 
		return None

	def find_tile_to_lay(self, card):
		tableue_tiles = []
		for tile in self.find_all(lambda x : not x in [BlankTile.INDEX, DiscardTile.INDEX, DeckTile.INDEX]):
			if tile.can_lay(card):
				if tile.index in FoundationTile.INDEXES:
					return tile 
				tableue_tiles.append(tile)
		if any(tableue_tiles):
			return tableue_tiles[0]
		return None

	@events.pause_events_method
	def on_quick_lay(self, event):
		card = event.card 
		tile = self.find_tile_to_lay(card)
		source_tile = self.card_tiles[card.tile_index]
		if not tile == None:
			source_tile.pop()
			tile.lay(card)
			if not tile.index == source_tile.index:
				self.post_score_update(tile.index)
				print('Action> {} -> {} -> {}'.format(source_tile.index, card, tile))
				undo_args = (source_tile, tile, card)
				undo_action = acts.UndoAction(self.undo_card_layed, self.redo_card_layed, *undo_args)
				imp.IMP().actions.post(undo_action)
			else:
				print('NonAction> {} <- {}'.format(source_tile, card))
			if self.check_win():
				events.UserEvent(CustomEvent.GAME_OVER).post()

	@events.pause_events_method
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
			if not selected_tile.index == original_tile and selected_tile.can_lay(selected_card):
				self.post_score_update(selected_tile.index)
				print('Action> {} -> {} -> {}'.format(original_tile.index, selected_card, selected_tile))
				selected_tile.lay(selected_card)
				undo_args = (original_tile, selected_tile, selected_card)
				undo_action = acts.UndoAction(self.undo_card_layed, self.redo_card_layed, *undo_args)
				imp.IMP().actions.post(undo_action)
			else:
				print('NonAction> {} <- {}'.format(original_tile, selected_card))
				original_tile.lay(selected_card)
			if self.check_win():
				events.UserEvent(CustomEvent.GAME_OVER).post()

	def post_score_update(self, index):
		if index in FoundationTile.INDEXES:
			events.UserEvent(CustomEvent.UPDATE_SCORE).post(inc=10)
		else:
			events.UserEvent(CustomEvent.UPDATE_SCORE).post(inc=-5)

	def undo_card_layed(self, source_tile, dest_tile, card):
		print('UndoAction> {} <- {} <- {}'.format(source_tile, card, dest_tile.index))
		events.UserEvent(CustomEvent.UPDATE_SCORE).post(inc=-1)
		dest_tile.remove(card)
		source_tile.lay(card)

	def redo_card_layed(self, source_tile, dest_tile, card):
		print('RedoAction> {} -> {} -> {}'.format(source_tile.index, card, dest_tile))
		events.UserEvent(CustomEvent.UPDATE_SCORE).post(inc=-1)
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
		self.tile_size = (self.tile_width, self.tile_height)

	def recenter(self, w, h):
		extra_w = (w - (4 * self.tile_width  + 5 * self.mw)) // 2 + self.mw
		extra_h = (h - (3 * self.tile_height + 4 * self.mh)) // 2 + self.mh
		for i in range(self.cols):
			for j in range(self.rows):
				card_tile = self.card_tiles[3 * i + j]
				x, y = card_tile.left_top
				card_tile.set_position((x + extra_w, y + extra_h))

	def fill_tile(self, tile, index, x, y):
		tile.cards.clear()
		tile.set_index(index)
		tile.set_size(self.tile_size)
		tile.set_position((x, y))	

	def resize(self, left, top, w, h):
		self.assay(w // 2, h // 2)
		for i in range(self.cols):
			for j in range(self.rows):
				index = 3 * i + j
				tile = self.card_tiles[index]
				cx = left + i * (self.tile_width + self.mw)
				cy = top + j * (self.tile_height + self.mh)
				self.fill_tile(tile, index, cx, cy)	
		self.recenter(w, h)

	def fill(self, left, top, w, h):
		pass_thr = (0, 0)
		module = sys.modules[__name__]
		for i in range(self.cols):
			for j in range(self.rows):
				tile = self.tile_info[3 * i + j]
				self.card_tiles.append(tile.instance(module, pass_thr, pass_thr, 0))
		self.resize(left, top, w, h)

	def refill(self, left_top, new_size):
		for tile in self.card_tiles:
			tile.reset()
		self.fill(*left_top, *new_size)

	def restart(self):
		self.reset(CustomEvent.RESTART)

	def new_deal(self):
		self.reset(CustomEvent.NEW_DEAL)

	def reset(self, event):
		imp.IMP().actions.clear()
		for tile in self.card_tiles:
			tile.reset()
		events.UserEvent(event).post(tiles=self.find_all(), deck_tile=self.find(DeckTile.INDEX))

	def find(self, index):
		return self.card_tiles[index]

	def find_all(self, filter=(lambda x : True)):
		return [tile for i, tile in enumerate(self.card_tiles) if filter(i)]

	def update(self):
		self.process_click()
		self.process_unclick()
		for tile in self.card_tiles:
			tile.update()
		self.deck.update()

	def draw(self, surface):
		for tile in self.card_tiles:
			tile.draw(surface)
		self.deck.draw(surface)		

if __name__=='__main__':
	pass
