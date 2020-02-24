#go.py
import pygame
from pygame import freetype
from structs import *

def plottable(cls):
	class PlottableClass (cls):
		def __init__(self, left_top, size, *args, margins=(0, 0), **kargs):
			self.m_w, self.m_h = self.margins = margins
			self.loading = True
			self.set_size(size)
			self.set_position(left_top)
			self.loading = False
			if hasattr(super(), '__init__'):
				super().__init__(*args, **kargs)

		def set_size(self, size):
			self.w, self.h = self.size = size
			self.h_w, self.h_h = self.w // 2, self.h // 2
			if not self.loading and hasattr(super(), 'set_size'):
				super().set_size(size)

		def set_position(self, left_top):
			left, top = self.origin = left_top
			self.left, self.right = left + self.m_w, left + self.w - self.m_w 
			self.top, self.bottom = top + self.m_h, top + self.h - self.m_h 
			self.left_top = (self.left, self.top)
			self.left_bottom = (self.left, self.bottom)
			self.right_top = (self.right, self.top)
			self.right_bottom = (self.right, self.bottom) 
			self.x, self.y = self.center = self.left + self.h_w, self.top + self.h_h
			if not self.loading and hasattr(super(), 'set_position'):
				super().set_position(left_top)

		def get_size(self):
			if hasattr(super(), 'get_size'):
				return super().get_size()
			return self.size 

		def center_on(self, position):
			x, y = position
			w, h = self.get_size()
			self.set_position((x - w // 2, y - h // 2))
			if hasattr(super(), 'center_on'):
				return super().center_on(self.left_top)
			return self

		def move(self, dx, dy):
			self.set_position((self.left + dx, self.top + dy))
			if hasattr(super(), 'move'):
				super().move(dx, dy)
	return PlottableClass

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
		self.line.point2 = (self.left + self.height, self.top)

	def draw(self, surface, color):
		self.line.draw(surface, color)

class Rect:
	def __init__(self, left_top, size, width=0):
		self.width = width 
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

	def draw_at(self, surface, color, pos):
		left, top = pos
		pygame.draw.rect(surface, color, pygame.Rect((left - self.w // 2, right - self.h // 2), self.size))

	def draw(self, surface, color):
		pygame.draw.rect(surface, color, pygame.Rect(self.left_top, self.size))

class FontInfo:
	def __init__(self, font_size=20, font_name='lucidaconsole'):
		self.font_name = font_name
		self.font_size = font_size

class RenderText (Rect):
	def __init__(self, text_str, font_info=FontInfo()):
		if not freetype.get_init():
			freetype.init()
		self.text_str = text_str
		self.font_info = font_info
		self.font = self.create_font()
		super().__init__((0, 0), self.get_size())

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
		self.font = self.create_font()

	def get_size(self):
		return self.font.get_rect(self.text_str).size 

	def get_font_size(self):
		return self.font_info.font_size

	def draw_at(self, surface, color, pos):
		self.font.render_to(surface, pos, self.text_str, color)

	def draw(self, surface, color):
		self.font.render_to(surface, self.left_top, self.text_str, color)
