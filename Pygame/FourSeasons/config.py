#config.py
import traceback

WHITE_SPACE = ' \n\t'

class TypeError (Exception):
	pass

class BoolTypeError (TypeError):
	pass

class InvalidOperatorError (Exception):
	pass

class StringWrapper:
	def __init__(self, string):
		self.string = string.strip(WHITE_SPACE)

	def __str__(self):
		return self.string

	def __getattr__(self, attr):
		return getattr(self.string, attr)

	def __getitem__(self, item):
		return StringWrapper(self.string.__getitem__(item))

	def length(self):
		return len(self.string)

	def is_list(self):
		return self.string.startswith('[') and self.string.endswith(']')

	def is_dict(self):
		return self.string.startswith('{') and self.string.endswith('}')

	def is_tuple(self):
		return self.string.startswith('(') and self.string.endswith(')')

	def contains(self, patern_str):
		return patern_str in self.string

	def is_number(self):
		return self.is_int() or self.is_float()

	def is_int(self):
		return self.string.isdigit()

	def is_float(self):
		if self.contains('.'):
			index = self.string.index('.')
			if self.string[index + 1:].isdigit() and self.string[:index].isdigit():
				return True
		return False

	def is_bool(self):
		if self.string.lower() == 'true' or self.string.lower() == 'false':
			return True 
		return False

	def parse_int(self):
		return int(self.string)

	def parse_float(self):
		return float(self.string)

	def parse_bool(self):
		if self.string.lower() == 'true':
			return True
		elif self.string.lower() == 'false':
			return False 
		raise BoolTypeError()

	def get_strip_str(self, enclosed_chars):
		return '{0}{1}'.format(WHITE_SPACE, enclosed_chars)

	def split_first(self, split_str, enclosed_chars='\'"'):
		is_enclosed = False
		current_word = ''
		strip_chars = ' {0}'.format(enclosed_chars)
		first, second = '', ''
		for i, c in enumerate(self.string):
			if c in enclosed_chars:
				is_enclosed = not is_enclosed
			else:
				if c == split_str:
					first, second = current_word.strip(strip_chars), self.string[i+1:].strip(strip_chars) 
					break
			current_word += c
		return (first.strip(WHITE_SPACE), StringWrapper(second.strip(WHITE_SPACE)))

	def split(self, split_str, enclosed_chars='\'"'):
		is_enclosed = False
		current_word = ''
		word_list = []
		for c in self.string:
			if c == split_str and not is_enclosed:
				word_list.append(current_word.strip(WHITE_SPACE))
				current_word = ''
			else:
				current_word += c
				if c in enclosed_chars:
					is_enclosed = not is_enclosed
		if current_word:
			word_list.append(current_word.strip(WHITE_SPACE))
		return word_list

class ObjectContainer:
	def __init__(self, type, parameters):
		self.type = type
		self.parameters = parameters

	def __repr__(self):
		return '{0}{1}'.format(self.type, self.parameters)

	def __str__(self):
		return '{0}{1}'.format(self.type, self.parameters)

	def set_parameters(self, parameters):
		self.parameters = parameters

	def instance(self, parent):
		return getattr(parent, self.type)(*self.parameters) 

class MathContainer:
	MATH_OPERATORS = '-+/*'

	def __init__(self, arith_str):
		self.original = arith_str
		self.solution = self.solve(self.original)

	def __repr__(self):
		return '{0} = {1}'.format(self.original, self.solution)

	def __repr__(self):
		return '{0} = {1}'.format(self.original, self.solution)

	def next_op():
		for op in MathContainer.MATH_OPERATORS:
			yield op  

	def next_index(arith_str):
		for op in MathContainer.next_op():
			index = arith_str.find(op)
			if not index == -1:
				return index 
		return -1

	def is_arithmatic(arith_str):
		index = MathContainer.next_index(arith_str)
		if not index == -1:
			return MathContainer.is_arithmatic(arith_str[:index]) and MathContainer.is_arithmatic(arith_str[index + 1:])
		return arith_str.is_number()

	def solve(self, arith_str):
		index = MathContainer.next_index(arith_str)
		if not index == -1:
			op = arith_str[index].strip(WHITE_SPACE)
			return self.operator(op, arith_str[:index], arith_str[index + 1:])
		return self.parse_number(arith_str)

	def parse_number(self, arith_str):
		if arith_str.is_int():
			return arith_str.parse_int()
		else:
			return arith_str.parse_float()

	def operator(self, op, ls, rs):
		if op == '+':
			return self.solve(ls) + self.solve(rs)
		elif op == '-':
			return self.solve(ls) - self.solve(rs)
		elif op == '*':
			return self.solve(ls) * self.solve(rs)
		elif op == '/':
			return self.solve(ls) / self.solve(rs)
		else:
			raise InvalidOperatorError('Operator: {0}'.format(op))

