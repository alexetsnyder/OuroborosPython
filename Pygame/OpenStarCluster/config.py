#config.py
import color

class Scope:
	def __init__(self):
		self.scope = {}

	def add(self, key, value):
		self.scope[key] = value

	def try_get(self, key, default):
		if key in self.scope:
			return self.scope[key]
		return default

class KeyValuePair:
	def __init__(self, key=None, value=None):
		self.key = key 
		self.value = value

def split_first(split_str, split_char):
	new_list = split_str.split(split_char)
	key = new_list.pop(0)
	return (key, '{0}'.format(split_char).join(new_list))

class Tokenizer:
	def __init__(self, file, module):
		self.file = file
		self.module = module
		self.scope = Scope()

	def next_token(self):
		convert_data = Convert('=', self.scope, self.module)
		key, data = (None, None)
		line = self.next_line()
		while line != '':
			if not line.isspace() and not line.startswith('#'):
				key, data = tuple(s.strip() for s in split_first(line, '='))
				more_lines = ''
				if data.startswith('[') and not data.endswith(']'):
					more_lines = self.read_to_char(']')
				elif (data.startswith('$') or data.startswith('{')) and not data.endswith('}'):
					more_lines = self.read_to_char('}')
				elif data.startswith('(') and not data.endswith(')'):
					more_lines = self.read_to_char(')')
				data = convert_data.convert('{0} {1}'.format(data, more_lines))	
				break
			line = self.next_line()
		self.scope.add(key, data)
		return KeyValuePair(key, data)

	def next_line(self):
		return self.file.readline()

	def read_to_char(self, end_char):
		aggregate = ''
		for line in self.file:
			aggregate += line.strip() 
			if line.strip().endswith(end_char):
				aggregate = aggregate.strip()
				break 		
		return aggregate

class Convert:
	def __init__(self, split_char, scope, module):
		self.split_char = split_char
		self.module = module
		self.scope = scope

	def convert(self, value):
		value = value.strip()
		data = None
		if value.startswith('['):
			data = [self.replace_and_convert(x, '#', ',') for x in self.split(value, '[]', ',', '#')] 
		elif value.startswith('{'):
			data = {self.replace_and_convert(x, '#', ',') for x in self.split(value, '\{\}', ',', '#')} 
		elif value.startswith('$'):
			key, data = tuple(s.strip() for s in split_first(value, '=')) 
			data = getattr(self.module, key[1:])(*[self.replace_and_convert(x, '#', ',') for x in self.split(data, '\{\}', ',', '#')])
		elif value.startswith('('):
			data = tuple(self.replace_and_convert(x, '#', ',') for x in self.split(value, '()', ',', '#'))
		elif value.startswith('@'):
			data = self.scope.try_get(value[1:].strip('\''), None)
		elif value.isdigit() or value[:1] == '-' and value[1:].isdigit():
			data = int(value)
		elif value.lower() == 'true':
			data = True 
		elif value.lower() == 'false':
			data = False 
		elif value.startswith('|'):
			data = self.convert_math(value.strip('|'))
		elif value.startswith('color.'):
			data = getattr(color, value.split('.')[1].strip())
		elif '.' in value and (lambda x, y : x.isdigit() and y.isdigit)(*tuple(x.strip() for x in value.split('.'))):
			data = float(value)
		else:
			data = value.strip('\'')
		return data

	def replace_and_convert(self, raw_str, char_to_rep, rep_char):
		return self.convert(self.replace_inner_chars(raw_str, char_to_rep, rep_char))

	def split(self, raw_str, outer_strip_chars, split_char, rep_char):
		return self.replace_inner_chars(raw_str.strip(outer_strip_chars), split_char, rep_char).split(split_char)

	def convert_math(self, value):
		new_value = 0
		if '+' in value:
			new_value = (lambda x, y : x + y)(*tuple(int(self.convert(x.strip())) for x in value.split('+'))) 
		elif '-' in value:
			new_value = (lambda x, y : x - y)(*tuple(int(self.convert(x.strip())) for x in value.split('-'))) 
		elif '/' in value:
			new_value = (lambda x, y : x // y)(*tuple(int(self.convert(x.strip())) for x in value.split('/'))) 
		elif '*' in value:
			new_value = (lambda x, y : x * y)(*tuple(int(self.convert(x.strip())) for x in value.split('*'))) 
		return new_value

	def replace_inner_chars(self, raw_str, char_to_rep, rep_char):
		inner = ['{', '(', '[']
		end_inner = ['}', ')', ']'] 
		stack = []
		is_in_quotes = False
		fixed_str = ''
		for c in raw_str:
			new_char = c 
			if c == '\'':
				if is_in_quotes:
					is_in_quotes = False
				else:
					is_in_quotes = True
			elif c in inner:
				stack.append(c)
			elif c in end_inner:
				stack.pop()
			elif len(stack) > 0 or is_in_quotes:
				if c == char_to_rep:
					new_char = rep_char
			fixed_str += new_char
		return fixed_str

class Data:
	def __init__(self, file_path, module):
		self.FILE_PATH = file_path
		self.module = module
		self.data = self.load_from_file()

	def load_from_file(self):
		temp_data = {}
		with open(self.FILE_PATH, 'r') as file:
			tokenizer = Tokenizer(file, self.module)
			while True:
				token = tokenizer.next_token()
				if token.key == None and token.value == None:
					break
				temp_data[token.key] = token.value
		return temp_data

	def __str__(self):
		return '\n'.join(['{0} = {1}'.format(key, self.data[key]) for key in self.data])

	def try_get(self, key, default):
		if key in self.data:
			return self.data[key]
		return default

if __name__=='__main__':
	import pygame
	import Main
	pygame.init()
	config = Data('configdata.txt', Game)
	print(config)
	print()
	print('\n'.join([str(x) for x in config.try_get('game_objects', [])])) 