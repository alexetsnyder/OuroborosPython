#C:\Users\asnyder\AppData\Local\Programs\Python\Python36-32\python.exe
import os 
import random as r
import datetime as time
import calendar as cal
import functools as tools
import traceback as trace

MAX_DAY_OF_WEEK = 7
DEFAULT_DATA_FILE = 'data/lunchdata.txt'

class eInput:
	DATA_LEARNING = 0
	ENTER_LUNCH = 1 
	SET_UP = 2

def max(*args):
	return tools.reduce(lambda a, b: a if a > b else b, args)
	
def sum(*args):
	return tools.reduce(lambda a, b: a + b, args)
	
def print_whitespace(line):
	print(line.replace(' ', '\\0').replace('\t', '\\t').replace('\n', '\\n'))

class ConfigData:
	CONFIG_FILE_PATH = 'data\configdata.txt'

	def __init__(self):
		self.data = self.load_from_file()
		
	def try_get(self, key, default):
		if key in self.data:
			return self.data[key]
		return default
		
	def load_from_file(self):
		tempData = {}
		with open(ConfigData.CONFIG_FILE_PATH, 'r') as f:
			line = f.readline()
			while line != '':
				if not line.isspace() and not line.startswith('#'):
					key, data = line.split('=')
					key, data = key.strip(), data.strip()
					if data.startswith('['):
						more_lines = ''
						if not data.endswith(']'):
							more_lines = self.read_in_rest(f, ']')
						data = self.convert_string_to_list(data + more_lines)
					elif data.startswith('{'):
						more_lines = ''
						if not data.endswith('}'):
							more_lines = self.read_in_rest(f, '}')
						data = self.convert_string_to_dict(data + more_lines)
					elif data.isdigit():
						data = int(data)
					elif data.lower() == 'true':
						data = True 
					elif data.lower() == 'false':
						data = False
					else:
						data = data.strip('\'')
					tempData[key] = data 
				line = f.readline()
		return tempData

	def __str__(self):
		return '\n'.join(['{0} = {1}'.format(key, self.data[key]) for key in self.data])	
		
	def read_in_rest(self, file, end_char):
		string = ''
		for line in file:
			string += line 
			if line.strip().endswith(end_char):
				string = string.strip()[:-1]
				break 		
		return string
	
	def convert_string_to_list(self, string):
		return [x.strip().strip('\'').replace('\\', '') for x in string.strip('[]').split(',')]
		
	def convert_string_to_dict(self, string):
		return {x[:x.index(':')].strip(): x[x.index(':')+1:].strip() for x in string.strip('{}').split(',')}
	
