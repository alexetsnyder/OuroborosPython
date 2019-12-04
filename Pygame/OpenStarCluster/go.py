#go.py
import pygame
from pygame import freetype
import color

class GameObjects:
	def __init__(self, config):
		self.config = config
		self.game_objects = self.config.try_get('GAME_OBJECTS', [])
		self.look_up_object = {obj.id : obj for obj in self.game_objects}
		self.render_order_attr = self.config.try_get('RENDOR_ORDER_ATTR', '')
		self.sort(self.render_order_attr)
		self.set_parent_all()

	def sort(self, attr, func=(lambda x, y : x > y)):
		if len(self.game_objects) > 1:
			is_done = False
			while not is_done:
				is_done = True
				for i in range(len(self.game_objects) - 1):
					if func(getattr(self.game_objects[i], attr), getattr(self.game_objects[i+1], attr)):
						self.switch(i, i+1)
						is_done = False

	def switch(self, i1, i2):
		self.game_objects[i1], self.game_objects[i2] = self.game_objects[i2], self.game_objects[i1]

	def set_parent_all(self):
		for game_object in self.game_objects:
			game_object.set_parent(self)

	def add(self, object):
		object.set_parent(self)
		self.game_objects.append(object)
		self.sort(self.render_order_attr)
		self.look_up_object[object.id] = object 

	def get_obj(self, id):
		return self.look_up_object[id]

	def get_all(self):
		return self.game_objects

	def find(self, name):
		for obj in self.game_objects:
			if obj.name == name:
				return obj 
		return None 

	def find_all(self, name):
		ret_list = []
		for obj in self.game_objects:
			if obj.name == name:
				ret_list.append(obj)
		return ret_list  

	def update(self):
		for game_object in self.game_objects:
			game_object.update()

	def draw_to(self, surface):
		for game_object in self.game_objects:
			game_object.draw_to(surface)

class GameObject:
	ID = 0

	def __init__(self, name, center, bounds, objects, velocity=(0, 0), render_order=0):
		self.id = GameObject.ID
		self.name = name
		self.parent = None
		self.objects = objects
		self.set_bounds(bounds)
		self.set_center(center)
		self.set_velocity(velocity)
		self.render_order = render_order
		GameObject.ID += 1

	def __str__(self):
		return 'GameObject: (ID: {0}, Name: {1}, Center: {2}, Bounds: {3}, {4})'.format(str(self.id), self.name, self.center, self.bounds, str(self.objects))

	def __repr__(self):
		return 'GameObject: (ID: {0}, Name: {1}, Center: {2}, Bounds: {3}, {4})'.format(str(self.id), self.name, self.center, self.bounds, str(self.objects))

	def set_parent(self, parent_cls):
		self.parent = parent_cls

	def add_object(self, object):
		self.objects.append(object)

	def set_center(self, center):
		self.x, self.y = self.center = center

	def get_center(self):
		return self.center

	def set_velocity(self, velocity):
		self.vx, self.vy = self.velocity = velocity
		for object in self.objects:
			object.set_velocity(velocity)

	def get_velocity(self):
		return self.velocity

	def set_bounds(self, bounds):
		self.width, self.height = self.bounds = bounds

	def get_bounds(self):
		return self.bounds

	def move(self, dx, dy):
		self.x += dx 
		self.y += dy
		self.center = (self.x, self.y)

	def is_within(self, position):
		for object in self.objects:
			if object.is_within(position):
				return True
		return False

	def update(self):
		for object in self.objects:
			object.update()

	def draw_to(self, surface):
		for object in self.objects:
			object.draw_to(surface)

class BaseShape:
	def __init__(self, parent_cls, mod_func=(lambda x, y : (x, y)), velocity=(0, 0), color=color.WHITE):
		self.mod_func = mod_func
		self.parent = parent_cls
		self.set_velocity(velocity)
		self.color = color 

	def __str__(self):
		return '(Center: {0}, Velocity: {1}, Color: {2})'.format(str(self.center), str(self.velocity), str(self.color))

	def __repr__(self):
		return '(Center: {0}, Velocity: {1}, Color: {2})'.format(str(self.center), str(self.velocity), str(self.color))

	def set_func(self, mod_func):
		self.mod_func = mod_func

	def get_center(self):
		return self.mod_func(*self.parent.get_center()) 

	def set_velocity(self, velocity):
		self.vx, self.vy = self.velocity = velocity

	def get_velocity(self):
		return self.velocity

	def get_bounds(self):
		return (0, 0)

	def is_within(self, position):
		return False

	def update(self):
		pass

	def draw_to(self, surface):
		pass

