#island_map
import go, time
from structs import *
from opensimplex import OpenSimplex
from geo import plottable

class BinaryTree:
	def __init__(self, l):
		self.list = l
		self.sort()
		self.index = len(self.list) // 2
		self.root = self.list[self.index]
		left = self.list[:self.index]
		right = self.list[self.index + 1:]
		self.left = None
		self.right = None
		self.is_leaf = False
		if len(left) > 0:
			self.left = BinaryTree(left)
		if len(right) > 0:
			self.right = BinaryTree(right)
		if self.left == None and self.right == None:
			self.is_leaf = True

	def __str__(self):
		return '[Root: {}, Left: {}, Right: {}]'.format(self.root, str(self.left), str(self.right))
		
	def sort(self):
		is_changed = True
		while is_changed:
			is_changed = False
			for i in range(len(self.list) - 1):
				if self.list[i] > self.list[i + 1]:
					self.list[i], self.list[i + 1] = self.list[i + 1], self.list[i]
					is_changed = True

class List2D:
	def __init__(self, rows, cols):
		self._list = []
		self.rows, self.cols = rows, cols 
		self.generate()

	def __setitem__(self, index, value):
		i, j = index 
		self._list[i][j] = value 

	def __getitem__(self, index):
		i, j = index 
		return self._list[i][j]

	def get_row_stack(self):
		return BinaryTree([x for x in range(self.rows)])

	def get_column_stack(self):
		return BinaryTree([x for x in range(self.cols)])

	def generate(self):
		self.create_rows()
		self.create_columns()

	def create_rows(self, default_value=[]):
		for c in range(self.rows):
			self._list.append(default_value)

	def create_columns(self, default_value=None):
		for i in range(self.rows):
			for j in range(self.cols):
				self._list[i].append(default_value) 

	# def binary_search(self, row_comparer, col_comparer):
	# 	row_stack = [for i in range(self.rows)]
	# 	col_stack = [for j in range(self.cols)]
	# 	center_row, center_col = len(row_stack) // 2, len(col_stack) // 2
	# 	while len(row_stack) > 0 and len(col_stack) > 0:
	# 		left_row_stack, right_row_stack  = row_stack[:center_row], row_stack[center_row:]
	# 		left_col_stack, right_col_stack = col_stack[:center_col], col_stack[center_col:]
	# 		if row_comparer(center_row, center_col):
	# 			row_stack = left_row_stack
	# 		else:
	# 			row_stack = right_row_stack
	# 		if col_comparer(center_row, center_col):
	# 			col_stack = left_col_stack
	# 		else:
	# 			col_stack = right_col_stack
	# 		if len()

	# def insert(i, j, value):
	# 	if i >= len(self._list):
	# 		self.fill_rows(i)
	# 	if j >= len(self._list[i]):
	# 		self.fill_columns(i, j)
	# 	self._list[i][j] = value 

@plottable
class ColorMap:
	def __init__(self, rows, cols):
		self.map = List2D(rows, cols)
		self.scale = 0.007
		self.seed = int(time.time())
		self.simplex = OpenSimplex(self.seed)
		self.rows, self.cols = rows, cols 
		self.tile_width, self.tile_height = self.tile_size = self.h // self.rows, self.w // self.cols 
		self.generate()

	def generate(self):
		for i in range(self.rows):
			for j in range(self.cols):
				left, top = left_top = (j * self.tile_width, i * self.tile_height)
				self.map[(i, j)] = BlockColor(left_top, self.tile_size, self.get_grey_scale(left, top))

	def get_grey_scale(self, x, y):
		n = (self.simplex.noise2d(x * self.scale, y * self.scale) + 1) / 2 * 255
		return (n, n, n)

	def get(self, x, y):
		color_block = self.binary_search(x, y)
		if color_block == None:
			return Color.BLACK 
		return color_block.color

	def binary_search(self, x, y):
		row_stack, col_stack = self.map.get_row_stack(), self.map.get_column_stack()
		while True:
			color_block = self.map[(row_stack.root, col_stack.root)]
			print('({}, {}) <- ({}, {}) '.format(x, y, *color_block.left_top))
			if color_block.bounds((x, y)):
				return color_block
			elif row_stack.is_leaf and col_stack.is_leaf:
				return None
			else:
				if not row_stack.is_leaf:
					row_stack = row_stack.left if y < color_block.top else row_stack.right
				if not col_stack.is_leaf:
					col_stack = col_stack.left if x < color_block.left else col_stack.right
				if col_stack == None or row_stack == None:
					return None

# class ColorMap:
# 	def __init__(self, rows, cols):
# 		self._list = []
# 		self.rows, self.cols = rows, cols 
# 		self.init()

# 	def init(self):
# 		for i in range(self.rows):
# 			self._list.append([])

# 	def __setitem__(self, index, value):
# 		x, y = index 
# 		self._list[x][y] = value   

# 	def __getitem__(self, index):
# 		x, y = index 
# 		return self._list[x][y]

# 	def append(self, x, y, value):
# 		self._list[x].insert(y, value)

# 	def get(self, x, y):
# 		print('get:', x, y)
# 		i = len(self._list) // 2
# 		j = len(self._list[i]) // 2
# 		return self.binary_search(x, y, i, j)

# 	def binary_search(self, x, y, i, j):
# 		if self._list[i][j].bounds((x, y)):
# 			return self._list[i][j]
# 		left, top = self._list[i][j].left_top
# 		print(left, top)
# 		next_i, next_j = self.middle_row_index(left, x, i), self.middle_col_index(top, y, i, j)
# 		return self.binary_search(x, y, next_i, next_j)
		
# 	def middle_row_index(self, left, x, i):
# 		index = len(self._list[i:]) // 2
# 		if (x < left):
# 			index = len(self._list[:i]) // 2
# 		return index 

# 	def middle_col_index(self, top, y, i, j):
# 		index = len(self._list[i][j:]) // 2
# 		if (y < top):
# 			index = len(self._list[i][:j]) // 2
# 		return index

@plottable
class BlockColor:
	def __init__(self, color):
		self.color = color 

	def bounds(self, position):
		x1, y1 = position
		x2, y2 = self.center
		return (x2 - x1) ** 2 <= (self.w // 2) ** 2 and (y2 - y1) ** 2 <= (self.h // 2) ** 2 

@plottable
class IslandMap:
	def __init__(self, rows, cols):
		self.mask = IslandMask(self.center, self.h // 2)
		self.color_map = ColorMap(self.left_top, self.size, rows, cols)
		
	# def refresh(self, left_top, size):
	# 	self.set_size(size)
	# 	self.set_position(left_top)
	# 	self.tile_width = self.w // self.rows
	# 	self.tile_height = self.h // self.cols
	# 	left, top = left_top = self.left_top
	# 	for i in range(self.rows):
	# 		for j in range(self.cols):
	# 			self.color_map[(i, j)].set_position(left_top)
	# 			left, top = left_top = left + self.tile_width, top + self.tile_height 

	def update(self):
		pass

	def draw(self, surface):
		for x in range(self.left, self.right):
			for y in range(self.top, self.bottom):
				surface.set_at((x, y), self.color_map.get(x, y))

class IslandMask:
	def __init__(self, center, radius):
		self.center = center
		self.r = self.radius = radius

	def is_masked(self, x, y):
		v = geo.Vector(x, y) - geo.Vector(*self.center)
		return v.length_sqr() > self.radius ** 2

if __name__=='__main__':
	import sys
	flat_list = [i for i in range(int(sys.argv[1]))]
	print()
	print(flat_list)
	print(BinaryTree(flat_list))