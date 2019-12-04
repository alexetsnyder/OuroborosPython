#C:\Users\asnyder\AppData\Local\Programs\Python\Python36-32\python.exe SurveyFont.py
import pygame
from pygame import freetype
from Color import Color

class FontInfo:
	def __init__(self, font_name, font_size, font_color):
		self.font_name = font_name
		self.font_size = font_size
		self.font_color = font_color

class Text:
	def __init__(self, text_str, font_info):
		self.text_str = text_str
		self.font_name = font_info.font_name
		self.font_size = font_info.font_size
		self.font_color = font_info.font_color
		self.font = freetype.SysFont(self.font_name, self.font_size)
		self.width = self.font.get_rect(self.text_str).width
		self.height = self.font.get_rect(self.text_str).height

	def draw_to(self, surface, position):
		self.font.render_to(surface, position, self.text_str, self.font_color)

class SurveySurface:
	def __init__(self, letter, font_info, dimensions, background_color):
		self.text = Text(letter, font_info) 
		self.width, self.height = dimensions
		self.background_color = background_color
		self.surface = pygame.Surface((self.width, self.height))
		self.draw_char_to_surface()
		self.pixel_array = pygame.PixelArray(self.surface)

	def get_char_width(self):
		return self.text.width 

	def get_char_height(self):
		return self.text.height

	def draw_char_to_surface(self):
		self.surface.fill(self.background_color)
		self.text.draw_to(self.surface, (self.width/2, self.height/2))

	def get_pixel(self, x, y):
		return self.surface.unmap_rgb(self.pixel_array[x, y])[:3]

class SurveyedPart:
	def __init__(self, left, right):
		self.left = left 
		self.right = right

	def get_length(self):
		return (self.right - self.left)

	def get_line(self):
		return self.get_length() * '-'

	def __str__(self):
		return '(left, right) = ({0}, {1})'.format(self.left, self.right) 

class SurveyedRow:
	def __init__(self, height, *args):
		self.parts = []
		self.height = height
		for arg in args:
			left, right = arg 
			self.parts.append(SurveyedPart(left, right))

	def __str__(self):
		return ' '.join(['Height: {0}'.format(self.height)] + [str(p) for p in self.parts])

