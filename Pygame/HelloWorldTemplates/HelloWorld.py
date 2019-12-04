import pygame
from pygame import freetype

class Color:
	WHITE  		  = (255, 255, 255)
	BLACK  		  = (  0,   0,   0)
	RED           = (255,   0,   0)
	GREEN  		  = (  0, 255,   0)
	SEA_GREEN     = ( 46, 139,  87)
	FOREST_GREEN  = ( 13,  55,  13)
	BLUE   		  = (  0,   0, 255)
	DEEP_SKY_BLUE = (  0, 191, 255)
	YELLOW 		  = (255, 255,   0)
	SAND          = ( 76,  70,  50)
	SILVER 		  = (192, 192, 192)

class FontInfo:
	def __init__(self, font_name, font_size, font_color):
		self.font_name = font_name
		self.font_size = font_size
		self.font_color = font_color

class RenderText:
	def __init__(self, text_str, font_info, position=(0,0)):
		self.text_str = text_str
		self.font_info = font_info
		self.position = position
		self.font = freetype.SysFont(self.font_info.font_name, self.font_info.font_size)
		self.width = self.font.get_rect(self.text_str).width
		self.height = self.font.get_rect(self.text_str).height

	def draw_to(self, surface):
		x, y = self.position
		self.font.render_to(surface, (x - self.width / 2, y - self.height / 2), self.text_str, self.font_info.font_color)

class App:
	WINDOW_SIZE = (640, 400)

	def __init__(self):
		pygame.init()
		self.running = True
		self.font_info = FontInfo('lucidaconsole', 40, Color.WHITE)
		self.surface = pygame.display.set_mode(App.WINDOW_SIZE, pygame.HWSURFACE)
		self.text = RenderText('Hello World!', self.font_info, tuple(x // 2 for x in App.WINDOW_SIZE))

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self.running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.running = False

	def update(self):
		pass

	def draw(self):
		self.surface.fill(Color.BLACK)
		self.text.draw_to(self.surface)
		pygame.display.flip()

	def game_loop(self):
		while self.running:
			for event in pygame.event.get():
				self.on_event(event)
			self.update()
			self.draw()

	def clean_up(self):
		pygame.quit()

	def run(self):
		self.game_loop()
		self.clean_up()

if __name__=='__main__':
	app = App()
	app.run()