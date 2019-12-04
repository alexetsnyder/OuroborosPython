#C:\Users\asnyder\AppData\Local\Programs\Python\Python36-32\python.exe CreateBackups.py
import re
import sys
import shutil
import datetime
from os import path
sys.path.insert(0, '..\Helpers')
from FileHelper import Folder
from Tools import CommandArguments, ASCIILine

def zip_dir(source_dir, output_file):
	shutil.make_archive(output_file, 'zip', source_dir)
	
class Date:
	def __init__(self, date_string):
		first_dash = date_string.find('-')
		last_dash = date_string.rfind('-')
		self.year = int(date_string[:first_dash])
		self.month = int(date_string[first_dash+1:last_dash])
		self.day = int(date_string[last_dash+1:])
		
	def __lt__(self, other):
		return self.year < other.year or ((self.year == other.year and self.month < other.month) or (self.month == other.month and self.day < other.day))
		
	def __str__(self):
		return '{0}-{1}-{2}'.format(self.year, self.month, self.day)

class Backups:
	def __init__(self, cmd_args):
		self.search_path = cmd_args.try_get('PATH_SEARCH', '.')
		self.line = ASCIILine(cmd_args.try_get('DIVIDING_LINE_LENGTH', 0), cmd_args.try_get('DIVIDING_LINE_CHAR', '-'))
		self.programs = self.get_programs()
		self.now = datetime.datetime.now()
		self.time_stamp_re = re.compile('(\\d\\d\\d\\d)-((1[0-2])|(0?\\d))-((3[0-1])|([1-2]?\\d))')
		
	def get_programs(self):
		progs = []
		for folder_name in Folder(self.search_path).list_all(lambda fp, f: not path.isfile(fp) and not f.endswith('.ini')):
			if not folder_name == 'Backups':
				folder = path.join(self.search_path, folder_name)
				if self.has_python(folder):
					progs.append(folder)
		return progs 
		
	def has_python(self, folder):
		if Folder(folder).list_all(lambda fp, f: f.endswith('.py')):
			return True 
		return False
	
	def time_stamp(self):
		return '{0}-{1}-{2}'.format(self.now.year, self.now.month, self.now.day)
		
	def parse_time_stamp(self, file_name):
		return self.time_stamp_re.search(file_name).group()
	
	def create_output_file(self, program_dir):
		index = program_dir.rfind('\\')
		return '{0}{1}'.format(program_dir[index+1 if not index == -1 else 0:], self.time_stamp()) 
	
	def move_old_backups(self):
		time_stamp = Date(self.time_stamp())
		zip_files = Folder('.').list_all(lambda fp, f: f.endswith('.zip'))
		for zip_file in zip_files:
			file_time_stamp = Date(self.parse_time_stamp(zip_file))
			if file_time_stamp < time_stamp:
				Folder(zip_file).move_to(Folder('Old Backups').join(str(file_time_stamp)))	
	
	def zip_all(self):
		self.line.draw()
		print('CREATE ALL BACKUPS:')
		self.line.draw()
		for program in self.programs:
			success = self.zip_file(program)
			self.line.draw() 
		
	def zip_file(self, program_dir):
		backup_file_name = self.create_output_file(program_dir)
		if not Folder('.').exists('{0}.zip'.format(backup_file_name)):
			print('Creating Backup as: {0}'.format(backup_file_name))
			zip_dir(program_dir, backup_file_name)
		else:
			print('File {0} already created today.'.format(backup_file_name))
	
if __name__=='__main__':
	cmd_args = CommandArguments(*sys.argv)
	backups = Backups(cmd_args)
	backups.move_old_backups()
	backups.zip_all()
	
	