#geo.py
import pygame
from general import Color
from pygame import freetype

class Paras:
	data = {}

	def __init__(self, *args, **kargs):
		for i in range(len(args)):
			self.data[i] = args[i];
		for key, value in kargs.items():
			self.data[key] = value;

	def try_get(self, key, default):
		if key in self.data:
			return self.data[key];
		return default;

class Plottable:
	def __init__(self, *args, **kargs):
		self.paras = Paras(*args, **kargs)
		self._set_size(self.paras.try_get('size', (0, 0)))
		self._set_pos(self.paras.try_get('left_top', (0, 0)))

	def _set_size(self, size):
		self.w, self.h = self.size = size

	def set_size(self, size):
		self._set_size(size)

	def _set_pos(self, left_top):
		self.left, self.top = self.left_top = left_top
		self.right, self.bottom = self.right_bottom = self.left + self.w, self.top + self.h
		self.right_top = self.right, self.top 
		self.left_bottom = self.left, self.bottom
		self.x, self.y = self.center = self.left + self.w / 2, self.top + self.h / 2

	def set_pos(self, left_top):
		self._set_pos(left_top)

	def _center_on(self, center):
		x, y = center 
		self._set_pos((x - self.w / 2, y - self.h / 2))

	def center_on(self, center):
		self._center_on(center)

class Rect (Plottable):
	def __init__(self, left_top, size, color):
		super().__init__(left_top=left_top, size=size)
		self.color = color

	def draw_to(self, surface):
		pygame.draw.rect(surface, self.color, pygame.Rect(self.left_top, self.size))

class FontInfo:
	def __init__(self, font_size=20, font_color=Color.SILVER, font_name='lucidaconsole'):
		self.font_name = font_name
		self.font_size = font_size
		self.font_color = font_color

class RenderText (Plottable):
	def __init__(self, text_str, *args, font_info=FontInfo(), **kargs):	
		super().__init__(*args, **kargs)
		self.paras = Paras(*args, **kargs);	
		self.text_str = text_str
		self.font_info = font_info
		self.font = freetype.SysFont(self.font_info.font_name, self.font_info.font_size)
		self.set_size(self.font.get_rect(self.text_str).size)
		self.set_pos(self.paras.try_get('left_top', (0, 0)))	

	def set_text(self, text_str):
		self.text_str = text_str
		self.set_size(self.font.get_rect(self.text_str).size)

	def draw_to(self, surface):
		self.font.render_to(surface, (self.left, self.top), self.text_str, self.font_info.font_color)