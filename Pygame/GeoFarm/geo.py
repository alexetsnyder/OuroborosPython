#geo.py
import pygame
from pygame import freetype

from enums import Color

class Point:
	def __init__(self, pair):
		self = self.to_pair(*pair)

	def to_tuple(self):
		return (self.x, self.y)

	def to_pair(self, x, y):
		self.x = x
		self.w = x
		self.first = x

		self.y = y
		self.w = y
		self.second = y
		return self

class BaseClass:
	def __init__(self, left_top, size):
		self.set_size(size)
		self.set_pos(left_top)

	def set_size(self, size):
		self.w, self.h = self.size = size 

	def set_pos(self, left_top):
		self.left, self.top = self.left_top = left_top
		self.right, self.bottom = self.right_bottom = self.left + self.w, self.top + self.h
		self.left_bottom = self.left, self.bottom
		self.right_top = self.right, self.top 
		self.x, self.y = self.center = self.left + self.w // 2, self.top + self.h // 2

	def center_on(self, center):
		x, y = center 
		self.set_pos((x - self.w // 2, y - self.h // 2))
		return self

class Rect (BaseClass):
	def __init__(self, left_top, size, color):
		super().__init__(left_top, size)
		self.color = color 

	def update(self):
		pass

	def draw_to(self, surface):
		pygame.draw.rect(surface, self.color, pygame.Rect(self.left_top, self.size))

class BorderedRect (Rect):
	def __init__(self, left_top, size, color, width=1):
		super().__init__(left_top, size, color);
		self.width = width

	def draw_to(self, surface):
		super().draw_to(surface)
		pygame.draw.rect(surface, Color.BLACK, pygame.Rect(self.left_top, self.size), self.width)

class FontInfo:
	def __init__(self, font_size=20, font_color=Color.SILVER, font_name='lucidaconsole'):
		self.font_name = font_name
		self.font_size = font_size
		self.font_color = font_color

class RenderText (BaseClass):
	def __init__(self, text_str, font_info=FontInfo()):
		self.text_str = text_str
		self.font_info = font_info
		self.font = freetype.SysFont(self.font_info.font_name, self.font_info.font_size)
		self.set_size()
		self.set_pos((0, 0))

	def set_size(self):
		self.w, self.h = self.size = self.font.get_rect(self.text_str).size 

	def update(self):
		pass

	def draw_to(self, surface):
		self.font.render_to(surface, (self.x - self.w / 2, self.y - self.h / 2), self.text_str, self.font_info.font_color)

if __name__=='__main__':
	pass