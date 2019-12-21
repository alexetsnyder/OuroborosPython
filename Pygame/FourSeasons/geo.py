#geo.py

def plottable(cls):
	class PlottableClass (cls):
		def __init__(self, *args, margins=(0, 0), **kargs):
			self.m_w, self.m_h = margins
			super().__init__(*args, **kargs)

		def set_size(self, size):
			self.w, self.h = self.size = size
			self.h_w, self.h_h = self.w // 2, self.h // 2
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

def in_rect(self, rect, position):
	pass

def in_circle(self, circle, position):
	pass

if __name__=='__main__':
	pass