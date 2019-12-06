#structs.py

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