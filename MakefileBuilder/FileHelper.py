#C:\Users\asnyder\AppData\Local\Programs\Python\Python36-32\python.exe FileHelper.py
from Tools import Filter
from shutil import copyfile
from os import mkdir, listdir, path

class eInput:
	READ  = 0
	WRITE = 1

class FileIO:
	def __init__(self, file_name, input):
		self.file_name = file_name
		self.input = input
	
	def load(self):
		if self.input == eInput.WRITE:
			raise IOException('Cannot write a read only file.')
		with open(self.file_name, 'r') as f:
			return f.readlines()
		
	def save(self, string):
		if self.input == eInput.READ:
			raise IOException('Cannot read a write only file.')
		with open(self.file_name, 'w') as f:
			f.write(string)

class Folder:
	KBYTES_TO_BYTES = 1000
					  
	def __init__(self, file_path):
		self.file_path = file_path
		if not path.exists(file_path):
			mkdir(file_path)
			
	def list_all(self, filter_function=lambda f, p: True):
		return [file for file in listdir(self.file_path) if filter_function(self.file_path, file)] 
			
	def __str__(self):
		return '\n'.join(self.list_all())
		
	def copy_to(self, dest_folder, convert_function=lambda x: x, filter=lambda x: True):
		files = self.list_all(filter)
		for file in files:
			copyfile(path.join(self.file_path, file), path.join(dest_folder.file_path, convert_function(file)))
		return len(files)

if __name__=='__main__':
	import sys
	folder = Folder(sys.argv[1])
	print(folder)