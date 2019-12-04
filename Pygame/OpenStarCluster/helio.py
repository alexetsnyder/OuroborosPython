#osc.py
import pygame
import random
import go, color
from enums import *

class HudInfo (go.GameObject):
	def __init__(self, name, exclude_list=[], text_color=color.FOREST_GREEN, back_color=color.NAVY_BLUE):
		self.max_width = 0
		self.total_height = 0
		self.max_render_order = 0
		self.map_id_to_object = {}
		self.back_color = back_color
		self.exclude_list = exclude_list
		self.font_info = go.FontInfo('lucidaconsole', 20, text_color)
		self.back_panel = go.Rect(self, (0, 0), (0, 0), self.back_color)
		go.GameObject.__init__(self, name, (0, 0), (0, 0), [self.back_panel], (0, 0), 0)

	def format_numbers(self, a, b, c):
		padding_b = 4 - len(str(b))
		padding_c = 4 - len(str(c))
		return 'ID: {0} & Vel: ({1}, {2})'.format(a, ' ' * padding_b + str(b), ' ' * padding_c + str(c))

	def update(self):
		if self.parent:
			self.search_new_objects()
			self.update_hud()
		go.GameObject.update(self)

	def search_new_objects(self):
		if len(self.map_id_to_object) + 1 < len(self.parent.get_all()):
			self.parent.sort('id')
			for game_object in self.parent.get_all():
				id = game_object.id
				if not self.id == id and not game_object.name in self.exclude_list:
					if not id in self.map_id_to_object:
						self.add_hud_text(game_object)
						self.update_rendor_order(game_object.render_order)			
			height = 0
			for hud_text in self.objects[1:]:
				text_height = hud_text.get_bounds()[Bound.HEIGHT]
				hud_text.set_func((lambda h : lambda x, y : (x, y + h))(height + 20 - self.total_height//2 - text_height // 2))
				height += text_height
			self.parent.sort(self.parent.render_order_attr)

	def add_hud_text(self, game_object):
		text_str = self.format_numbers(game_object.id, *game_object.velocity)
		hud_text = go.RenderText(self, text_str, self.font_info, (0, 0))
		self.add_object(hud_text)
		self.map_id_to_object[game_object.id] = hud_text 
		self.total_height += hud_text.get_bounds()[Bound.HEIGHT]

	def update_hud(self):
		for id in self.map_id_to_object:
			object = self.map_id_to_object[id]
			object.set_text(self.format_numbers(id, *self.parent.get_obj(id).get_velocity()))
			new_width = object.get_bounds()[Bound.WIDTH]
			if new_width > self.max_width:
				self.max_width = new_width
		self.back_panel.set_bounds((self.max_width + 10, self.total_height + 10))
		self.set_bounds((self.max_width, self.total_height))
		self.set_center((self.width // 2  + 10, self.height // 2 + 10))

	def update_rendor_order(self, render_order):
		if render_order > self.render_order:
			self.render_order = render_order + 1

class ThreeRects (go.GameObject):
	def __init__(self, name, center, velocity=(0, 0), block_size=20, color=color.GREEN, render_order=0):
		object1 = go.Rect(self, (block_size, block_size), velocity, color, 0, (lambda x, y : (x - block_size // 2, y - block_size // 2)))
		object2 = go.Rect(self, (block_size, block_size), velocity, color, 0, (lambda x, y : (x + block_size // 2, y - block_size // 2)))
		object3 = go.Rect(self, (block_size, block_size), velocity, color, 0, (lambda x, y : (x, y + block_size // 2)))
		go.GameObject.__init__(self, name, center, (2 * block_size, 2 * block_size), [object1, object2, object3], velocity, render_order)

class Ground (go.GameObject):
	def __init__(self, name, center, velocity=(0, 0), block_size=20, color=color.GREEN, render_order=0):
		object = go.Rect(self, (block_size, block_size), velocity, color, 1)
		go.GameObject.__init__(self, name, center, object.get_bounds(), [object], velocity, render_order)

class Player (go.GameObject):
	def __init__(self, name, center, velocity=(0, 0), block_size=20, color=color.RED, render_order=0):
		object = go.Rect(self, (block_size, block_size), velocity, color)
		go.GameObject.__init__(self, name, center, object.get_bounds(), [object], velocity, render_order)

class Star (go.GameObject):
	def __init__(self, name, center, radius, velocity=(0, 0), color=color.BLUE, render_order=0):
		object = go.Circle(self, radius, velocity, color)
		go.GameObject.__init__(self, name, center, object.get_bounds(), [object], velocity, render_order)

#Questions of set_center every time it moves?
class MovingText (go.GameObject):
	def __init__(self, name, text_str='', center=(0,0), velocity=(0, 0), color=color.WHITE, render_order=0):
		object = go.RenderText(self, text_str, go.FontInfo('lucidaconsole', 20, color), velocity)
		go.GameObject.__init__(self, name, center, object.get_bounds(), [object], velocity, render_order)

	def set_text(self, text_str):
		self.objects[0].set_text(text_str)

class ToolTip (go.GameObject):
	def __init__(self, name, text_str='', center=(0,0), velocity=(0, 0), color=color.WHITE, render_order=0):
		object = go.RenderText(self, text_str, go.FontInfo('lucidaconsole', 20, color), velocity)
		go.GameObject.__init__(self, name, center, object.get_bounds(), [object], velocity, render_order)

	def set_text(self, text_str):
		self.objects[0].set_text(text_str)
		w, h = self.objects[0].get_bounds()
		self.objects[0].mod_func = lambda x, y : (x + w // 2 + 10, y + h // 2)

	def set_center(self, center):
		x, y = center
		w, h = self.objects[0].get_bounds()
		go.GameObject.set_center(self, center)

class WorldGen:
	def __init__(self, world_center, radius, window_dimensions, block_size=20):
		self.x, self.y = self.world_center = world_center
		self.width, self.height = self.window_dimensions = window_dimensions
		self.block_size = block_size
		self.radius = radius

	def __repr__(self):
		return '({0}, {1}, {2}, {3})'.format(self.world_center, self.radius, self.window_dimensions, self.block_size)

	def generate(self, current_center):
		game_objects = []	
		circle = GameObject.Circle(self.world_center, self.radius)
		for x in range(self.x-self.width//2, self.x+self.width//2, self.block_size):
			for y in range(self.y-self.height//2, self.y+self.height//2, self.block_size):
				if circle.is_within((x, y)):
					game_objects.append(GameObject.Ground((x, y), self.block_size, color.BROWN))
		return game_objects

class EventManager:
	def __init__(self, game_objects):
		self.frame = 0
		self.key_press = []
		self.game_objects = game_objects

	def on_event(self, event):
		if event.type == pygame.KEYDOWN:
			self.key_press.append(event.key)
		elif event.type == pygame.KEYUP:
			self.key_press.remove(event.key)
			if event.key == pygame.K_EQUALS or event.key == pygame.K_MINUS or event.key == pygame.K_r:
				self.frame = 0
		elif event.type == pygame.MOUSEMOTION:
			mouse_pos = pygame.mouse.get_pos()
			tool_tip = self.game_objects.find('tooltipid')
			if not tool_tip == None:
				for game_object in self.game_objects.get_all():
					if not game_object.name == 'tooltipid' and game_object.is_within(mouse_pos):
						tool_tip.set_text('ID: {0}'.format(game_object.id))
						tool_tip.set_center(mouse_pos)
						break
				else:
					tool_tip.set_text('')

	def mod_vel(self, v, mod):	
		if mod < 0 and v < 0 or mod > 0 and v < 0:
			mod = -mod 
		elif mod < 0 and v == 0:
			mod = 0
		return v + mod

	def update(self):
		player = self.game_objects.find('Player')
		if not player == None:
			player.set_velocity((0, 0))
			for key in self.key_press:
				self.parse_key(player, key)

	def parse_key(self, object, key):
		vx, vy = object.get_velocity()
		if key == pygame.K_d:
			object.set_velocity((4,  vy))
		elif key == pygame.K_a:
			object.set_velocity((-4, vy))
		elif key == pygame.K_w:
			object.set_velocity((vx, -4))
		elif key == pygame.K_s:
			object.set_velocity((vx,  4))
		elif key == pygame.K_EQUALS:
			if self.frame % 8 == 0:
				for game_object in self.game_objects.get_all():
					if not game_object.name in ['Player', 'tooltipid']:
						vx, vy = game_object.get_velocity()
						game_object.set_velocity((self.mod_vel(vx, 1), self.mod_vel(vy, 1)))
			self.frame += 1
		elif key == pygame.K_MINUS:
			if self.frame % 8 == 0:
				for game_object in self.game_objects.get_all():
					if not game_object.name in ['Player', 'tooltipid']:
						vx, vy = game_object.get_velocity()
						game_object.set_velocity((self.mod_vel(vx, -1), self.mod_vel(vy, -1)))
			self.frame += 1
		elif key == pygame.K_r:
			if self.frame % 8 == 0:
				for game_object in self.game_objects.get_all():
					if not game_object.name == 'tooltipid':
						game_object.set_velocity((random.choice([-1, 1]), random.choice([-1, 1])))
			self.frame += 1

if __name__=='__main__':
	pass