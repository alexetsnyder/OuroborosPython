#go.py
import pygame
from pygame import freetype
from structs import *
from geo import plottable, Vector

@plottable
class BasicShape:
	def __init__(self, color, is_visible=True):
		self.surface = pygame.Surface(size)
		self.set_color(color)
		self.set_visibility(is_visible)

	def set_size(self, size):
		if hasattr(self, 'surface'):
			self.surface = pygame.Surface(size)

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
		self.set_visibility(self.is_visible)
		super().draw_at(surface, position)

	def draw(self, surface):
		pygame.draw.rect(self.surface, self.color, pygame.Rect((0, 0), (int(self.w), int(self.h))), self.border_width)
		self.set_visibility(self.is_visible)
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
		self.color = font_info.font_color
		self.font = self.create_font()

	def get_size(self):
		return self.font.get_rect(self.text_str).size 

	def get_font_size(self):
		return self.font_info.font_size

	def draw_at(self, surface, position):
		self.font.render_to(surface, position, self.text_str, self.get_color())

	def draw(self, surface):
		self.font.render_to(surface, self.left_top, self.text_str, self.get_color())
