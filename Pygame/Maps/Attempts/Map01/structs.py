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
	pass

class WindowSide:
	LEFT   = 0
	RIGHT  = 1
	TOP    = 2
	BOTTOM = 3

class WindowOr:
	VERTICAL   = 0
	HORIZONTAL = 1