class WeightedChoice:
	def __init__(self, config, choices):
		self.weighted_dicts = self.load(config.try_get('DATA_FILE_NAME', DEFAULT_DATA_FILE))
		self.isFirstTime = False 
		if not self.weighted_dicts:
			self.weighted_dicts = {i: {choice:0 for choice in choices} for i in range(MAX_DAY_OF_WEEK)}
			self.isFirstTime = True
		if config.try_get('DEBUG', False):
			print('\nWeighted Choices:')
			print(self)
		self.config = config	
	
	def sync_with_choices(self, choices):
		choice_set = set(choices)
		added_choices = choice_set - set(self.weighted_dicts[0])
		if self.config.try_get('DEBUG', False):
			print('\nSync Data:')
			print('\nAdded Choices:', added_choices)
		if added_choices:
			for day_key in self.weighted_dicts:
				for choice_key in added_choices:
					self.weighted_dicts[day_key][choice_key] = 0
					if self.config.try_get('DEBUG', False):
						print('Added: Day: {0}, Choice: {1}, Value: {2}'.format(day_key, choice_key, self.weighted_dicts[day_key][choice_key]))
		removed_choices = set(self.weighted_dicts[0]) - choice_set
		if self.config.try_get('DEBUG', False):
			print('\nRemoved Choices:', removed_choices) 
		if removed_choices:
			for day_key in self.weighted_dicts:
				for choice_key in removed_choices:
					if self.config.try_get('DEBUG', False):
						print('Removing: Day: {0}, Choice: {1}, Value: {2}'.format(day_key, choice_key, self.weighted_dicts[day_key][choice_key]))
					del self.weighted_dicts[day_key][choice_key]
		return added_choices or removed_choices
					
	def add_day_choice(self, day, choice):
		self.weighted_dicts[day][choice] += 1
		
	def set_day_choice(self, day, choice):
		self.weighted_dicts[day][choice] = 1
		
	def set_all_choices_to_one(self, day):
		for choice in self.weighted_dicts[day]:
			self.weighted_dicts[day][choice] = 1
			
	def __repr__(self):
		return '#'.join([''.join(['({0}, {1})'.format(inner_key, self.weighted_dicts[key][inner_key]) for inner_key in self.weighted_dicts[key]]) for key in self.weighted_dicts])
			
	def __str__(self):
		return '\n'.join([cal.day_name[key] + ':\n' + ' '.join([inner_key + ': ' + str(self.weighted_dicts[key][inner_key]) for inner_key in self.weighted_dicts[key]]) for key in self.weighted_dicts])
		
	def save(self, file_name):
		with open(file_name, 'w') as f:
			f.write(self.__repr__())
	
	def load(self, file_name): 
		weighted_dicts = {}
		if os.path.exists(file_name):
			with open(file_name, 'r') as f:
				index = 0
				for line in f:
					x, y = '', 0
					acc = ''
					for char in line:
						if char == '(':
							continue 
						elif char == '#':
							index += 1
						elif char == ')':
							y = int(acc)
							if not index in weighted_dicts:
								weighted_dicts[index] = {}
							weighted_dicts[index][x] = y
							x, y = '', 0
							acc = ''
						elif char == ',':
							x = acc
							acc = ''
						else:
							acc += char 
		return weighted_dicts
	
	def weighted_choice(self, day_int):
		return r.choices([key for key in self.weighted_dicts[day_int]], [self.weighted_dicts[day_int][key] for key in self.weighted_dicts[day_int]])[0]	
	