class Circle (BaseShape):
	def __init__(self, parent_cls, radius, velocity=(0, 0), color=color.BLUE, mod_func=(lambda x, y : (x, y))):
		BaseShape.__init__(self, parent_cls, mod_func, velocity, color)
		self.radius = radius
		
	def __str__(self):
		return 'Circle: (Radius: {0}, BaseShape: {1})'.format(str(self.radius), BaseShape.__str__(self))

	def __repr__(self):
		return 'Circle: (Radius: {0}, BaseShape: {1})'.format(str(self.radius), BaseShape.__repr__(self))

	def get_bounds(self):
		return (2 * self.radius, 2 * self.radius)

	def is_within(self, position):
		x, y = position
		h, k = self.get_center()
		return (x - h) ** 2 + (y - k) ** 2 <= self.radius ** 2

	def draw_to(self, surface):
		h, k = self.get_center()
		x = h - self.radius 
		while x < h + self.radius: 
			y = k - self.radius
			while y < k + self.radius:
				if self.is_within((x, y)):
					pygame.draw.rect(surface, self.color, pygame.Rect((x, y), (1, 1)))
				y += 1
			x += 1

class Rectangle (BaseShape):
	def __init__(self, parent, bounds, mod_func=(lambda x, y : (x, y)), velocity=(0, 0), color=color.RED):
		self.width, self.height = self.bounds = bounds
		BaseShape.__init__(self, parent, mod_func, velocity, color)

	def __str__(self):
		return 'Rectangle: (Bounds: {0}, BaseShape: {1})'.format(str(self.bounds), BaseShape.__str__(self))

	def __repr__(self):
		return 'Rectangle: (Bounds: {0}, BaseShape: {1})'.format(str(self.bounds), BaseShape.__repr__(self))

	def set_bounds(self, bounds):
		self.width, self.height = self.bounds = bounds

	def get_bounds(self):
		return self.bounds

	def is_within(self, position):
		x1, y1 = position
		x2, y2 = self.get_center()
		return ((self.width / 2) ** 2 >= (x2 - x1) ** 2) and ((self.height / 2) ** 2 >= (y2 - y1) ** 2)

class Rect (Rectangle):
	def __init__(self, parent, bounds, velocity=(0, 0), color=color.RED, border_width=1, mod_func=(lambda x, y : (x, y))):
		Rectangle.__init__(self, parent, bounds, mod_func, velocity, color)
		self.border_width = border_width

	def __str__(self):
		return 'Rect: (Border Width: {0}, Rectangle: {1})'.format(self.border_width, Rectangle.__str__(self))

	def __repr__(self):
		return 'Rect: (Border Width: {0}, Rectangle: {1})'.format(self.border_width, Rectangle.__repr__(self))	

	def draw_to(self, surface):
		x, y = self.get_center()
		rect = pygame.Rect((x - self.width // 2, y - self.height // 2), self.get_bounds())
		pygame.draw.rect(surface, self.color, rect)
		if self.border_width > 0:
			pygame.draw.rect(surface, color.BLACK, rect, self.border_width)

class FontInfo:
	def __init__(self, font_name, font_size, font_color):
		self.font_name = font_name
		self.font_size = font_size
		self.font_color = font_color

	def __str__(self):
		return 'FontInfo: (Name: {0}, Size: {1}, Color: {2})'.format(self.font_name, str(self.font_size), str(self.font_color))

	def __repr__(self):
		return 'FontInfo: (Name: {0}, Size: {1}, Color: {2})'.format(self.font_name, str(self.font_size), str(self.font_color))

class RenderText (Rectangle):
	def __init__(self, parent, text_str, font_info, velocity=(0, 0), mod_func=(lambda x, y : (x, y))):
		self.text_str = text_str
		self.font_info = font_info
		self.font = freetype.SysFont(self.font_info.font_name, self.font_info.font_size)
		Rectangle.__init__(self, parent, self.get_bounds(), mod_func, velocity, self.font_info.font_color)

	def __str__(self):
		return 'RenderText: (Text: {0}, {1}, Rectangle: {2})'.format(self.text_str, str(self.font_info), Rectangle.__str__(self))

	def __repr__(self):
		return 'RenderText: (Text: {0}, {1}, Rectangle: {2})'.format(self.text_str, str(self.font_info), Rectangle.__repr__(self))

	def set_text(self, text_str):
		self.text_str = text_str
		Rectangle.set_bounds(self, self.get_bounds())

	def set_bounds(self, bounds):
		pass

	def get_bounds(self):
		return (self.font.get_rect(self.text_str).width, self.font.get_rect(self.text_str).height)

	def draw_to(self, surface):
		x, y = self.get_center()
		self.font.render_to(surface, (x - self.width / 2, y - self.height / 2), self.text_str, self.color)