class Convert:
	def __init__(self, data_history):
		self.line_number = 1
		self.data_history = data_history

	def convert(self, data_str, strip_chars='{0}\'"'.format(WHITE_SPACE)):
		data_str = StringWrapper(data_str.strip(strip_chars))
		data = None
		if data_str.is_list():
			data = self.convert_list(data_str)
		elif data_str.is_dict():
			data = self.convert_dict(data_str)
		elif data_str.is_tuple():
			data = self.convert_tuple(data_str)
		elif data_str.is_bool():
			data = data_str.parse_bool()
		elif data_str.is_float():
			data = data_str.parse_float()
		elif data_str.is_int():
			data = data_str.parse_int()
		elif self.is_object(data_str):
			data = self.convert_object(data_str)
		elif self.is_var(data_str):
			data = self.replace_var(data_str)
		elif self.is_arithmatic(data_str):
			data = self.convert_arithmatic(data_str)
		else:
			data = data_str.string
		return data

	def split(self, data_str, enclosed_chars):
		return StringWrapper(data_str.strip(' {0}'.format(enclosed_chars))).split(',')

	def increment(self):
		self.line_number += 1

	def is_object(self, data_str):
		return data_str.startswith('@')

	def is_var(self, data_str):
		return data_str.startswith('>')

	def is_arithmatic(self, data_str):
		return MathContainer.is_arithmatic(data_str)

	def has_parameters(self, data_str):
		index = data_str.find('<')
		return not index == -1 and data_str[index+1:].is_tuple()

	def convert_object(self, data_str):
		para_index = data_str.length()
		parameters = ()
		if self.has_parameters(data_str):
			para_index = data_str.index('<')
			parameters = self.convert_tuple(data_str[para_index + 1:])
		return ObjectContainer(data_str[1:para_index], parameters)

	def convert_arithmatic(self, data_str):
		return MathContainer(data_str)

	def replace_var(self, data_str):
		return self.data_history[data_str[1:].string]

	def convert_list(self, data_str):
		return [self.convert(x) for x in self.split(data_str, '[]')]

	def convert_tuple(self, data_str):
		return tuple(self.convert(x) for x in self.split(data_str, '()'))

	def convert_dict(self, data_str):
		return {self.convert(key) : self.convert(value) for key, value in self.get_kv_list(data_str)}

	def get_kv_list(self, data_str):
		return [StringWrapper(x).split_first(':') for x in self.split(data_str, '\{\}')]

class Config:
	def __init__(self, file_name):
		self.data = {}
		self.converter = Convert(self.data)
		self.load_file(file_name)

	def load_file(self, file_name):
		with open(file_name, 'r') as config_file:
			try:
				for config_line in config_file:
					if not config_line.startswith('#') and not config_line in '\n\t ':
						key, value = StringWrapper(config_line).split_first('=')
						more_lines = ''
						if value.startswith('[') and not value.endswith(']'):
							more_lines += self.read_to_char(config_file, ']')
						elif value.startswith('{') and not value.endswith('}'):
							more_lines += self.read_to_char(config_file, '}')
						elif value.startswith('(') and not value.endswith(')'):
							more_lines += self.read_to_char(config_file, ')')
						self.data[key] = self.converter.convert('{0} {1}'.format(value, more_lines))
					self.converter.increment()
			except Exception as ex:
				print('Error: {0}'.format(ex))
				if self.try_get('DEBUG', False):
					traceback.print_exc()

	def read_to_char(self, file, end_char):
		full_str = ''
		for line in file:
			full_str += line.strip(WHITE_SPACE)
			if full_str.endswith(end_char):
				break
		return full_str

	def keys(self):
		return self.data.keys()

	def items(self):
		return self.data.items()

	def get(self, key):
		return self.data[key]
			
	def try_get(self, key, default=None):
		if key in self.data:
			return self.data[key]
		return default

if __name__=='__main__':
	import sys
	config = Config(sys.argv[1])
	for key, value in config.items():
		print('\ntype: {2}\nkey: {0}\nvalue: {1}'.format(key, value, type(value)))