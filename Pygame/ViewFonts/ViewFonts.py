#C:\Users\asnyder\AppData\Local\Programs\Python\Python36-32\python.exe ViewFonts.py
import pygame
import functools
from pygame import freetype
from Color import Color
from SurveyFont import check_font

class Text:
	ID = 0

	def __init__(self, text, font_name, font_size):
		self.text = text
		self.font_size = font_size
		self.font_color = Color.WHITE
		self.font_name = font_name
		self.font = freetype.SysFont(self.font_name, self.font_size)
		self.height = self.font.get_rect(self.text).height
		self.width = self.font.get_rect(self.text).width
		self.id = Text.ID
		Text.ID += 1

	def draw_to(self, surface, position):
		x, y = position
		self.font.render_to(surface, (x - self.width/2, y), self.text, self.font_color)

class eMouseButton:
	LEFT           = 1
	MIDDLE         = 2
	RIGHT          = 3
	FORWARD_WHEEL  = 4
	BACKWARD_WHEEL = 5

class ScrollView:
	def __init__(self, objects, dimensions, sensitivity=10, min_height=10):
		self.current = min_height
		self.objects = objects
		self.min_height = min_height
		self.sensitivity = sensitivity
		self.width, self.height = dimensions
		self.visible = []
		self.total_height = functools.reduce((lambda x, y : x + y), [obj.height for obj in self.objects])

	def on_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == eMouseButton.FORWARD_WHEEL:
				if self.current > self.min_height:
					self.current -= self.sensitivity
			elif event.button == eMouseButton.BACKWARD_WHEEL:
				if self.current + self.sensitivity < self.total_height:
					self.current += self.sensitivity
		elif event.type == pygame.VIDEORESIZE:
			self.width = event.w

	def update(self):
		current_height = self.min_height
		self.visible.clear()
		for object in self.objects:
			current_height += object.height
			if current_height > self.current and current_height < (self.current + self.height):
				self.visible.append(object)

	def draw_to(self, surface):
		x, y = self.width/2, self.min_height
		h = 0
		for object in self.visible:
			object.draw_to(surface, (x, y + h))
			h += object.height + 10

class AllFonts:
	def __init__(self):
		self.fonts = []
		self.font_names = pygame.font.get_fonts()
		self.create_font_objects()

	def create_font_objects(self):
		for i, font in enumerate(self.font_names):
			if check_font(font):
				temp_text = Text('{0}: {1}'.format(i, font), font, 20)
				self.fonts.append(temp_text)

	def get_fonts(self):
		return self.fonts

class App:
	def __init__(self):
		pygame.init()
		self._running = True
		self.fonts = AllFonts()
		self.surface = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
		self.window_size = self.surface.get_size()
		self.scroll_view = ScrollView(self.fonts.get_fonts(), self.window_size, 50)
		
	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False
		elif event.type == pygame.VIDEORESIZE:
			self.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self._running = False 
		self.scroll_view.on_event(event)
		
	def update(self):
		self.scroll_view.update()
		
	def draw(self):
		self.surface.fill(Color.BLACK)
		self.scroll_view.draw_to(self.surface)
		pygame.display.flip()
		
	def clean_up(self):
		pygame.quit()
		
	def run(self):
		while self._running:
			for event in pygame.event.get():
				self.on_event(event)
			self.update()
			self.draw()
		self.clean_up()

if __name__=='__main__':
	app = App()
	app.run()