class SurveyedLetter:
	def __init__(self, letter, font_info, dimensions, background_color):
		self.rows = []
		self.letter = letter
		self.font_info = font_info
		self.width, self.height = dimensions
		self.background_color = background_color
		self.current_col = 0
		self.current_row = 0
		self.survey_surface = SurveySurface(self.letter, self.font_info, dimensions, self.background_color)
		self.char_width = self.survey_surface.get_char_width()
		self.char_height = self.survey_surface.get_char_height()
		self.left, self.right = (self.width//2, self.width//2 + self.char_width)
		self.top, self.bottom = (self.height//2, self.height//2 + self.char_height)

	def __str__(self):
		return '\n'.join([str(r) for r in self.rows])

	def print_as_letter(self):
		min_left = self.left
		for i in range(len(self.rows)):
			row_str = ''
			for j in range(len(self.rows[i].parts)):
				space_number = 0
				if j == 0:
					space_number = self.rows[i].parts[j].left - min_left
				else:
					space_number = self.rows[i].parts[j].left - self.rows[i].parts[j-1].right
				row_str += '{0}{1}'.format(space_number * ' ', self.rows[i].parts[j].get_line())
			print(row_str)
			if i + 1 < len(self.rows):
				print((self.rows[i+1].height - self.rows[i].height - 1) * '\n', sep='', end='')

	def burn_contiguous(self):
		 while self.current_row < self.right and not self.survey_surface.get_pixel(self.current_row, self.current_col)[:3] == Color.BLACK:
		 	self.current_row += 1

	def burn_space(self):
		while self.current_row < self.right and self.survey_surface.get_pixel(self.current_row, self.current_col)[:3] == Color.BLACK:
			self.current_row += 1

	def get_row(self):
		self.tuples = []
		self.burn_space()
		while self.current_row < self.right:		
			previous_row = self.current_row
			self.burn_contiguous()
			self.tuples.append((previous_row, self.current_row))
			self.burn_space()
		if self.tuples:
			return SurveyedRow(self.current_col, *self.tuples)
		return None

	def next_row(self):
		row = self.get_row()
		if row:
			self.rows.append(row)
		self.current_row = 0
		self.current_col += 1
		if self.current_col >= self.bottom:
			return False
		return True

	def survey(self):
		self.current_row = self.left
		self.current_col = self.top
		self.loop()

	def loop(self):
		while True:
			if not self.next_row():
				return

	def is_rendered(self):
		self.survey()
		has_top, has_bottom, has_left, has_right = False, False, False, False
		if len(self.rows[0].parts) == 1 and self.rows[0].parts[0].get_length() == self.char_width:
			has_top = True
		if len(self.rows[-1].parts) == 1 and self.rows[-1].parts[0].get_length() == self.char_width:
			has_bottom = True
		l, r = 0, 0
		for row in self.rows:
			if row.parts[0].left == self.left:
				l += 1
			if row.parts[-1].right == self.right:
				r += 1
		if l == self.char_height:
			has_left = True
		if r == self.char_height:
			has_right = True
		return not has_top or not has_bottom or not has_right or not has_left

def survey_char(letter = '2:', font_number=46, font_size=20):
	pygame.init()
	dimensions = (1920, 1080)
	font_name = pygame.font.get_fonts()[font_number]
	print('\nFont:\n{0}\n'.format(font_name))
	font_info = FontInfo(font_name, font_size, Color.WHITE)
	survey_letter = SurveyedLetter(letter, font_info, dimensions, Color.BLACK)
	survey_letter.survey()
	print(survey_letter, end='\n\n')
	survey_letter.print_as_letter()

def print_char_from_problem_fonts(letter = '0', font_size=20):
	pygame.init()
	#problem_fonts = [46, 63, 68, 69, 74, 94, 169, 181, 196, 197, 198]
	problem_fonts = [17, 47, 64, 69, 70, 95, 167, 173, 185, 200, 201]
	dimensions = (1920, 1080)
	for font_number in problem_fonts:
		font_name = font_name = pygame.font.get_fonts()[font_number]
		font_info = FontInfo(font_name, font_size, Color.WHITE)
		print('\nFont:\n{0}\n'.format(font_name))
		survey_letter = SurveyedLetter(letter, font_info, dimensions, Color.BLACK)
		survey_letter.survey()
		survey_letter.print_as_letter()

def check_one_font(font_number=46):
	pygame.init()	
	font_info = FontInfo(pygame.font.get_fonts()[font_number], 20, Color.WHITE)
	survey_letter = SurveyedLetter('0', font_info, (1920, 1080), Color.BLACK)
	if survey_letter.is_rendered():
		print('Rendered...')
	else:
		print('Not Rendered...')			

def check_all_fonts():
	pygame.init()
	dimensions = (1920, 1080)
	font_size = 20
	text_color = Color.WHITE
	background_color = Color.BLACK
	letter = '3'
	rendered = []
	not_rendered = []
	for i, font_name in enumerate(pygame.font.get_fonts()):
		font_info = FontInfo(font_name, font_size, text_color)
		survey_letter = SurveyedLetter(letter, font_info, dimensions, background_color)
		name = '{0}) {1}'.format(i, font_name)
		if survey_letter.is_rendered():
			rendered.append(name)
		else:
			not_rendered.append(name)
	print('\nRendered:')
	print('\n'.join(rendered))
	print('\nUnRendered:')
	print('\n'.join(not_rendered))

class AssayEdge:
	def __init__(self, survey_surface, position, direction, length, break_color):
		self.survey_surface = survey_surface
		self.length = length 
		self.position = position
		self.dir_x, self.dir_y = direction
		self.break_color = break_color 

	def assay(self):
		count = 0
		x, y = self.position
		while count < self.length:
			if self.survey_surface.get_pixel(x, y) == self.break_color:
				break
			count += 1
			x, y = x + self.dir_x, y + self.dir_y
		else:
			return True
		return False

class Survey:
	def __init__(self, letter, font_info, dimensions, background_color):
		self.letter = letter
		self.font_info = font_info
		self.width, self.height = dimensions
		self.background_color = background_color
		self.survey_surface = SurveySurface(self.letter, self.font_info, dimensions, self.background_color)
		self.char_width = self.survey_surface.get_char_width()
		self.char_height = self.survey_surface.get_char_height()
		self.left, self.right = (self.width//2, self.width//2 + self.char_width)
		self.top, self.bottom = (self.height//2, self.height//2 + self.char_height)

	def assay(self):
		left = AssayEdge(self.survey_surface, (self.left, self.top), (0, 1), self.char_height, self.background_color)
		right = AssayEdge(self.survey_surface, (self.right-1, self.top), (0, 1), self.char_height, self.background_color)
		top = AssayEdge(self.survey_surface, (self.left, self.top), (1, 0), self.char_width, self.background_color)
		bottom = AssayEdge(self.survey_surface, (self.left, self.bottom-1), (1, 0), self.char_width, self.background_color)
		return left.assay() and right.assay() and top.assay() and bottom.assay()

def check_font(font_name):
	font_info = FontInfo(font_name, 10, Color.WHITE)
	survey = Survey('5', font_info, (1920, 1080), Color.BLACK)
	return not survey.assay()
	
if __name__=='__main__':
	import sys
	print()
	print('Args:')
	for i, arg in enumerate(sys.argv):
		print('{0}) {1}'.format(i+1, arg))
	if len(sys.argv) == 3:
		print_char_from_problem_fonts(sys.argv[1], int(sys.argv[2]))
	elif len(sys.argv) == 4:
		survey_char(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
	else:
		check_all_fonts()