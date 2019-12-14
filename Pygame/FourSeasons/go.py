#go.py
import pygame
from pygame import freetype
from structs import *

class Vector:
	def __init__(self, *args):
		self.values = {self.get(i) : args[i] for i in range(len(args))}

	def get(self, index):
		return 'v{0}'.format(index)

	def add_range(self, *args):
		for i in range(len(kargs)):
			self.values[self.get(i)] = args[i]

	def length_sqr(self):
		return sum([self.values[key] ** 2 for key in self.values])

	def __str__(self):
		return '({0})'.format(', '.join(['{0}: {1}'.format(key, self.values[key]) for key in self.values]))

	def __getattr__(self, key):
		return self.values[key]

	def __getitem__(self, index):
		return self.values[self.get(index)]

	def __setitem__(self, index, item):
		self.values[self.get(index)] = item

	def __sub__(self, other):
		new_vector = Vector()
		for key in self.values:
			new_vector.values[key] = self.values[key] - other.values[key]
		return new_vector

class GeometryObject:
	def __init__(self, left_top, size, color, width=0, is_visible=True):
		self.width = width
		self.set_size(size)
		self.set_color(color)
		self.set_position(left_top)
		self.is_visible = is_visible

	def set_size(self, size):
		self.w, self.h = self.size = size

	def set_position(self, left_top):
		self.left, self.top = self.left_top = left_top
		self.right, self.bottom = (self.left + self.w, self.top + self.h)
		self.right_top = (self.right, self.top)
		self.left_bottom = (self.left, self.bottom)
		self.right_bottom = (self.right, self.bottom)
		self.center = self.left + self.w // 2, self.top + self.h // 2

	def center_on(self, position):
		x, y = position
		w, h = self.get_size()
		self.set_position((x - w // 2, y - h // 2))
		return self

	def set_color(self, color):
		self.color = color 

	def set_visibility(self, is_visible):
		self.is_visible = is_visible

	def get_area(self):
		return self.w * self.h

	def get_size(self):
		return self.size 

	def get_color(self):
		if self.is_visible:
			return self.color 
		else:
			return Color.TRANSPARENT

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

	def move(self, dx, dy):
		self.set_position((self.left + dx, self.top + dy))

	def update(self):
		pass

	def draw_at(self, surface, position):
		x, y = position
		pygame.draw.rect(surface, self.get_color(), pygame.Rect((int(x), int(y)), (int(self.w), int(self.h))), self.width)

	def draw(self, surface):
		pygame.draw.rect(surface, self.get_color(), pygame.Rect((int(self.left), int(self.top)), (int(self.w), int(self.h))), self.width)

class FontInfo:
	def __init__(self, font_size=20, font_color=Color.SILVER, font_name='lucidaconsole'):
		self.font_name = font_name
		self.font_size = font_size
		self.font_color = font_color

class RenderText (GeometryObject):
	def __init__(self, text_str, is_visible=True, left_top=(0, 0), font_info=FontInfo()):
		self.text_str = text_str
		self.font_info = font_info
		self.font = self.create_font()
		super().__init__(left_top, self.get_size(), font_info.font_color, 0, is_visible)

	def create_font(self):
		return freetype.SysFont(self.font_info.font_name, self.font_info.font_size)

	def set_position(self, left_top):
		super().set_position(left_top)

	def set_text(self, text_str):
		self.text_str = text_str
		super().set_size(self.get_size())

	def set_font_size(self, value):
		self.font_info.font_size = value 
		self.font = self.create_font()

	def get_size(self):
		return self.font.get_rect(self.text_str).size 

	def get_font_size(self):
		return self.font_info.font_size

	def draw_at(self, surface, center):
		x, y = center
		self.font.render_to(surface, (int(self.left), int(self.top)), self.text_str, self.get_color())

	def draw(self, surface):
		self.font.render_to(surface, (int(self.left), int(self.top)), self.text_str, self.get_color())

class Rect (GeometryObject):
	def __init__(self, top_left, size, is_visible=True, color=Color.SILVER, width=0):
		super().__init__(top_left, size, color, width, is_visible)
