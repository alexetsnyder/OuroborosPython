import pygame
import time, random, string
from pygame import freetype
from opensimplex import OpenSimplex

def test_noise(n):
	max = 0
	min = 5
	p = OpenSimplex()
	for x in range(n):
		for y in range(n):
			tmp = p.noise2d(x, y)
			if tmp > max:
				max = tmp
			if tmp < min:
				min = tmp
	print('max: {0:.3f}, min: {1:.3f}'.format(max, min))

def test_mod(val):
	for i in range(val - 100, val + 101):
		print('{0} : {1} : {2}'.format(i, i % 20, (i - (i%20) if i%20 < 10 else i - ((i%20)-20))))

class Color:
	WHITE  		  = (255, 255, 255)
	BLACK  		  = (  0,   0,   0)
	RED           = (255,   0,   0)
	GREEN  		  = (  0, 255,   0)
	SEA_GREEN     = ( 46, 139,  87)
	FOREST_GREEN  = ( 13,  55,  13)
	BLUE   		  = (  0,   0, 255)
	DEEP_SKY_BLUE = (  0, 191, 255)
	YELLOW 		  = (255, 255,   0)
	SAND          = ( 76,  70,  50)
	SILVER 		  = (192, 192, 192)

class MouseButton:
	LEFT   		  = 1
	MIDDLE 		  = 2
	RIGHT  		  = 3
	FORWARD_WHEEL = 4
	BACK_WHEEL 	  = 5

class FontInfo:
	def __init__(self, font_name, font_size, font_color):
		self.font_name = font_name
		self.font_size = font_size
		self.font_color = font_color

class RenderText:
	def __init__(self, text_str, font_info, position=(0,0)):
		self.text_str = text_str
		self.font_info = font_info
		self.position = position
		self.font = freetype.SysFont(self.font_info.font_name, self.font_info.font_size)
		self.width, self.height = self.bounds = self.get_bounds()

	def set_text(self, text_str):
		self.text_str = text_str
		self.width, self.height = self.bounds = self.get_bounds()

	def get_bounds(self):
		return (self.font.get_rect(self.text_str).width, self.font.get_rect(self.text_str).height)

	def draw_to(self, surface):
		x, y = self.position
		self.font.render_to(surface, (x - self.width / 2, y - self.height / 2), self.text_str, self.font_info.font_color)

class BLOCK:
	def __init__(self, bounds, color):
		self.w, self.h = self.bounds = bounds
		self.color = color 

	def draw_at(self, position, surface):
		pygame.draw.rect(surface, self.color, pygame.Rect(position, self.bounds))
		# pygame.draw.rect(surface, Color.BLACK, pygame.Rect(position, self.bounds), 1)

class Vector:
	def __init__(self, *args):
		self.values = {self.get(i) : args[i] for i in range(len(args))}

	def get(self, index):
		return 'v{0}'.format(index)

	def add_range(self, *args):
		for i in range(len(kargs)):
			self.values[self.get(i)] = args[i]

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

class DrawingObject:
	def __init__(self, position, object):
		self.object = object
		self.position = position
		self.camera_pos = position

	def transform_pos(self, cam_func):
		self.camera_pos = cam_func(self.position)

	def draw_to(self, surface):
		self.object.draw_at(self.camera_pos, surface)

class Camera:
	def __init__(self, surface, position, bounds, step=20):
		self.keys = []
		self.surface = surface
		self.w, self.h = self.bounds = bounds
		self.x, self.y = self.position = position
		self.is_mouse_button_pressed = False
		self.prev_mouse_position = Vector(0, 0)
		self.wheel_arc = 20
		self.step = step
		self.movement = {
						 pygame.K_w : (         0, -self.step), 
						 pygame.K_s : (         0,  self.step),
						 pygame.K_a : (-self.step,  		0),
						 pygame.K_d : ( self.step,  		0)
						}

	def set_rect(self, rect):
		self.set_position(rect.topleft)
		self.set_bounds(rect.size)

	def set_position(self, position):
		self.x, self.y = self.position = position

	def set_bounds(self, bounds):
		self.w, self.h = self.bounds = bounds

	def on_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key in self.movement:
				self.keys.append(event.key)
		elif event.type == pygame.KEYUP:
			if event.key in self.movement:
				self.keys.remove(event.key)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == MouseButton.LEFT:
				self.is_mouse_button_pressed = True
				self.prev_mouse_position = Vector(*event.pos)
			# elif event.button == MouseButton.FORWARD_WHEEL:
			# 	self.surface = pygame.transform.scale(self.surface, tuple(x - self.wheel_arc for x in self.bounds))
			# 	self.set_rect(self.surface.get_rect())
			# 	print(self.position, self.bounds)
			# elif event.button == MouseButton.BACK_WHEEL:
			# 	self.surface = pygame.transform.scale(self.surface, tuple(x + self.wheel_arc for x in self.bounds))
			# 	self.set_rect(self.surface.get_rect())
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == MouseButton.LEFT:
				self.is_mouse_button_pressed = False
		elif event.type == pygame.MOUSEMOTION:
			if self.is_mouse_button_pressed:
				self.move_virtual_window(self.prev_mouse_position - Vector(*event.pos))
				self.prev_mouse_position = Vector(*event.pos)

	def update(self):
		for key in self.keys:
			self.move_virtual_window(Vector(*self.movement[key]))

	def move_virtual_window(self, vec):
		self.x += vec.v0 
		self.y += vec.v1 
		self.position = self.x, self.y

	def in_virtual_window(self, position):
		x, y = position
		return x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h 

	def get_virtual_bounds(self):
		return (self.x, self.y, self.x + self.w, self.y + self.h)

	def virtual_to_win_pos(self, position):
		x, y = position
		return (x - self.x, y - self.y)

	def draw(self, drawing_obects):
		for obj in drawing_obects:
			obj.transform_pos(self.virtual_to_win_pos)
			obj.draw_to(self.surface)

