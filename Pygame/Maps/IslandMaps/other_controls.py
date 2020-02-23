#other_controls.py
import math, time
import go, imp, events
from geo import plottable
from structs import *

class StopWatch (Control):
	def __init__(self, left_top=(0, 0), color=Color.BLACK, digit_color=Color.RED):
		self.color = color 
		self.digit_color = digit_color
		self.is_visible = True
		self.time = 0
		self.prv_time = 0
		self.padding = 4
		self.is_running = False
		self.font_info = go.FontInfo(font_size=20, font_color=digit_color)
		self.seperator_txt = go.RenderText(':', self.font_info)
		self.seconds_txt = go.RenderText(self.display_format(0), self.font_info)
		self.minutes_txt = go.RenderText(self.display_format(0), self.font_info)
		self.hours_txt = go.RenderText(self.display_format(0), self.font_info)
		self.box = go.Rect(left_top, (0, 0), color=color)
		super().__init__(left_top, (0, 0), default_size=self.get_clock_size())

	def set_display(self):
		hours, minutes, seconds = self.get_time()
		if hours >= 24:
			self.time = 0
			hours, minutes, seconds = (0, 0, 0)
		self.seconds_txt.set_text(self.display_format(seconds))
		self.minutes_txt.set_text(self.display_format(minutes))
		self.hours_txt.set_text(self.display_format(hours))

	def display_format(self, time):
		return '{:02}'.format(time)

	def set_size(self, size):
		super().set_size(size)
		self.box.set_size(size)

	def set_position(self, left_top):
		super().set_position(left_top)
		self.box.set_position(self.left_top)
		left = self.left + self.padding * 2
		self.hours_txt.set_position((left, self.y - self.hours_txt.h // 2))
		left += self.hours_txt.w + self.seperator_txt.w + self.padding
		self.minutes_txt.set_position((left, self.y - self.minutes_txt.h // 2))
		left += self.minutes_txt.w + self.seperator_txt.w + self.padding
		self.seconds_txt.set_position((left, self.y - self.seconds_txt.h // 2))

	def get_clock_size(self):
		clock_width =  self.padding + self.hours_txt.w + self.padding // 2
		clock_width += self.seperator_txt.w + self.padding // 2
		clock_width += self.minutes_txt.w + self.padding // 2
		clock_width += self.seperator_txt.w + self.padding // 2
		clock_width += self.seconds_txt.w + self.padding
		return (clock_width, self.seconds_txt.h + self.padding)

	def get_time(self):
		r_time = math.ceil(self.time)
		return ((r_time//60//60), (r_time//60)%60, r_time%60)

	def set_visibility(self, is_visible):
		self.is_visible = is_visible
		self.box.set_visibility(self.is_visible)
		self.seperator_txt.set_visibility(self.is_visible)
		self.hours_txt.set_visibility(self.is_visible)
		self.minutes_txt.set_visibility(self.is_visible)
		self.seconds_txt.set_visibility(self.is_visible)

	def start(self):
		self.prv_time = time.time()
		self.is_running = True

	def stop(self):
		self.is_running = False

	def reset(self):
		self.is_running = False
		self.time = self.prv_time = 0

	def tick(self):
		if self.is_running:
			current = time.time()
			self.time += current - self.prv_time 
			self.prv_time = current

	def update(self):
		self.tick()
		self.set_display()
		self.set_position(self.origin)
		self.seperator_txt.update()
		self.seconds_txt.update()
		self.minutes_txt.update()
		self.hours_txt.update()
		self.box.update()

	def draw_clock(self, surface):
		left = self.left + self.padding + 2
		self.hours_txt.draw(surface)
		left += self.hours_txt.w + self.padding
		self.seperator_txt.draw_at(surface, (left, self.top + self.h // 4 + 2))
		left += self.seperator_txt.w + self.padding // 2
		self.minutes_txt.draw(surface)
		left += self.minutes_txt.w + 2
		self.seperator_txt.draw_at(surface, (left, self.top + self.h // 4 + 2))
		self.seconds_txt.draw(surface)

	def draw(self, surface):
		self.box.draw(surface)
		self.draw_clock(surface)
		super().draw(surface)

class CounterBox (Control):
	def __init__(self, digits, can_grow=False, limit=100, left_top=(0, 0), color=Color.BLACK, digit_color=Color.RED):
		self.color = color 
		self.digit_color = digit_color
		self.limit = limit
		self.can_grow = can_grow
		self.digits = digits
		self.post_update = False
		self.div = 10 * int('{}{}'.format(1, ''.join(['0' for i in range(self.digits-1)])))
		self.counter = 0
		self.padding = 4
		self.is_visible = True
		self.box = go.Rect(left_top, (0, 0), color=color)
		self.font_info = go.FontInfo(font_size=30, font_color=digit_color)
		self.display_text = go.RenderText(self.get_display_str(), font_info=self.font_info)
		super().__init__(left_top, (0, 0), default_size=tuple(x + self.padding for x in self.display_text.size))

	def set_size(self, size):
		super().set_size(size)
		self.box.set_size(size)

	def set_position(self, left_top):
		super().set_position(left_top)
		self.box.set_position((self.left, self.top))
		self.display_text.center_on(self.center)

	def get_display_str(self):
		format_str = '{:0' + str(self.digits) + '}'
		return format_str.format(self.counter)

	def post_sidebar_refresh(self):
		events.UserEvent(CustomEvent.REFRESH_SIDEBAR).post()

	def set_visibility(self, is_visible):
		self.is_visible = is_visible
		self.box.set_visibility(self.is_visible)
		self.display_text.set_visibility(self.is_visible)

	def reset(self):
		self.counter = 0

	def increment(self, n=1):
		self.counter += n 

	def decrement(self, n=1):
		self.counter -= n

	def update_counter(self):
		if self.can_grow and self.counter / self.div >= 1:
			self.div *= 10
			self.post_update = True
			self.post_sidebar_refresh()
		elif not self.can_grow and self.counter >= self.limit:
			self.counter = 0

	def update(self):
		self.update_counter()
		self.display_text.set_text(self.get_display_str())
		if self.post_update:
			self.set_size(tuple(x + self.padding for x in self.display_text.size))
			self.set_position(self.origin)
			self.post_update = False
		self.display_text.update()
		self.box.update()

	def draw(self, surface):
		self.box.draw(surface)
		self.display_text.draw(surface)
		super().draw(surface)

if __name__=='__main__':
	import pygame
	pygame.init()

	imp.IMP().event_dispatcher = events.EventDispatcher()

	left_btn = Button('Left')
	right_btn = Button('Right')
	top_btn = Button('Top')
	bottom_btn = Button('Bottom')
	disable_btn = Button('Disable')
	check_box = CheckBox('Checked', on_checked= lambda event : print('(Un)Checked!'))
	counter_box = CounterBox(4, can_grow=True)
	increment_btn = Button('Increment', lambda event : counter_box.increment(1000))
	stop_watch = StopWatch()
	start_btn = Button('Start', lambda event : stop_watch.start())
	stop_btn = Button('Stop', lambda event : stop_watch.stop())
	reset_btn = Button('Reset', lambda event : stop_watch.reset())

	controls = []
	controls.append(left_btn)
	controls.append(right_btn)
	controls.append(top_btn)
	controls.append(bottom_btn)
	controls.append(disable_btn)
	controls.append(counter_box)
	controls.append(increment_btn)
	controls.append(stop_watch)
	controls.append(start_btn)
	controls.append(stop_btn)
	controls.append(reset_btn)
	controls.append(check_box)
	side_bar = SideBar((600, 400), WindowSide.LEFT, controls=controls)

	def on_left_click(event):
		side_bar.set_window_side(WindowSide.LEFT)

	def on_right_click(event):
		side_bar.set_window_side(WindowSide.RIGHT)

	def on_top_click(event):
		side_bar.set_window_side(WindowSide.TOP)

	def on_bottom_click(event):
		side_bar.set_window_side(WindowSide.BOTTOM)

	def toggle_controls_enabled(event):
		controls_enabled = not left_btn.is_enabled
		left_btn.set_enabled(controls_enabled)
		right_btn.set_enabled(controls_enabled)
		top_btn.set_enabled(controls_enabled)
		bottom_btn.set_enabled(controls_enabled)
		check_box.set_enabled(controls_enabled)
		increment_btn.set_enabled(controls_enabled)
		start_btn.set_enabled(controls_enabled)
		stop_btn.set_enabled(controls_enabled)
		reset_btn.set_enabled(controls_enabled)

	left_btn.set_onclick(on_left_click)
	right_btn.set_onclick(on_right_click)
	top_btn.set_onclick(on_top_click)
	bottom_btn.set_onclick(on_bottom_click)
	disable_btn.set_onclick(toggle_controls_enabled)

	def update():
		side_bar.update()

	def draw(surface):
		surface.fill(Color.TEAL_FELT)
		side_bar.draw(surface)
		pygame.display.flip()

	surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
	running = True
	while running:
		for event in pygame.event.get():
			imp.IMP().dispatch(event)
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.VIDEORESIZE:
				surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
		update()
		draw(surface)
	pygame.quit()