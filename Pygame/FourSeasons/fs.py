#fs.py
import imp
import random, time
from structs import *

class Card:
	def __init__(self, value, suit):
		self.suit = suit 
		self.value = value

	def __repr__(self):
		return '<{} {}>'.format(CARD_VAL_TO_STR[self.value], SUIT_TO_STR[self.suit])

	def __str__(self):
		return '<{} {}>'.format(CARD_VAL_TO_STR[self.value], SUIT_TO_STR[self.suit])

def copy(src_list):
	return [item for item in src_list]

class WinState:
	def __init__(self):
		self.state = self.randomized_win()
		self.suit_list = [suit for suit in self.state]

	def get_next_card(self):
		if not self.empty():
			random_suit = random.choice(self.suit_list)
			next_val = self.state[random_suit].pop(0)
			if self.is_empty(random_suit):
				self.suit_list.remove(random_suit)
			return Card(next_val, random_suit)

	def is_empty(self, suit):
		return len(self.state[suit]) == 0

	def empty(self):
		return len(self.suit_list) == 0

	def remove(self, key):
		del self.state[key]

	def randomized_win(self):
		random_vals = self.randomize_values()
		random_suits = self.randomize_suits()
		return {suit : copy(random_vals) for suit in random_suits}

	def randomize_suits(self):
		suits_copy = copy(SUITS)
		random.shuffle(suits_copy)
		return suits_copy

	def randomize_values(self):
		random_val = random.choice(CARD_VALUES)
		return CARD_VALUES[random_val:] + CARD_VALUES[:random_val]

class TableueState:
	def __init__(self):
		self.state = {i : [] for i in range(6)}

	def __str__(self):
		return ', '.join(['{} {}'.format(i, self.state[i]) for i in self.state])

	def get_next_card(self):
		tile = self.next_tile()
		if not tile == None:
			return self.state[tile].pop()
		return None

	def next_tile(self):
		tile_list = [tile for tile in self.state]
		while tile_list:
			tile = random.choice(tile_list)
			if not self.is_empty(tile):
				return tile 
			tile_list.remove(tile)
		return None

	def find_available_tile(self, next_card):
		for tile_index in self.state:
			if self.can_lay(tile_index, next_card):
				return tile_index
		return -1

	def can_lay(self, tile_index, next_card):
		if self.is_empty(tile_index):
			return True
		tile_cards = self.state[tile_index]
		last_card = tile_cards[-1]
		if last_card.value > next_card.value or last_card.value == 1 and next_card.value == 13:
			return True
		return False

	def lay(self, card, tile_index):
		self.state[tile_index].append(card)

	def is_empty(self, tile_index):
		return len(self.state[tile_index]) == 0

	def empty(self):
		for tile_index in self.state:
			if not self.is_empty(tile_index):
				return False
		return True

class DiscardState:
	def __init__(self):
		self.state = []

	def __str__(self):
		return ', '.join([str(card) for card in self.state])

	def add(self, card):
		self.state.append(card)

	def clear(self):
		self.state.clear()

	def convert(self, cls, *args):
		conv_list = []
		for card in self.state:
			conv_list.append(cls(card.value, card.suit, *args))
		return conv_list

class Shuffler:
	SUIT_COUNT  = 4
	CARDS_PER_SUIT = 13

	def __init__(self):
		self.deck = DiscardState()

	def random_hand(self):
		self.deck.clear()
		self.create()
		self.shuffle()
		return self.deck

	def winnable_hand(self):
		self.new_seed()
		self.deck.clear()
		win_state = WinState()
		tab_state = TableueState()
		while not win_state.empty() or not tab_state.empty():
			self.backward_action(win_state, tab_state)
		return self.deck

	def backward_action(self, win_state, tab_state):	
		card_from = [FSTile.FOUNDATION_TILE, FSTile.TABLEUE_TILE]
		card_from_weights = [90, 10]
		from_choice = random.choices(card_from, card_from_weights)
		next_card = None
		if from_choice == FSTile.TABLEUE_TILE:
			next_card = tab_state.get_next_card()
			if not next_card == None:
				self.deck.add(next_card)
			else:
				self.foundation_to(win_state, tab_state)
		else:
			if not win_state.empty():
				self.foundation_to(win_state, tab_state)
			else:
				next_card = tab_state.get_next_card()
				if not next_card == None:
					self.deck.add(next_card)

	def foundation_to(self, win_state, tab_state):
		next_card = win_state.get_next_card()
		card_to = [FSTile.DISCARD_TILE, FSTile.TABLEUE_TILE]
		card_to_weights = [1, 99]
		to_choice = random.choices(card_to, card_to_weights)
		tile = tab_state.find_available_tile(next_card)
		if not tile == -1 and to_choice == FSTile.TABLEUE_TILE:
			tab_state.lay(next_card, tile)
		else:
			self.deck.add(next_card)

	def create(self):
		for suit in range(Shuffler.SUIT_COUNT):
			for i in range(1, Shuffler.CARDS_PER_SUIT + 1):
				self.deck.add(Card(i, suit))

	def shuffle(self):
		self.new_seed()
		self.print_seed()
		random.shuffle(self.deck.state)

	def new_seed(self):
		self.seed = int(time.time())
		random.seed(self.seed)

	def print_seed(self):
		print('Seed: {}'.format(self.seed))

if __name__=='__main__':
	print('Win State:')
	win_state = WinState()
	card_list = []
	while True:
		next_card = win_state.get_next_card()
		if next_card == None:
			break
		card_list.append(next_card)
	print(len(card_list))
	for card in card_list:
		print(card)

	print()
	print('Tableue State:')
	tab_state = TableueState()
	a_hearts = Card(Suit.HEARTS, 1)
	tile = tab_state.find_available_tile(a_hearts)
	print(tile)
	tab_state.lay(a_hearts, tile)
	print(tab_state)
	card = tab_state.get_next_card()
	print(card)

	print()
	print('Winnable Shuffle:')
	shuffler = Shuffler()
	shuffle = shuffler.winnable_hand()
	print(len(shuffle.state))
	print(shuffle)

	print()
	print('Random Shuffle:')
	shuffle = shuffler.random_hand()
	print(len(shuffle.state))
	print(shuffle)
	