#config.py
MULTI_LINE_CHARS 	 = ['\'', '"', '[', '(', '{']
MULTI_LINE_END_CHARS = ['\'', '"', ']', ')', '}']
STRING_BOOL_TRUE     = ['t', 'T', 'True', 'true']
STRING_BOOL_FALSE    = ['f', 'F', 'False', 'false']

MULTI_LINE_CHARS = {
	'\'' : '\'',
	'"'  : '"',
	'['  : ']',
	'('  : ')',
	'{'  : '}'
}

class DataType:
	INT      = 'int'
	DOUBLE   = 'double'
	STRING   = 'string'
	BOOL     = 'bool'
	VARIABLE = 'variable'
	OBJECT   = 'object'
	MATH     = 'math'
	EOF      = 'eof'

class String:
	def __init__(self, py_str):
		self.inner_str = py_str.strip()

	def __str__(self):
		return self.inner_str

	def __iadd__(self, other):
		self.inner_str += other.inner_str

	def split(self, string, n):
		return [String(item) for item in self.inner_str.split(string, n)]

	def length(self):
		return len(self.inner_str)

	def first_char(self):
		return self.inner_str[0]

	def last_char(self):
		return self.inner_str[-1]

	def to_int(self):
		return int(self.inner_str)

	def to_float(self):
		return float(self.inner_str)

	def to_bool(self):
		if self.inner_str in STRING_BOOL_TRUE:
			return True
		elif self.inner_str in STRING_BOOL_FALSE:
			return False 

class Line:
	SPLIT_CHAR = '='

	def __init__(self, raw_str):
		self.line_str = raw_str
		self.key, self.value = self.line_str.split(Line.SPLIT_CHAR, 1)
		self.first_char = self.value.first_char()
		self.last_char = self.value.last_char()

	def add(self, line_str):
		self.value += line_str

	def is_open(self):
		if self.first_char in MULTI_LINE_CHARS:
			if MULTI_LINE_CHARS[self.first_char] == self.last_char:
				return False
		return True

class File:
	def __init__(self, file_name):
		self.file_name = file_name 

	def next_line(self):
		with open(self.file_name, 'r') as file:
			while True:
				line = file.readline()
				if line == '':
					yield DataType.EOF 
					break;
				else:
					yield line 

class Command:
	def __init__(self, line):
		self.key = line.key 
		self.data = line.value

	def convert(self):
		if self.data

class Tokenizer:
	def __init__(self, file):
		self.line_number = 0
		self.file = File(file)
		self.current_line = None 

	def next(self):
		for line in self.file.next_line():
			self.line_number += 1
			line_str = String(line)
			if self.current_line == None:
				self.current_line = Line(line_str)
			elif not self.current_line.is_open():
				yield Command(self.current_line)
				self.current_line = Line(line_str)
			else:
				self.current_line.add(line_str)		

class Config:
	def __init__(self, file_path):
		self.tokenizer = Tokenizer(file_path)

	def get_next(self):
		while True:
			line = self.file.readline()
			#self.key, self.value = 

	def load(self):
		pass

	def convert(self):
		pass

def unit_test(*args, **kwargs):
	output_str = ''
	for i, arg in enumerate(args):
		output_str += ', {0}) {1}'.format(i+1, arg)
	output_str = output_str.lstrip(' ,')
	for key in kwargs:
		output_str += ', {0}: {1}'.format(key, kwargs[key])
	print(output_str.lstrip(' ,'))

if __name__=='__main__':
	str1 = String(' \t[skdfskdjfsldfksadf] \n ')
	str2 = String('skdfjslkdjfssk)')
	unit_test(startswith=str1.starts_with_any(MULTI_LINE_CHARS), endswith=str1.ends_with_any(MULTI_LINE_END_CHARS))
	unit_test(startswith=str2.starts_with_any(MULTI_LINE_CHARS), endswith=str2.ends_with_any(MULTI_LINE_END_CHARS))
