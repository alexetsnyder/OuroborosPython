#go.py
import pygame
from pygame import freetype
from structs import *

def round_up_10(n):
	int_n = int(n)
	mod_10 = int_n % 10
	if not mod_10 == 0:
		int_n += (10 - mod_10)
	return int_n

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

def plottable(cls):
	class PlottableClass (cls):
		def __init__(self, left_top, size, *args, margins=(0, 0), **kargs):
			self.m_w, self.m_h = margins
			self.set_size(size)
			self.set_position(left_top)
			super().__init__(*args, **kargs)

		def set_size(self, size):
			self.w, self.h = self.size = size
			self.h_w, self.h_h = self.w // 2, self.h // 2
			if hasattr(super(), 'set_size'):
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
			if hasattr(super(), 'set_position'):
				super().set_position(left_top)

		def get_size(self):
			if hasattr(super(), 'get_size'):
				return super().get_size()
			return self.size 

		def center_on(self, position):
			x, y = position
			w, h = self.get_size()
			self.set_position((x - w // 2, y - h // 2))
			return self

		def move(self, dx, dy):
			self.set_position((self.left + dx, self.top + dy))
	return PlottableClass

@plottable
class BasicShape:
	def __init__(self, color, is_visible=True):
		self.set_color(color)
		self.set_visibility(is_visible)

	def set_size(self, size):
		self.surface = pygame.Surface(size)
		self.clear(Color.TEAL_FELT)

	def set_color(self, color):
		self.color = color 

	def set_visibility(self, is_visible):
		if not is_visible:
			self.surface.set_alpha(0)
		else:
			self.surface.set_alpha(255)
		self.is_visible = is_visible

	def update(self):
		pass

	def clear(self, color):
		self.surface.fill(color)

	def draw_at(self, surface, position):
		x, y = position
		surface.blit(self.surface, (int(x), int(y)))
		self.clear(Color.TEAL_FELT)

	def draw(self, surface):
		surface.blit(self.surface, pygame.Rect((int(self.left), int(self.top)), (int(self.w), int(self.h))))
		self.clear(Color.TEAL_FELT)

class Rect (BasicShape):
	def __init__(self, left_top, size, width=0, color=Color.SILVER, is_visible=True):
		self.border_width = width 
		super().__init__(left_top, size, color, is_visible)

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

	def get_area(self):
		return self.w * self.h

	def draw_at(self, surface, position):
		pygame.draw.rect(self.surface, self.color, pygame.Rect((0, 0), (int(self.w), int(self.h))), self.border_width)
		super().draw_at(surface, position)

	def draw(self, surface):
		pygame.draw.rect(self.surface, self.color, pygame.Rect((0, 0), (int(self.w), int(self.h))), self.border_width)
		super().draw(surface)

class FontInfo:
	def __init__(self, font_size=20, font_color=Color.SILVER, font_name='lucidaconsole'):
		self.font_name = font_name
		self.font_size = font_size
		self.font_color = font_color

class RenderText (BasicShape):
	def __init__(self, text_str, font_info=FontInfo(), is_visible=True):
		self.text_str = text_str
		self.font_info = font_info
		self.font = self.create_font()
		super().__init__((0, 0), self.get_size(), font_info.font_color, is_visible)

	def set_visibility(self, is_visible):
		self.is_visible = is_visible

	def get_color(self):
		if self.is_visible:
			return self.color 
		else: 
			return Color.TRANSPARENT

	def create_font(self):
		return freetype.SysFont(self.font_info.font_name, self.font_info.font_size)

	def set_text(self, text_str):
		self.text_str = text_str
		super().set_size(self.get_size())

	def set_font_size(self, value):
		self.font_info.font_size = value 
		self.font = self.create_font()

	def set_font_info(self, font_info):
		self.font_info = font_info
		self.font = self.create_font()

	def get_size(self):
		return self.font.get_rect(self.text_str).size 

	def get_font_size(self):
		return self.font_info.font_size

	def draw_at(self, surface, position):
		self.font.render_to(surface, position, self.text_str, self.get_color())

	def draw(self, surface):
		self.font.render_to(surface, self.left_top, self.text_str, self.get_color())
