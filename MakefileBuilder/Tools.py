#C:\Users\asnyder\AppData\Local\Programs\Python\Python36-32\python.exe Tools.py

class Debug:
	def __init__(self, debug, seperator):
		self.DEBUG = debug
		self.SEPERATOR = seperator
	
	def is_debug(self):
		return self.DEBUG
	
	def log(self, *args, titles=[], sep='\n', end='\n'):
		if self.DEBUG:
			print('{0}\nDebug:\n{1}'.format(self.SEPERATOR, '{0}'.format(sep).join(['{0}\n{1}:\n{2}'.format(self.SEPERATOR, titles[i], arg) for i, arg in enumerate(args)])), end=end)
	
class DynamicSpaces:
	def __init__(self, *args):
		self.index = 0
		self.str_list = list(args)
		self._max = self.get_max_length()

	def get_max_length(self):
		max = 0
		for s in self.str_list:
			if len(s) > max:
				max = len(s)
		return max
		
	def spaces(self):
		spaces = (' ' * (self._max - len(self.str_list[self.index])))
		self.index += 1
		return spaces
		
class ASCIILine:
	def __init__(self, length, char='-'):
		self._length = length 
		self._char = char 
		
	def __str__(self):
		return self._char * self._length
		
	def draw(self):
		print(self._char * self._length, end=('\n' if self._length > 0 else ''))

class Filter:
	def __init__(self, value_function=lambda x: x, filter_function=lambda x: True):
		self.value_function = value_function
		self.filter_function = filter_function
		
	def __str__(self):
		return 'Value Function: {0}Filter Function: {1}'.format(self.value_function.__repr__(), self.filter_function.__repr__())
	
	def filter(self, *args):
		return self.filter_function(self.value_function(*args))

class Convert:
	def convert(value):
		if value.startswith('['):
			return Convert.string_to_list(value)
		elif value.startswith('{'):
			return Convert.string_to_dictionary(value)
		elif value.isdigit():
			return int(value)
		elif value.lower() == 'true':
			return True 
		elif value.lower() == 'false':
			return False
		else:
			return value.strip('\'') 
			
	def read_to_char(string_list, end_char):
		aggregate = ''
		for string in string_list:
			aggregate += string 
			if string.strip().endswith(end_char):
				aggregate = aggregate.strip()[:-1]
				break 		
		return aggregate
		
	def string_to_class_variable(class_name, string):
		return getattr(class_name, string)
		
	def string_to_list(string):
		return [x.strip().strip('\'').replace('\\', '') for x in string.strip('[]').split(',')]
		
	def string_to_dictionary(string):
		return {x[:x.index(':')].strip(): x[x.index(':')+1:].strip() for x in string.strip('{}').split(',')}

class ConfigData:
	def __init__(self, config_file_path):
		self.CONFIG_FILE_PATH = config_file_path
		self.data = self.load_from_file()
		
	def load_from_file(self):
		tempData = {}
		with open(self.CONFIG_FILE_PATH, 'r') as f:
			line = f.readline()
			while line != '':
				if not line.isspace() and not line.startswith('#'):
					key, data = line.split('=')
					key, data = key.strip(), data.strip()
					if data.startswith('[') and not data.endswith(']'):
						more_lines = Convert.read_to_char(f, ']')
						data = Convert.string_to_list(data + more_lines)
					elif data.startswith('{') and not data.endswith('}'):
						more_lines = Convert.read_to_char(f, '}')
						data = Convert.string_to_dictionary(data + more_lines)
					else:
						data = Convert.convert(data)
					tempData[key] = data 
				line = f.readline()
		return tempData

	def __str__(self):
		return '\n'.join(['{0} = {1}'.format(key, self.data[key]) for key in self.data])

	def try_get(self, key, default):
		if key in self.data:
			return self.data[key]
		return default
		
class CommandArguments:
	COMMAND_SPLIT_CHAR = '='

	def __init__(self, *args):
		self.cmd_args = {}
		positional_args = 0
		for i in range(1, len(args)):
			if CommandArguments.COMMAND_SPLIT_CHAR in args[i]: 
				key, value = args[i].split('=')
				self.cmd_args[key] = Convert.convert(value)
			else:
				key, value = positional_args, args[i]
				self.cmd_args[key] = Convert.convert(value)
				positional_args += 1
				
	def __str__(self):
		return '\n'.join(['{0}: {1}'.format(key, self.cmd_args[key]) for key in self.cmd_args])
			
	def try_get(self, key, default):
		if key in self.cmd_args:
			return self.cmd_args[key]
		return default
		
if __name__=='__main__':
	import sys 
	
	cmd_args = CommandArguments(*sys.argv)
	print(cmd_args)
	config_data = ConfigData(cmd_args.try_get('cf', ''))
	print(config_data)