class ChooseLunch:
	DAY_OF_WEEK_INT = time.datetime.today().weekday()
		
	def __init__(self, config):
		self.config = config 
		self.CHOICES = config.try_get('CHOICES', [])
		self.weighted_choice = WeightedChoice(config, self.CHOICES)
		self.isFirstTime = self.weighted_choice.isFirstTime
		self.current_week_samples = ''
		
	def __str__(self):
		return str(self.weighted_choice)

	def sync_with_weighted_choice(self):
		return self.weighted_choice.sync_with_choices(self.CHOICES)
		
	def choose_lunch_today(self):
		return self.weighted_choice.weighted_choice(ChooseLunch.DAY_OF_WEEK_INT)
		
	def choose_lunch(self, day_int):
		return self.weighted_choice.weighted_choice(day_int)
		
	def old_choose_lunch(self, day_int):
		return {**{i : (lambda y: (lambda x: x[y]))(i) for i in range(2)}, **{i: (lambda x: r.choice(x[2:])) for i in range(2, MAX_DAY_OF_WEEK)}}[day_int](self.CHOICES)
		
	def sample_week(self):
		return [self.choose_lunch(i) for i in range(MAX_DAY_OF_WEEK)]
	
	def multiple_choice_sample_weeks(self, n):
		choice_list = [self.sample_week() for i in range(n)]
		for i in range(MAX_DAY_OF_WEEK):
			max_len = max(*[len(choice_list[j][i]) for j in range(n)])
			for j in range(n):
				choice_list[j][i] += ' ' * (max_len - len(choice_list[j][i]))
		self.current_week_samples = '\n'.join([str(i + 1) + ' #' + '  #'.join(choice_list[i]) for i in range(len(choice_list))])	

	def add_day_choice(self, day, choice):
		self.weighted_choice.add_day_choice(day, choice)
		
	def set_day_choice(self, day, choice):
		self.weighted_choice.set_day_choice(day, choice)
	
	def set_all_choices_to_one(self, day):
		self.weighted_choice.set_all_choices_to_one(day)
		
	def add_row_choice(self, index):
		row = self.current_week_samples.split('\n')[index]
		for n in range(MAX_DAY_OF_WEEK):
			self.add_day_choice(n, self.get_nth_word(row, n))
			
	def get_nth_word(self, sample_week, n):
		word = ''
		count = 0
		clean_sample_week = sample_week[3:].strip()
		for i in range(len(clean_sample_week)):
			if clean_sample_week[i] == '#':
				if count == n:
					return word.strip()
				count += 1
				word = ''
			else:
				word += clean_sample_week[i]
		return word
		
	def save_data(self):
		self.weighted_choice.save(self.config.try_get('DATA_FILE_NAME', DEFAULT_DATA_FILE))
		
	def get_choices(self):
		new_choices = ['1: All' if i == 0 else '{0}: {1}'.format(i+1, self.CHOICES[i-1]) for i in range(len(self.CHOICES)+1)]
		max_len = max(*[len(x) + (-1 if i == 0 else 1) for i, x in enumerate(new_choices) if i % 2 == 0])
		for i in range(len(new_choices)):
			if i == 0:
				continue
			elif i == 1:
				new_choices[i] = (' ' * (max_len - 7)) + ' ' + new_choices[i]
			elif not i % 2 == 0:
				new_choices[i] = (' ' * (max_len - len(new_choices[i-1]))) + ' ' + new_choices[i]
			else:
				new_choices[i] = '\n' + new_choices[i]		
		return ''.join(new_choices)
		
	def select_choice(self, choice):
		if choice == 1:
			raise Exception('All is not an option for entering todays lunch.')
		else:
			self.add_day_choice(ChooseLunch.DAY_OF_WEEK_INT, self.CHOICES[choice - 2])
			
	def select_choices(self, day_int, choices):
		if len(choices) == 1 and choices[0] == 1:
			self.set_all_choices_to_one(day_int)
		else:
			for i in choices:
				self.set_day_choice(day_int, self.CHOICES[i - 2])
	