class Map:
	MAP_SIZE = (2000, 2000)
	COLOR_MAP = {
					(  0,  80) : Color.DEEP_SKY_BLUE,
					( 80, 100) : Color.SAND,
					(100, 150) : Color.FOREST_GREEN,
					(150, 180) : Color.SEA_GREEN,
					(180, 255) : Color.SILVER
 				}

	def __init__(self, camera):
		self.map = {}
		self.block_size = 20
		self.camera = camera 
		self.seed = int(time.time())
		print('Seed: {0}'.format(self.seed))
		self.simplex = OpenSimplex(self.seed)
		self.scale = 0.007
		self.generate()

	def on_event(self, event):
		pass

	def generate(self):
		w, h =  Map.MAP_SIZE
		for x in range(-w, w, self.block_size):
			for y in range(-h, h, self.block_size):
				self.map[(x, y)] = BLOCK((self.block_size, self.block_size), self.get_color(x, y))
	
	def round_values(self, values):
		ret_val = []
		for val in values:
			ret_val.append(self.round_to_chunk(val))
		return ret_val

	def round_to_chunk(self, val):
		mod_val = val % self.block_size
		return val - mod_val if mod_val < self.block_size // 2 else val - (mod_val - self.block_size)

	def get_color(self, x, y):
		color = Color.BLACK
		# n = (self.simplex.noise2d(x // self.block_size, y // self.block_size) + 1) / 2 * 255
		n = (self.simplex.noise2d(x * self.scale, y * self.scale) + 1) / 2 * 255
		for key in Map.COLOR_MAP:
			rb, lb = key
			if n >= rb and n < lb:
				color =  Map.COLOR_MAP[key]
				break
		else:
			print('Height map color not found at ({0}, {1}) with n = {2}.'.format(x, y, n))
		return color

	def choose_random_color(self):
		colors = [Color.RED, Color.BLUE, Color.GREEN, Color.SILVER, Color.YELLOW]
		return random.choice(colors)

	def draw(self):
		vx, vy, w, h = self.round_values(self.camera.get_virtual_bounds())
		drawing_objects = []
		for x in range(vx, w, self.block_size):
			for y in range(vy, h, self.block_size):
				if (x, y) in self.map:
					drawing_objects.append(DrawingObject((x, y), self.map[(x, y)]))
		self.camera.draw(drawing_objects)
		#print(len(drawing_objects))

class App:
	WINDOW_SIZE = (1280, 800)

	def __init__(self):
		pygame.init()
		self.running = True
		self.surface = pygame.display.set_mode(App.WINDOW_SIZE, pygame.HWSURFACE)
		self.camera = Camera(self.surface, (0, 0), App.WINDOW_SIZE, 5)
		self.map = Map(self.camera)

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self.running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == MouseButton.FORWARD_WHEEL:
				self.surface = pygame.transform.scale(self.surface, tuple(x // self.camera.wheel_arc for x in self.camera.bounds))
				self.camera.set_rect(self.surface.get_rect())
				print('wheel')
			elif event.button == MouseButton.BACK_WHEEL:
				self.surface = pygame.transform.scale(self.surface, tuple(x * self.camera.wheel_arc for x in self.camera.bounds))
				self.camera.set_rect(self.surface.get_rect())
		self.camera.on_event(event)

	def update(self):
		self.camera.update()

	def draw(self):
		self.surface.fill(Color.BLACK)
		self.map.draw()
		pygame.display.flip()

	def game_loop(self):
		while self.running:
			for event in pygame.event.get():
				self.on_event(event)
			self.update()
			self.draw()

	def clean_up(self):
		pygame.quit()

	def run(self):
		self.game_loop()
		self.clean_up()

if __name__=='__main__':
	app = App()
	app.run()