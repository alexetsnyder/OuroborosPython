#C:\Users\asnyder\AppData\Local\Programs\Python\Python36-32\python.exe FileHelper.py
from shutil import copyfile
from tools import Operator, Filter
from os import mkdir, listdir, path

class SearchOption:
	ALL = 0
	FILES = 1
	FOLDERS = 2
	
class Folder:
	KBYTES_TO_BYTES = 1000
	SEARCH_OPTIONS = {SearchOption.ALL     : lambda x: True, 
					  SearchOption.FILES   : path.isfile, 
					  SearchOption.FOLDERS : not path.isfile}
					  
	def __init__(self, file_path):
		self.file_path = file_path
		if not path.exists(file_path):
			mkdir(file_path)
			
	def list_all(self, option=SearchOption.ALL):
		return [file for file in listdir(self.file_path) if Directory.SEARCH_OPTIONS[option](path.join(self.file_path, file))] 
			
	def __str__(self):
		return '\n'.join(self.list_all())
		
	def filter(self, file_values, filter_value, operator, search_option=SearchOption.ALL):
		filter = Filter(filter_value, operator)
		return [file for i, file in enumerate(self.list_all(search_option)) if filter.filter(files_value[i])] 
		
	
class Directory:	
	KBYTES_TO_BYTES = 1000
	SEARCH_OPTIONS = {SearchOption.ALL     : lambda x: True, 
					  SearchOption.FILES   : path.isfile, 
					  SearchOption.FOLDERS : not path.isfile}
	
	def __init__(self, file_path, size_kb):
		self.FILE_SIZE_MIN = int(size_kb) * Directory.KBYTES_TO_BYTES
		self.file_path = file_path
		if not path.exists(file_path):
			mkdir(file_path)
			
	def __str__(self):
		return '\n'.join(self.list_all())
		
	def list_all(self, option=SearchOption.ALL):
		return [f for f in listdir(self.file_path) if Directory.SEARCH_OPTIONS[option](path.join(self.file_path, f))] 
		
	def filter(self, destination_file_list):
		filter_size = Filter(self.FILE_SIZE_MIN, Operator.GREATER_THAN)
		filter_matching = Filter(destination_file_list, Operator.NOT_IN_LIST)
		return [file for file in [file for file in self.list_all(SearchOption.FILES) if filter_size.filter(path.getsize(path.join(self.file_path, file)))] if filter_matching.filter('{0}.jpg'.format(file))]
	
	def copy_to(self, destination): 
		files = self.filter(destination.list_all(SearchOption.FILES))
		for file in files:
			copyfile(path.join(self.file_path, file), path.join(destination.file_path, '{0}.jpg'.format(file)))
		return len(files)

if __name__=='__main__':
	directory = Directory(sys.argv[1])
	print(directory)