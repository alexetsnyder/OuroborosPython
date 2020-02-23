#go.py
import pygame
from pygame import freetype
from structs import *

class Rect:
	def __init__(self, left_top, size, color=Color.SILVER, width=0):
		self.width = width 
		self.color = color 
		self.set_size(size)
		self.set_position(left_top)

	def set_size(self, size):
		self.w, self.h = self.size = size 

	def set_position(self, left_top):
		self.left, self.top = self.left_top = left_top
		self.right, self.bottom = self.right_bottom = self.left + self.w, self.top + self.h 
		self.left_bottom = self.left, self.bottom 
		self.right_top = self.right, self.top 
		self.x, self.y = self.center = self.left + self.w // 2, self.top + self.h // 2

	def center_on(self, pos):
		x, y = pos 
		self.set_position((x - self.w // 2, y - self.h // 2))

	def set_color(self, color):
		self.color = color 

	def get_area(self):
		return self.w * self.h

	def is_within(self, position):
		x1, y1 = position
		x2, y2 = self.center
		return (x2 - x1) ** 2 <= (self.w // 2) ** 2 and (y2 - y1) ** 2 <= (self.h // 2) ** 2 

	def is_intersecting(self, r2):
		left = max(self.left, r2.left)
		right = min(self.right, r2.right)
		bottom = min(self.bottom, r2.bottom)
		top = max(self.top, r2.top)
		return left < right and top < bottom

	def intersecting(self, r2):
		left = max(self.left, r2.left)
		right = min(self.right, r2.right)
		bottom = min(self.bottom, r2.bottom)
		top = max(self.top, r2.top)
		return Rect((left, top), (right - left, bottom - top))

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, pygame.Rect(self.left_top, self.size))


class FontInfo:
	def __init__(self, font_size=20, font_color=Color.SILVER, font_name='lucidaconsole'):
		self.font_name = font_name
		self.font_size = font_size
		self.font_color = font_color

class RenderText (Rect):
	def __init__(self, text_str, font_info=FontInfo()):
		if not freetype.get_init():
			freetype.init()
		self.text_str = text_str
		self.font_info = font_info
		self.font = self.create_font()
		super().__init__((0, 0), self.get_size(), color=font_info.font_color)

	def create_font(self):
		return freetype.SysFont(self.font_info.font_name, self.font_info.font_size)

	def set_text(self, text_str):
		self.text_str = text_str
		super().set_size(self.get_size())

	def set_font_size(self, value):
		self.font_info.font_size = value 
		self.font = self.create_font()

	def set_font_name(self, font):
		self.font_info.font_name = font 
		self.font = self.create_font()

	def set_font_info(self, font_info):
		self.font_info = font_info
		self.color = font_info.font_color
		self.font = self.create_font()

	def get_size(self):
		return self.font.get_rect(self.text_str).size 

	def get_font_size(self):
		return self.font_info.font_size

	def draw(self, surface):
		self.font.render_to(surface, self.left_top, self.text_str, self.color)
