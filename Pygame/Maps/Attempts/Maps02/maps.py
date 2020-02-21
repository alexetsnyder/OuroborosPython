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
		return (self.simplex.noise2d(x * self.scale, y * self.scale) + 1) / 2 * 255

@plottable
class IslandMap:
	def __init__(self):
		self.pixels = []
		self.scale = 0.007
		self.circuler_mask = CirculerMask(self.center, 200)
		self.seed_noise()
		self.wire_events()
		self.generate()

	def wire_events(self):
		imp.IMP().add_listener(events.KeyDownEvent(pygame.K_r).listen(self.on_refresh))
		imp.IMP().add_listener(events.KeyDownEvent(pygame.K_EQUALS).listen(self.on_plus_scale))
		imp.IMP().add_listener(events.KeyDownEvent(pygame.K_MINUS).listen(self.on_minus_scale))

	def on_refresh(self, event):
		self.pixels.clear()
		self.seed_noise()
		self.generate()

	def on_plus_scale(self, event):
		self.scale += 0.001
		print('Scale: {}'.format(self.scale))

	def on_minus_scale(self, event):
		self.scale -= 0.001
		print('Scale: {}'.format(self.scale))

	def seed_noise(self):
		self.seed_x = int(time.time())
		self.seed_y	= int(time.time())
		self.noise_x = Noise(self.seed_x, self.scale)
		self.noise_y = Noise(self.seed_y, self.scale)

	def generate(self):
		for x in range(self.w):
			for y in range(self.h):
				if not self.circuler_mask.masked(x, y):
					noise_x = self.noise_x.get(x, y)
					noise_y = self.noise_y.get(x, y)
					self.pixels.append(((x + noise_x, y + noise_y), Color.RED))

	def draw(self, surface):
		for (x, y), color in self.pixels:
			surface.set_at((int(x), int(y)), color)

@plottable
class LineMap:
	def __init__(self):
		self.points = []
		self.circle = Circle(self.center, 200)
		self.sum_x, self.sum_y = 0, 0
		self.count_x, self.count_y = 0, 0
		self.seed_noise()	
		self.wire_events()
		self.generate()

	def wire_events(self):
		imp.IMP().add_listener(events.KeyDownEvent(pygame.K_r).listen(self.on_refresh))

	def on_refresh(self, event):
		self.points.clear()
		self.seed_noise()
		self.generate()

	def seed_noise(self):
		self.seed_x = int(time.time())
		self.seed_y	= int(time.time())
		self.noise_x = Noise(self.seed_x)
		self.noise_y = Noise(self.seed_y)

	def generate(self):
		for degree in range(360):
			point = Point(*self.circle.get(degree * math.pi / 180.0))
			noise_x = self.noise_x.get(*point.get())
			noise_y = self.noise_y.get(*point.get())
			self.record(noise_x, noise_y)
			self.points.append((point.x + noise_x, point.y + noise_y))
		self.recenter()

	def record(self, x, y):
		self.count_x += 1
		self.count_y += 1
		self.sum_x += x
		self.sum_y += y

	def recenter(self):
		ave_x, ave_y = self.sum_x / self.count_x, self.sum_y / self.count_y
		print('Average X: {}, Average Y: {}'.format(ave_x, ave_y))
		for i in range(len(self.points)):
			x, y = self.points[i]
			self.points[i] = (x - ave_x, y - ave_y)

	def draw(self, surface):
		pygame.draw.lines(surface, Color.RED, True, self.points)

if __name__=='__main__':
	pass