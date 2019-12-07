#go.py
import pygame
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
	def __init__(self, left_top, size, color, width=0):
		self.width = width
		self.set_size(size)
		self.set_color(color)
		self.set_position(left_top)

	def set_size(self, size):
		self.w, self.h = self.size = size

	def set_position(self, left_top):
		self.left, self.top = self.left_top = left_top
		self.right, self.bottom = (self.left + self.w, self.top + self.h)
		self.right_top = (self.right, self.top)
		self.left_bottom = (self.left, self.bottom)
		self.right_bottom = (self.right, self.bottom)
		self.center = self.left + self.w // 2, self.top + self.h // 2

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

	def move(self, dx, dy):
		self.set_position((self.left + dx, self.top + dy))

	def update(self):
		pass

	def draw_at(self, surface, position):
		x, y = position
		pygame.draw.rect(surface, self.color, pygame.Rect((int(x), int(y)), (int(self.w), int(self.h))), self.width)

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, pygame.Rect((int(self.left), int(self.top)), (int(self.w), int(self.h))), self.width)

class FontInfo:
	def __init__(self, font_size=20, font_color=Color.SILVER, font_name='lucidaconsole'):
		self.font_name = font_name
		self.font_size = font_size
		self.font_color = font_color

class RenderText (GeometryObject):
	def __init__(self, text_str, center=(0, 0), font_info=FontInfo()):
		self.text_str = text_str
		self.font_info = font_info
		self.font = freetype.SysFont(self.font_info.font_name, self.font_info.font_size)
		x, y = center
		w, h = self.get_size()
		super().__init__((x - w // 2, y - h // 2), (w, h), font_info.font_color)

	def set_position(self, center):
		x, y = center
		w, h = self.get_size()
		super().set_position((x - w // 2, y - h // 2))

	def set_text(self, text_str):
		self.text_str = text_str
		return self.get_size()

	def get_size(self):
		return self.font.get_rect(self.text_str).size 

	def draw_at(self, surface, center):
		x, y = center
		self.font.render_to(surface, (int(self.left), int(self.top)), self.text_str, self.color)

	def draw(self, surface):
		self.font.render_to(surface, (int(self.left), int(self.top)), self.text_str, self.color)

class Rect (GeometryObject):
	def __init__(self, top_left, size, color=Color.SILVER, width=0):
		super().__init__(top_left, size, color, width)