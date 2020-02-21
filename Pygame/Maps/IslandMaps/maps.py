#maps.py
import time, math, pygame
import imp, go, events, geo
from geo import plottable
from opensimplex import OpenSimplex
from structs import *

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y 
		
	def get(self):
		return (self.x, self.y)

class Circle:
	def __init__(self, center, radius):
		self.r = self.radius = radius
		self.h, self.k = self.center = center

	def get(self, angle):
		return (self.h + self.r * math.cos(angle), self.k + self.r * math.sin(angle)) 

class CirculerMask:
	def __init__(self, center, radius):
		self.circle = Circle(center, radius)

	def masked(self, x, y):
		v = geo.Vector(x, y) - geo.Vector(*self.circle.center)
		return v.length_sqr() > self.circle.radius ** 2

class Noise:
	def __init__(self, seed, scale = 0.007):
		self.scale = scale
		self.simplex = OpenSimplex(seed)

	def get(self, x, y):
		return self.simplex.noise2d(x * self.scale, y * self.scale) / 2 * 255

	def height(self, x, y):
		return (self.simplex.noise2d(x * self.scale, y * self.scale) + 1) / 2 * 255

class Land:
	VALUES = [
		((0, 50), Color.SAND),
		((50, 100), Color.SEA_GREEN),
		((100, 150), Color.FOREST_GREEN),
		((150, 200), Color.GREY),
		((200, 250), Color.WHITE)
	]

	def __init__(self):
		self.map = {}
		self.reverse = {}
		for (start, end), color in Land.VALUES:
			self.reverse[color] = (start, end)
			for i in range(start, end):
				self.map[i] = color 

	def convert(self, color):
		return self.reverse[color]

	def get(self, noise):
		return self.map[int(noise)]

class MapFill:
	def __init__(self, island_map):
		self.island_map = island_map

	def survey(self):
		rows, cols = self.island_map.rows, self.island_map.cols
		for i in range(rows):
			row, first, last = None, None, None
			for j in range(cols):
				color = self.island_map.get(i, j).color
				if not color == Color.BLUE:
					if row == None:
						row = i
						first = j
					else:
						last = j
			if not row == None and not last == None:
				self.fill(row, first, last)
			
	def fill(self, row, first, last):
		prv_color = self.island_map.get(row, first).color
		for j in range(first, last):
			color = self.island_map.get(row, j).color
			if color == Color.BLUE:
				self.island_map.set(row, j, prv_color)
			else:
				prv_color = color

@plottable
class Tile:
	def __init__(self, color):
		self.color = color 

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, pygame.Rect(self.left_top, self.size))

@plottable
class IslandMap:
	def __init__(self, radius, tile_size):
		self.grid = []
		self.rows, self.cols = 0, 0
		self.tw, self.th = self.tile_size = tile_size
		self.color_map = ColorMap(self.left_top, self.size, radius)
		self.map_fill = MapFill(self)
		self.generate()
		self.refresh(self.size)
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_listener(events.KeyDownEvent(pygame.K_r).listen(self.on_reset))

	def on_reset(self, event):
		self.reset()

	def set_position(self, left_top):
		index = 0
		for i in range(self.left, self.right, self.tw):
			for j in range(self.top, self.bottom, self.th):
				self.grid[index].set_position((i, j))
				index += 1

	def get(self, i, j):
		return self.grid[self.get_index(i, j)]

	def set(self, i, j, color):
		self.grid[self.get_index(i, j)].color = color

	def get_index(self, i, j):
		index = i*self.cols + j
		if index >= len(self.grid):
			print('i: {}, j: {}, rows: {}, cols: {}, index: {}, len(grid): {}'.format(i, j, self.rows, self.cols, index, len(self.grid)))
		return index

	def refresh(self, size):
		self.center_on(tuple(x // 2 for x in size))

	def reset(self):
		self.grid.clear()
		self.color_map.new_map()
		self.generate()

	def generate(self):
		self.rows, self.cols = len(range(self.left, self.right, self.tw)), len(range(self.top, self.bottom, self.th))
		color_left, color_top = self.color_map.left_top
		for i in range(self.left, self.right, self.tw):
			for j in range(self.top, self.bottom, self.th):
				color = self.color_map.get(color_left, color_top)
				self.grid.append(Tile((i, j), self.tile_size, color))
				if i == 120 and j == 640:
					print('i: {}, j: {}, len(grid): {}'.format(i, j, len(self.grid)))
				color_top += self.th
			color_top = self.color_map.top
			color_left += self.tw
		self.map_fill.survey()

	def draw(self, surface):
		#self.color_map.draw(surface)
		for tile in self.grid:
		 	tile.draw(surface)

@plottable
class ColorMap:
	def __init__(self, radius):
		self.scale = 0.007
		self.land = Land()
		self.island_radius = radius
		self.circuler_mask = CirculerMask(self.center, self.island_radius)
		self.map_surface = pygame.Surface(self.size)
		self.new_map()

	def get(self, i, j):
		return self.map_surface.get_at((i, j))

	def set(self, i, j, color):
		self.map_surface.set_at((i, j), color)

	def new_map(self):
		self.seed_noise()
		self.generate()

	def seed_noise(self):
		self.seed_height = int(time.time())
		self.seed_x = int(time.time())
		self.seed_y	= int(time.time())
		self.noise_x = Noise(self.seed_x, self.scale)
		self.noise_y = Noise(self.seed_y, self.scale)
		self.height_map = Noise(self.seed_height, self.scale)

	def generate(self):	
		self.map_surface.fill(Color.BLUE)
		rect = self.map_surface.get_rect()
		for x in range(rect.left, rect.right):
			for y in range(rect.top, rect.bottom):
				if not self.circuler_mask.masked(x, y):
					noise_x = round(self.noise_x.get(x, y))
					noise_y = round(self.noise_y.get(x, y))
					height = self.height_map.height(x, y)
					self.map_surface.set_at((x + noise_x, y + noise_y), self.land.get(height))

	def draw(self, surface):
		surface.blit(self.map_surface, pygame.Rect(self.left_top, self.size))

@plottable
class LineMap:
	def __init__(self, radius):
		self.points = []
		self.radius = radius
		self.sum_x, self.sum_y = 0, 0
		self.count_x, self.count_y = 0, 0
		self.circle = Circle(self.center, self.radius)	
		self.new_map()
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_listener(events.KeyDownEvent(pygame.K_r).listen(self.on_reset))

	def set_position(self, left_top):
		self.circle = Circle(self.center, self.radius)

	def on_reset(self, event):
		self.points.clear()
		self.new_map()

	def seed_noise(self):
		self.seed_x = int(time.time())
		self.seed_y	= int(time.time())
		self.noise_x = Noise(self.seed_x)
		self.noise_y = Noise(self.seed_y)

	def refresh(self, size):
		w, h = size 
		cx, cy = self.center  
		self.set_size((w, h))
		self.center_on((w // 2, h // 2))
		vc = geo.Vector(self.x, self.y) - geo.Vector(cx, cy)
		for i in range(len(self.points)):
			x, y = self.points[i]
			self.points[i] = (x + vc.v0, y + vc.v1)

	def new_map(self):
		self.seed_noise()
		self.generate()

	def generate(self):
		for degree in range(360):
			point = Point(*self.circle.get(degree * math.pi / 180.0))
			noise_x = self.noise_x.get(*point.get())
			noise_y = self.noise_y.get(*point.get())
			self.points.append((point.x + noise_x, point.y + noise_y))

	def draw(self, surface):
		pygame.draw.lines(surface, Color.RED, True, self.points)

if __name__=='__main__':
	pass