#C:\Users\asnyder\AppData\Local\Programs\Python\Python36-32\python.exe makefile.py
import traceback
from tools import ConfigData

def get_file_name_without_ext(file_path):
	slash_pos, ext_pos = file_path.rfind('\\'), file_path.rfind('.')
	return file_path[(slash_pos + 1) if not slash_pos == -1 else 0:ext_pos if not ext_pos == -1 else -1]
	
def print_if_debug(debug, object):
	if debug:
		print(object)

if __name__=='__main__':
	print('Loading configdata.txt...')
	CONFIG = ConfigData('configdata.txt')
	DEBUG = CONFIG.try_get('DEBUG', False)
	print_if_debug(DEBUG, CONFIG)
	EXECUTABLE_PATH = CONFIG.try_get('EXECUTABLE_PATH', 'python')
	PYTHON_FILE_PATH = CONFIG.try_get('PYTHON_FILE_PATH', '')
	SHELL_STARTUP = CONFIG.try_get('SHELL_STARTUP', '')	
	BATCH_NAME = '{0}.bat'.format(get_file_name_without_ext(PYTHON_FILE_PATH))
	print_if_debug(DEBUG, 'BATCH_NAME: {0}'.format(BATCH_NAME))
	INCLUDE_IN_COMMAND_ARGS = CONFIG.try_get('INCLUDE_IN_COMMAND_ARGS', '')
	CMD_ARGS = ' '.join(['{0}="{1}"'.format(key, CONFIG.data[key]) for key in CONFIG.data if key in INCLUDE_IN_COMMAND_ARGS])
	print_if_debug(DEBUG, 'CMD_ARGS {0}'.format(CMD_ARGS))
	
	SUCCESS = True
	try:
		print('Opening file to write...')
		with open(BATCH_NAME, 'w') as bat:
			print('Writing to file...')
			bat.write('@ECHO {0}\n'.format('ON' if DEBUG else 'OFF'))
			bat.write('"{0}" "{1}" {2}\n'.format(EXECUTABLE_PATH, PYTHON_FILE_PATH, CMD_ARGS))
			bat.write('set /p=Press Enter to Continue...')
		
	except Exception as ex:
		print('Error: {0}'.format(ex))
		if DEBUG:
			traceback.print_exc()
		SUCCESS = False
		
	print('{0}'.format('Success: Bat was Created...' if SUCCESS else 'Error: Bat was not Created...'))
		
