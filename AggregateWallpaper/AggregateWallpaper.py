#C:\Users\asnyder\AppData\Local\Programs\Python\Python36-32\python.exe  AggregateWallpaper.py
#To do: line length config, file size min, log makefile
import sys
from os import path
from FileHelper import Directory
from tools import CommandArguments, ASCIILine
	
class App:
	def __init__(self):	
		self.cmd_args = CommandArguments(*sys.argv)	
		self.line = ASCIILine(100)
		if self.cmd_args.try_get('DEBUG', False):
			self.line.draw()
			print(self.cmd_args)
	
	def print_result(self, affected, file_path):
		self.line.draw()
		print('{0} new files added to {1}'.format(affected, path.split(file_path)[1]))
		self.line.draw()
	
	def run(self):
		source_dir = Directory(self.cmd_args.try_get('SOURCE_FILE', ''), self.cmd_args.try_get('FILE_SIZE_MIN_IN_KB', 0))
		destination_dir = Directory(self.cmd_args.try_get('DESTINATION_FILE', ''), self.cmd_args.try_get('FILE_SIZE_MIN_IN_KB', 0))
		affected = source_dir.copy_to(destination_dir)
		self.print_result(affected, destination_dir.file_path)

if __name__ == '__main__':
	app = App()
	app.run()
	
	