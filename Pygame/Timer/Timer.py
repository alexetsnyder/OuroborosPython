#C:\Users\asnyder\AppData\Local\Programs\Python\Python36-32\python.exe Timer.py
import time
import math
import pygame
import winsound
from Color import Color

#Features
#Keyboard to fill out timer, and to pause with space
#Change eEvents to eCustomEvents
#Button has rect, and acts more like button
#Can change colors
#Beeping class
#Show all fonts?
#Size Bar

def print_rect(rect):
	print('(x, y) = {0}, (w, h) = ({1}, {2})'.format(rect.center, rect.width, rect.height))

class eEvents:
	TIMER_EXPIRED = 0
	BUTTON_PRESS  = 1
	PLAY_SOUND    = 2

class Timer:
	def __init__(self):
		self.running = False
		self.previous = 0
		self.end_time = 0
		self.time_left = 0

	def set_time(self, seconds):
		self.end_time = seconds
		self.time_left = seconds

	def start(self):
		if self.time_left > 0:
			self.running = True
			self.previous = time.time()

	def pause(self):
		self.running = False

	def restart(self):
		self.time_left = self.end_time
		self.start()

	def reset(self):
		self.running = False
		self.previous = 0
		self.end_time = 0
		self.time_left = 0
		
	def update(self):
		if self.running:
			current = time.time()
			self.time_left -= (current - self.previous)
			self.previous = current
			if self.time_left <= 0:
				self.time_left = 0
				self.alarm()

	def alarm(self):
		self.running = False
		event = pygame.event.Event(pygame.USEREVENT, name=eEvents.TIMER_EXPIRED)
		pygame.event.post(event)
	
	def get_time(self):
		r_time = math.ceil(self.time_left)
		return ((r_time//60//60), (r_time//60)%60, r_time%60)

def in_rect(rect, pos):
	x2, y2 = pos 
	x1, y1 = rect.center 
	#print('(x1, y1) = ({0}, {1}), (x2, y2) = ({2}, {3}), (w, h) = ({4}, {5})'.format(x1, y1, x2, y2, rect.width, rect.height))
	return ((rect.width/2) ** 2 >= (x2 - x1) ** 2) and ((rect.height/2) ** 2 >= (y2 - y1) ** 2)
	
class Text:
	def __init__(self, text, center, font_size, font_color, font_name='lucidaconsole'):
		self.text = text
		self.center = center
		self.font_size = font_size
		self.font_color = font_color
		self.font_name = font_name
		self.font = pygame.font.SysFont(self.font_name, self.font_size)
		self.surface = self.font.render(self.text, True, self.font_color)
		self.rect = self.surface.get_rect()
		self.update()
		
	def size(self):
		return self.font.size(self.text)

	def is_within(self, position):
		return in_rect(self.rect, position)

	def set_center(self, center):
		self.center = center
		self.update()

	def get_center(self):
		return self.center

	def set_text(self, text):
		self.text = text 
		self.surface = self.font.render(self.text, True, self.font_color)

	def update(self):
		self.rect.center = self.center
	
	def draw_to(self, surface):
		#pygame.draw.rect(surface, Color.SILVER, self.rect, 2)
		surface.blit(self.surface, self.rect)

class Image:
	def __init__(self, file_path, center, dimensions):
		self.file_path = file_path
		self.center = center
		self.width, self.height = dimensions
		self.image = pygame.image.load(self.file_path)
		self.image = pygame.transform.scale(self.image, (self.width, self.height))
		self.rect = self.image.get_rect()
		self.rect.center = self.center
		self.rect.width, self.rect.height = self.width, self.height

	def is_within(self, position):
		return in_rect(self.rect, position)

	def draw_to(self, surface):
		surface.blit(self.image, self.rect)

class Rect:
	def __init__(self, center, dimensions, color, width=0):
		self.center = self.x, self.y = center
		self.width, self.height = dimensions
		self.border_width = width
		self.color = color
		self.rect = pygame.Rect((self.x - self.width/2, self.y - self.height/2), dimensions)

	def set_center(self, center):
		self.center = center 
		self.rect.center = center

	def is_within(self, position):
		return in_rect(self, position)

	def draw_to(self, surface):
		pygame.draw.rect(surface, self.color, self.rect, self.border_width)

class eButton:
	PAUSE   = 0
	START   = 1
	RESTART = 2
	CANCEL  = 3

class Button:
	def __init__(self, file_name, button, center, dimensions):
		self.center = center 
		self.file_name = file_name
		self.dimensions = dimensions
		self.button = button
		self.button_image = Image(file_name, center, dimensions)
		
	def is_clicked(self, position):
		return self.button_image.is_within(position)

	def on_click(self):
		event = pygame.event.Event(pygame.USEREVENT, name=eEvents.BUTTON_PRESS, button=self.button)
		pygame.event.post(event)

	def draw_to(self, surface):
		self.button_image.draw_to(surface)

class eTimerState:
	START   = 0
	PAUSE   = 1
	EXPIRED = 2

class TimerControlButtons:
	def __init__(self, center):
		x, y = center
		dimensions = w, h = (80, 80)
		self.margin = 10
		self.start_button = Button('start.png', eButton.START, center, dimensions)
		self.pause_button = Button('pause.png', eButton.PAUSE, center, dimensions)
		self.restart_button = Button('restart.png', eButton.RESTART, (x - w/2 - self.margin/2, y), dimensions)
		self.cancel_button = Button('cancel.png', eButton.CANCEL, (x + w/2 + self.margin/2, y), dimensions)
		self.states = {eTimerState.START : (self.start_button,), eTimerState.PAUSE : (self.pause_button,), eTimerState.EXPIRED : (self.restart_button, self.cancel_button)}
		self.current_state = eTimerState.START

	def switch_state(self, state):
		self.current_state = state

	def on_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
			for button in self.states[self.current_state]:
				if button.is_clicked(mouse_pos):
					button.on_click()
		elif event.type == pygame.USEREVENT:
			if event.name == eEvents.TIMER_EXPIRED:
				self.switch_state(eTimerState.EXPIRED)
			elif event.name == eEvents.BUTTON_PRESS:
				if event.button == eButton.START:
					self.switch_state(eTimerState.PAUSE)
				elif event.button == eButton.PAUSE:
					self.switch_state(eTimerState.START)
				elif event.button == eButton.RESTART:
					self.switch_state(eTimerState.PAUSE)
				elif event.button == eButton.CANCEL:
					self.switch_state(eTimerState.START)	

	def draw_to(self, surface):
		for button in self.states[self.current_state]:
			button.draw_to(surface)
	
class CounterDisplay:
		def __init__(self, limit, center, font_size, font_color, font_name='lucidaconsole'):
			self.count = 0
			self.text = self.format_text()
			self.limit = limit
			self.display = Text(self.text, center, font_size, font_color, font_name)
			self.is_dirty = False
			
		def format_text(self):
			return '{0}{1}'.format('' if len(str(self.count)) > 1 else '0', self.count)

		def size(self):
			return self.display.size()

		def get_count(self):
			return self.count

		def set_center(self, center):
			self.display.set_center(center)
		
		def is_clicked(self, position):
			return self.display.is_within(position)

		def on_click(self, mouse_button):
			self.is_dirty = True
			if mouse_button == eMouseButton.LEFT:
				self.count += 1
				if self.count == self.limit:
					self.count = 0
			elif mouse_button == eMouseButton.RIGHT:
				self.count = 0

		def clear(self):
			self.count = 0
			
		def set_display(self, value):
			self.count = value

		def update_text(self):
			self.text = self.format_text()
			self.display.set_text(self.text)
			
		def update(self):
			self.update_text()
			self.display.update()
			self.is_dirty = False 
			
		def draw_to(self, surface):
			# x, y = self.display.get_center()
			# w, h = self.size()
			# pygame.draw.rect(surface, Color.SILVER, pygame.Rect((x-w/2, y-h/2), (w, h)), 2)
			self.display.draw_to(surface)
	
class eMouseButton:
	LEFT           = 1
	MIDDLE         = 2
	RIGHT          = 3
	FORWARD_WHEEL  = 4
	BACKWARD_WHEEL = 5

class ClockDisplay:
	def __init__(self, center, font_size, font_color, font_name='lucidaconsole'):
		self.colon_str = ':'
		self.dx_m = -40
		self.cx_m = 8
		self.cy_m = -5
		self.center = center
		pos_gen = self.get_next_pos(center)
		self.hour = CounterDisplay(24, center, font_size, font_color, font_name)
		self.colon_text1 = Text(self.colon_str, pos_gen(self.hour, self.dx_m, self.cy_m), font_size, font_color, font_name)
		self.minute = CounterDisplay(60, pos_gen(self.colon_text1, self.cx_m), font_size, font_color, font_name)
		self.colon_text2 = Text(self.colon_str, pos_gen(self.minute, self.dx_m, self.cy_m), font_size, font_color, font_name)
		self.second = CounterDisplay(60, pos_gen(self.colon_text2, self.cx_m), font_size, font_color, font_name)
		self.center_display()
		self.timer = Timer()
		self.timer_expired_text = Text('Timer Expired!', self.center, font_size//2, font_color, font_name)
		self.display_timer_expired_text = False
		self.sound_after_draw = False
		self.play_timer_expired_sound = False
		self.border_rect = Rect(self.center, (self.total_width()+10, self.hour.size()[1]+10), Color.SILVER)
		self.background_rect = Rect(self.center, (self.total_width(), self.hour.size()[1]), Color.BLUE)
	
	def center_display(self):
		total_width = self.total_width()
		x, y = self.center
		x -= total_width/2 - self.hour.size()[0]/2
		pos_gen = self.get_next_pos((x, y))
		self.hour.set_center((x, y))
		self.colon_text1.set_center(pos_gen(self.hour, self.dx_m, self.cy_m))
		self.minute.set_center(pos_gen(self.colon_text1, self.cx_m))
		self.colon_text2.set_center(pos_gen(self.minute, self.dx_m, self.cy_m))
		self.second.set_center(pos_gen(self.colon_text2, self.cx_m))

	def total_width(self):
		return self.hour.size()[0] + self.dx_m + self.colon_text1.size()[0] + self.cx_m + self.minute.size()[0] + self.dx_m + self.colon_text2.size()[0] + self.cx_m + self.second.size()[0]

	def on_event(self, event):
		if event.type == pygame.USEREVENT:
			if event.name == eEvents.BUTTON_PRESS:
				if event.button == eButton.START:
					if self.get_time() > 0:
						self.timer.set_time(self.get_time())
						self.timer.start()
				elif event.button == eButton.PAUSE:
					self.timer.pause()
				elif event.button == eButton.RESTART:
					self.timer.restart()
					self.display_timer_expired_text = False
				elif event.button == eButton.CANCEL:
					self.timer.reset()
					self.display_timer_expired_text = False
			elif event.name == eEvents.TIMER_EXPIRED:
				self.zero_display()
				self.display_timer_expired_text = True
				self.play_timer_expired_sound = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
			if self.hour.is_clicked(mouse_pos):
				self.hour.on_click(event.button)
			elif self.minute.is_clicked(mouse_pos):
				self.minute.on_click(event.button)
			elif self.second.is_clicked(mouse_pos):
				self.second.on_click(event.button)

	def zero_display(self):
		self.hour.set_display(0)
		self.minute.set_display(0)
		self.second.set_display(0)

	def update(self):
		if self.play_timer_expired_sound:
			if self.sound_after_draw:
				for i in range(3):
					winsound.Beep(440, 500)
				self.play_timer_expired_sound = False
				self.sound_after_draw = False
			else:
				self.sound_after_draw = True
			
		self.timer.update()
		if self.timer.running:
			self.update_clock()
		self.hour.update() 
		self.minute.update()
		self.second.update()
	
	def draw_to(self, surface):
		if self.display_timer_expired_text:
			self.timer_expired_text.draw_to(surface)
		else:
			self.border_rect.draw_to(surface)
			self.background_rect.draw_to(surface)
			self.hour.draw_to(surface)
			self.colon_text1.draw_to(surface)
			self.minute.draw_to(surface)
			self.colon_text2.draw_to(surface)
			self.second.draw_to(surface)
	
	def get_time(self):
		return self.hour.get_count() * 3600 + self.minute.get_count() * 60 + self.second.get_count()

	def update_clock(self):
		h, m, s = self.timer.get_time()
		self.hour.set_display(h)
		self.minute.set_display(m)
		self.second.set_display(s)

	def get_next_pos(self, position):
		x, y = position
		def func(object, xm=0, ym=0):
			nonlocal x 
			x += object.size()[0] + xm
			return x, y + ym
		return func
		
class App:
	WINDOW_SIZE = (640, 400)

	def __init__(self):
		pygame.init()
		w, h = App.WINDOW_SIZE
		self._running = True
		self.clock_display = ClockDisplay((w/2, h/2), 80, Color.RED)
		self.buttons = TimerControlButtons((w/2, h/2+100))
		self.surface = pygame.display.set_mode(App.WINDOW_SIZE, pygame.HWSURFACE)
		
	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self._running = False 
		self.clock_display.on_event(event)
		self.buttons.on_event(event)
		
	def update(self):
		self.clock_display.update() 
		
	def draw(self):
		self.surface.fill(Color.BLACK)
		self.clock_display.draw_to(self.surface)
		self.buttons.draw_to(self.surface)
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