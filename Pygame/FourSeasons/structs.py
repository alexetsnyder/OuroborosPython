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