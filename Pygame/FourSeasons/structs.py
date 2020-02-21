#structs.py

class Color:
	WHITE  		  = (255, 255, 255, 255)
	BLACK  		  = (  0,   0,   0, 255)
	RED           = (255,   0,   0, 255)
	GREEN  		  = (  0, 255,   0, 255)
	SEA_GREEN     = ( 46, 139,  87, 255)
	FOREST_GREEN  = ( 13,  55,  13, 255)
	TEAL_FELT     = ( 20, 118,  98, 255)
	BLUE   		  = (  0,   0, 255, 255)
	ALICE_BLUE    = (240, 248, 255, 255)
	DEEP_SKY_BLUE = (  0, 191, 255, 255)
	YELLOW 		  = (255, 255,   0, 255)
	SAND          = ( 76,  70,  50, 255)
	SILVER 		  = (192, 192, 192, 255)
	GREY          = (128, 128, 128, 255)
	TRANSPARENT   = (  0,   0,   0,   0)

class MouseButton:
	LEFT           = 1
	MIDDLE         = 2
	RIGHT          = 3
	FORWARD_WHEEL  = 4 
	BACKWARD_WHEEL = 5

class CustomEvent:
	CARD_TABLE_RESIZED = 0
	TILE_CLICKED       = 1
	CARD_CLICKED       = 2
	CARD_LAYED         = 3
	CARD_MOTION        = 4
	NEW_DEAL           = 5
	FIRST_CARD         = 6
	DRAW_ONE           = 7
	GAME_OVER          = 8
	RESTART            = 9
	PAUSE              = 10
	REDO_STACK_CLEARED = 11
	UNDO_ENABLED       = 12
	REDO_ENABLED       = 14
	UNDO_STACK_CLEARED = 15
	QUICK_LAY          = 16
	TILE_DBL_CLICKED   = 17
	CARD_DROPPED       = 18
	WINNABLE_HANDS     = 19
	REFRESH_SIDEBAR    = 20
	UPDATE_SCORE       = 21

class Suit:
	DIAMONDS = 0
	HEARTS   = 1
	SPADES   = 2
	CLUBS    = 3

SUITS = [Suit.HEARTS, Suit.SPADES, Suit.CLUBS, Suit.DIAMONDS]

SUIT_TO_CHAR = {
 	Suit.DIAMONDS : '♢',
 	Suit.HEARTS   : '♡',
 	Suit.SPADES   : '♤',
	Suit.CLUBS    : '♧' 
}

SUIT_TO_STR = {
 	Suit.DIAMONDS : 'Diamonds',
 	Suit.HEARTS   : 'Hearts',
 	Suit.SPADES   : 'Spades',
	Suit.CLUBS    : 'Clubs' 
}

SUIT_TO_COLOR = {
 	Suit.DIAMONDS : Color.RED,
 	Suit.HEARTS   : Color.RED,
 	Suit.SPADES   : Color.BLACK,
 	Suit.CLUBS    : Color.BLACK 
}

CARD_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

CARD_STR_TO_VAL = {
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

CARD_VAL_TO_STR = {
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

class FSTile:
	TABLEUE_TILE    = 0
	FOUNDATION_TILE = 1
	DECK_TILE       = 2
	DISCARD_TILE    = 3

class WindowSide:
	LEFT   = 0
	RIGHT  = 1
	TOP    = 2
	BOTTOM = 3

class WindowOr:
	VERTICAL   = 0
	HORIZONTAL = 1