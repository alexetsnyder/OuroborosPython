#C:\Users\asnyder\AppData\Local\Programs\Python\Python36-32\python.exe Makefile.py
import sys
import traceback
from os import path
from FileHelper import Folder
from Tools import ConfigData, Debug, ASCIILine, CommandArguments

class Executable:
	def __init__(self, CONFIG):
		self.PROGRAM_NAME = CONFIG.try_get('BATCH_NAME', '')
		self.EXECUTABLE_FILE = CONFIG.try_get('EXECUTABLE_FILE', 'python')
		self.PYTHON_FILE = CONFIG.try_get('PYTHON_FILE', '')
		self.CMD_ARGS = {key : CONFIG.try_get(key, '') for key in CONFIG.try_get('INCLUDE_IN_COMMAND_ARGS', [])}
		self.SET_STRINGS = '\n'.join(['set {0}="{1}"'.format(key, self.CMD_ARGS[key]) for key in self.CMD_ARGS])
		self.LINE = ASCIILine(CONFIG.try_get('DIVIDING_LINE_LENGTH', 0), CONFIG.try_get('DIVIDING_LINE_CHAR', '-'))
		self.DEBUG = Debug(CONFIG.try_get('DEBUG', False), self.LINE)
		
	def __str__(self):
		aggregate = self.SET_STRINGS
		aggregate += '\n"{0}" "{1}" {2}'.format(self.EXECUTABLE_FILE, self.PYTHON_FILE, ' '.join(['{0}=%{0}%'.format(key) for key in self.CMD_ARGS]))
		return aggregate

class Make:
	def __init__(self, cmd_args):
		self.cmd_args = cmd_args
		self.folder_path = self.cmd_args.try_get('MAKEFILE_PATH_SEARCH', '.')
		self.CONFIG_FILE_NAME = self.cmd_args.try_get('MAKEFILE_CONFIG_NAME', 'config.txt')
		self.programs = self.get_programs()
		self.line = ASCIILine(self.cmd_args.try_get('DIVIDING_LINE_LENGTH', 0), self.cmd_args.try_get('DIVIDING_LINE_CHAR', '-'))
		self.debug = Debug(self.cmd_args.try_get('DEBUG', False), self.line)
		
	def get_programs(self):
		progs = []
		for folder_name in Folder(self.folder_path).list_all(lambda fp, f: not path.isfile(fp) and not f.endswith('.ini')):
			folder = path.join(self.folder_path, folder_name)
			if self.has_config(folder):
				progs.append(folder)
		return progs 
		
	def has_config(self, folder_path):
		if self.CONFIG_FILE_NAME in Folder(folder_path).list_all(lambda fp, f: f.endswith('.txt')):
			return True 
		return False
		
	def make(self, file_path):
		print('Loading config file in: {0}.'.format(file_path))
		config = ConfigData(path.join(file_path, self.CONFIG_FILE_NAME))	
		executable = Executable(config)
		self.debug.log(config, executable, titles=['Config File', 'Executable'])
		include_stop = config.try_get('INCLUDE_STOP', True)	
		SUCCESS = True
		try:
			print('Creating file: {0} from config file in: {1}.'.format(executable.PROGRAM_NAME, file_path))
			with open(path.join(file_path, executable.PROGRAM_NAME), 'w') as bat:
				print('Writing to file: {0} from config file in: {1}.'.format(executable.PROGRAM_NAME, file_path))
				bat.write('@ECHO {0}\n'.format('ON' if executable.DEBUG.is_debug() else 'OFF'))
				bat.write(str(executable))
				if include_stop:
					bat.write('\nset /p=Press Enter to Continue...')		
		except Exception as ex:
			print('Error: {0}'.format(ex))
			if self.debug.is_debug():
				traceback.print_exc()
			SUCCESS = False
		print('File: {0} {1} in config file: {2}.'.format(executable.PROGRAM_NAME, 'created' if SUCCESS else 'was not created', file_path))
	
	def make_all(self):
		self.line.draw()
		print('MAKE ALL')
		self.line.draw()
		for program in self.programs:
			success = self.make(program)
			self.line.draw()

if __name__=='__main__':
	cmd_args = CommandArguments(*sys.argv)
	makefile = Make(cmd_args)
	makefile.make_all()
	input('Press Enter to Quit...')
	