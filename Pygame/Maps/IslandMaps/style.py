#style.py
from structs import *

class Style:
	def __init__(self, color=Color.BLACK, font_size=20, font_name='lucidaconsole'):
		self.color = color 
		self.font_size = font_size
		self.font_name = font_name

styles = {
	'sidebar_enabled'		  : Style(Color.MEDIUM_SEA_GREEN),
	'sidebar_disabled'        : Style(Color.DARK_SEA_GREEN),
	'default_enabled'         : Style(Color.ALICE_BLUE),
	'default_disabled'        : Style(Color.LIGHT_GREY),
	'default_text_enabled'    : Style(Color.BLACK, font_size=10),
	'default_text_disabled'   : Style(Color.DIM_GREY, font_size=10),
	'default_border_enabled'  : Style(Color.BLACK),
	'default_border_disabled' : Style(Color.DIM_GREY),
	'btn_active'              : Style(Color.RED),
	'check_mark_enabled'      : Style(Color.BLACK),
	'check_mark_disabled'     : Style(Color.DIM_GREY),
	'digit_text_enabled'      : Style(Color.RED, font_size=20),
	'digit_text_disabled'     : Style(Color.LIGHT_CORAL, font_size=30),
	'clockback_enabled'       : Style(Color.BLACK),
	'clockback_disabled'      : Style(Color.LIGHT_GREY)
}

class Styles:
	def __init__(self):
		self.map = styles

	def __setitem__(self, key, style_info):
		self.map[key] = style_info

	def __getitem__(self, key):
		return self.map[key]

	def try_get(self, key, default):
		if key in self.map:
			return self.map[key]
		return default

if __name__=='__main__':
	pass