class App:
	def __init__(self):
		self.config = ConfigData()
		if self.config.try_get('DEBUG', False):
			print('Config Data:')
			print(self.config)
			
		self.dynamic_menu_maker()
		if self.config.try_get('DEBUG', False):
			print('\nDynamically Created Menu:')
			print(self.MAIN_MENU)
			print(self.MENU_FUNCTIONS)
			
		self.NUMBER_OF_MENU_OPTIONS = self.config.try_get('DATA_MENU_LEARNING_OPTIONS', 4)
		self.EXIT_CODES = self.config.try_get('EXIT_CODES', ['q', 'Q'])	
		self.choose_lunch = ChooseLunch(self.config)
		self.isFirstTime = self.choose_lunch.isFirstTime
		self.isDirty = False		
		if self.choose_lunch.sync_with_weighted_choice():
			self.isDirty = True 
		
	def dynamic_menu_maker(self):
		self.MAIN_MENU = []
		self.MENU_FUNCTIONS = {}
		index = 1
		for key in self.config.try_get('MAIN_MENU', {}):
			if self.config.try_get('DEBUG', False) or not key in self.config.try_get('DEBUG_OPTIONS', []):
				self.MAIN_MENU.append('{0}: {1}'.format(index, self.config.try_get('MAIN_MENU', {})[key]))
				self.MENU_FUNCTIONS[str(index)] = self.config.try_get('MAIN_MENU_FUNCTIONS', {key: ''})[key]
				index += 1	
		self.MAIN_MENU.append('q: Exit')
		self.MAIN_MENU.append('Enter Choice: ')	
		
	def program_header(self):
		self.dividing_line()
		print('Welcome to Choose Lunch AI : You never have to decide where to go to lunch ever again.')
		self.dividing_line()
		
	def menu_choices(self, origin):
		self.dividing_line()
		print(self.choose_lunch.get_choices())
		print('Enter choice {0}'.format('in comma seperated list:' if origin == eInput.SET_UP else ':'))
	
	def menu_data_learning(self, n):
		self.dividing_line()
		self.choose_lunch.multiple_choice_sample_weeks(n)
		print(self.choose_lunch.current_week_samples)
		print('Enter the week that best matches your lunch schedule (enter q to quit):')	
	
	def parse_input(self, input_string, origin):
		if input_string in self.EXIT_CODES or (origin == eInput.SET_UP and input_string[:-2] in self.EXIT_CODES):
			return False 
		else:
			try:
				if origin == eInput.DATA_LEARNING:
					input_int = int(input_string)
					self.choose_lunch.add_row_choice(input_int-1)
					self.dividing_line()
					print(self.choose_lunch.current_week_samples.split('\n')[input_int-1])
				elif origin == eInput.ENTER_LUNCH:
					input_int = int(input_string)
					self.choose_lunch.select_choice(input_int)
				else:
					self.choose_lunch.select_choices(int(input_string[-1:]), [int(i) for i in input_string[:-2].split(',')])
			except Exception as ex:
				self.dividing_line()
				print('Incorrect input: {0}'.format(ex))
				if self.config.try_get('DEBUG', False):
					trace.print_exc()
			return True
			
	def dividing_line(self):
		print('-' * self.config.try_get('DIVIDING_LINE', 100))
	
	def save_data(self):
		self.choose_lunch.save_data() 
	
	def run_startup(self):
		if self.isFirstTime:
			self.run_setup_week()
			self.isDirty = True
	
	def run_data_learning(self):
		while True:
			self.menu_data_learning(self.NUMBER_OF_MENU_OPTIONS)
			if not self.parse_input(input(), eInput.DATA_LEARNING):
				break
	
	def run_setup_week(self):
		for i in range(MAX_DAY_OF_WEEK):
			self.dividing_line()
			print('{0}:'.format(cal.day_name[i]))
			self.menu_choices(eInput.SET_UP)
			if not self.parse_input('{0}:{1}'.format(input(), i), eInput.SET_UP):
				break
			
	def main_menu(self):
		self.dividing_line()
		print('\n'.join(self.MAIN_MENU))
		
	def choose_today(self):
		self.dividing_line()
		print(cal.day_name[ChooseLunch.DAY_OF_WEEK_INT], ': ', self.choose_lunch.choose_lunch_today(), sep='')
		
	def choose_week(self):
		self.dividing_line()
		week = self.choose_lunch.sample_week()
		print(' '.join(['#{0}: {1}'.format(cal.day_name[i], week[i]) for i in range(len(week))]))
		
	def enter_todays_choice(self):
		self.menu_choices(eInput.ENTER_LUNCH)
		self.parse_input(input(), eInput.ENTER_LUNCH)
		self.isDirty = True 
		
	def set_up_week(self):
		self.run_setup_week()
		self.isDirty = True 
		
	def data_learning(self):
		self.run_data_learning()
		self.isDirty = True 
	
	def show_list(self):
		self.dividing_line()
		print(self.choose_lunch)
		
	def run(self):
		self.program_header()
		self.run_startup()
		while True:
			self.main_menu()
			choice = input()
			if choice in self.EXIT_CODES:
				break
			try:
				getattr(App, self.MENU_FUNCTIONS[choice])(self)
			except Exception as ex:
				self.dividing_line()
				print('Incorrect input: {0}'.format(ex))
				if self.config.try_get('DEBUG', False):
					trace.print_exc()
						
		if self.isDirty:
			print('Saving...')
			self.save_data()
						
if __name__ == '__main__':
	app = App()
	app.run()
	print('Thank you!')