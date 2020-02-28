#go.py
import pygame, imp, style
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

class Line:
	def __init__(self, point1, point2, thickness=1):
		self.thickness = thickness
		self.point1, self.point2 = point1, point2

	def draw(self, surface, color):
		pygame.draw.line(surface, color, self.point1, self.point2, self.thickness)

class HorizontalLine:
	def __init__(self, left_top, width, thickness=1):
		self.width = width 
		self.left, self.top = self.left_top = left_top
		self.line = Line(self.left_top, (self.left + self.width, self.top))
		
	def set_width(self, width):
		self.width = width 
		self.set_line()

	def set_position(self, left_top):
		self.left, self.top = self.left_top = left_top
		self.set_line()

	def set_line(self):
		self.line.point1 = self.left_top
		self.line.point2 = (self.left + self.width, self.top)

	def draw(self, surface, color):
		self.line.draw(surface, color)

class VerticalLine:
	def __init__(self, left_top, height, thickness=1):
		self.height = height
		self.left, self.top = self.left_top = left_top
		self.line = Line(self.left_top, (self.left, self.top + self.height))
		
	def set_height(self, height):
		self.height = height
		self.set_line()

	def set_position(self, left_top):
		self.left, self.top = self.left_top = left_top
		self.set_line()

	def set_line(self):
		self.line.point1 = self.left_top
		self.line.point2 = (self.left, self.top + self.height)

	def draw(self, surface, color):
		self.line.draw(surface, color)

class Rect:
	def __init__(self, left_top = (0, 0), size = (0, 0), width = 0):
		self.width = width 
		Rect.set_size(self, size)
		Rect.set_position(self, left_top)

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

	def move(self, dx, dy):
		self.set_position((self.left + dx, self.top + dy))

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

	def draw(self, surface, color):
		pygame.draw.rect(surface, color, pygame.Rect(self.left_top, self.size), self.width)

class BorderedRect (Rect):
	def __init__(self, left_top, size):
		super().__init__(left_top, size, width=1)
		self.border_color = imp.IMP().styles.try_get('default_border_enabled', style.Style()).color
		self.inner_rect = Rect((self.left + 1, self.top + 1), (self.w - 2, self.h - 2))

	def set_size(self, size):
		super().set_size(size)
		self.inner_rect.set_size((self.w - 2, self.h - 2))

	def set_position(self, left_top):
		super().set_position(left_top)
		self.inner_rect.set_position((self.left + 1, self.top + 1))

	def draw(self, surface, color):
		super().draw(surface, self.border_color)
		self.inner_rect.draw(surface, color)

class RenderText (Rect):
	def __init__(self, text_str, font_style=None):
		if not freetype.get_init():
			freetype.init()
		self.text_str = text_str
		self.font_style = font_style
		self.create_default_style()
		self.font = self.create_font()
		super().__init__((0, 0), self.get_size())

	def create_default_style(self):
		if self.font_style == None:
			self.font_style = imp.Style()

	def create_font(self):
		return freetype.SysFont(self.font_style.font_name, self.font_style.font_size)

	def set_text(self, text_str):
		self.text_str = text_str
		super().set_size(self.get_size())

	def set_font_size(self, value):
		self.font_style.font_size = value 
		self.font = self.create_font()

	def set_font_name(self, font):
		self.font_style.font_name = font 
		self.font = self.create_font()

	def set_font_style(self, font_style):
		self.font_style = font_style
		self.font = self.create_font()

	def get_size(self):
		return self.font.get_rect(self.text_str).size 

	def get_font_size(self):
		return self.font_style.font_size

	def draw_at(self, surface, color, pos):
		self.font.render_to(surface, pos, self.text_str, color)

	def draw(self, surface, color):
		self.font.render_to(surface, self.left_top, self.text_str, color)

if __name__=='__main__':
	pass
