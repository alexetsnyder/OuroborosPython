#structs.py

class Color:
	WHITE  		     = (255, 255, 255, 255)
	BLACK  		     = (  0,   0,   0, 255)
	RED              = (255,   0,   0, 255)
	LIGHT_CORAL      = (240, 128, 128, 255)
	GREEN  		     = (  0, 255,   0, 255)
	LIGHT_SEA_GREEN  = ( 32, 178, 170, 255)
	MEDIUM_SEA_GREEN = ( 60, 179, 113, 255)
	SEA_GREEN        = ( 46, 139,  87, 255)
	DARK_SEA_GREEN   = (143, 188, 143, 255)
	FOREST_GREEN     = ( 13,  55,  13, 255)
	TEAL_FELT        = ( 20, 118,  98, 255)
	BLUE   		     = (  0,   0, 255, 255)
	ALICE_BLUE       = (240, 248, 255, 255)
	DEEP_SKY_BLUE    = (  0, 191, 255, 255)
	YELLOW 		     = (255, 255,   0, 255)
	SAND             = ( 76,  70,  50, 255)
	LIGHT_GREY       = (211, 211, 211, 255)
	SILVER 		     = (192, 192, 192, 255)
	GREY             = (128, 128, 128, 255)
	DIM_GREY         = (105, 105, 105, 255)
	SLATE_GREY       = (112, 128, 144, 255)
	TRANSPARENT      = (  0,   0,   0,   0)

class MouseButton:
	LEFT           = 1
	MIDDLE         = 2
	RIGHT          = 3
	FORWARD_WHEEL  = 4 
	BACKWARD_WHEEL = 5

class CustomEvent:
	REFRESH_SIDEBAR = 20

class WindowSide:
	LEFT   = 0
	RIGHT  = 1
	TOP    = 2
	BOTTOM = 3

class WindowOr:
	VERTICAL   = 0
	HORIZONTAL = 1