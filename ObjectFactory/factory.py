#factory.py

class Item:
	def __init__(self, name, weight, price):
		self.name = name 
		self.weight = weight
		self.price = price 

	def __str__(self):
		return 'Name: {0}, Weight: {1}, Price: {2}'.format(self.name, self.weight, self.price)

def split(s, quotes=['\'', '"'], whitespace=[' ', '\n', '\t', '\r\n']):
	in_quotes = False
	current_word = ''
	return_list = []
	for c in s:
		if c in quotes:
			in_quotes = not in_quotes
		elif not in_quotes and c in whitespace:
			return_list.append(current_word)
			current_word = ''
		else:
			current_word += c
	if current_word:
		return_list.append(current_word)
	return return_list

class Object:
	def __init__(self, module, object_list):
		self.module = module
		self.name = object_list[0]
		self.arguments = object_list[1:]

	def instantiate(self):
		return getattr(self.module, self.name)(*self.arguments)

class ObjectFactory:
	def __init__(self, module, file_name):
		self.file_name = file_name
		self.module = module 
		self.objects = []

	def build_objects(self):
		with open(self.file_name, 'r') as f:
			for line in f:
				self.objects.append(Object(self.module, split(line)))

	def instantiate_objects(self):
		return [obj.instantiate() for obj in self.objects]

if __name__=='__main__':
	import sys
	factory = ObjectFactory(sys.modules[__name__], 'data.txt')
	factory.build_objects()
	objects = factory.instantiate_objects()
	for obj in objects:
		print(obj)