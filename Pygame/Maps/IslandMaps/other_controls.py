#other_controls.py
import math, time
import go, imp, events
from geo import plottable
from structs import *

@plottable
class Control:
	def __init__(self, controls=[], window_or=WindowOr.VERTICAL, default_size=(20, 20), is_override=False):
		self.mw, self.mh = self.margin = (8, 8)
		self.window_or = window_or
		self.children = controls
		self.set_default(default_size, is_override)
		self.set_size(self.assay_size())
		self.set_position(self.left_top)

	def set_position(self, left_top):
		self.position_children()

	def set_window_or(self, window_or, left_top):
		self.window_or = window_or
		self.set_size(self.assay_size())
		self.set_position(left_top)

	def set_default(self, default_size, is_override=False):
		self.set_override(is_override)
		self.default_w, self.default_h = self.default_size = default_size

	def set_override(self, is_override):
		self.is_override = is_override

	def assay_size(self):
		return (self.get_w(), self.get_h())

	def position_children(self):
		if self.window_or == WindowOr.VERTICAL:
			x = self.x
			y = self.top 
			for child in self.children:
				child.center_on((x, y + child.h // 2))
				y += child.h + self.mh
		else:
			x = self.left
			y = self.top
			for child in self.children:
				child.center_on((x + child.w // 2, y + 3 * child.h // 4))
				x += child.w + self.mw

	def get_w(self):
		if self.is_override or not any(self.children):
			return self.default_w + self.mw
		if self.window_or == WindowOr.VERTICAL:
			return self.get_max_width()	
		return self.get_total_width()

	def get_max_width(self):
		max_width = 0
		for child in self.children:
			width = child.w
			if width > max_width:
				max_width = width 
		return max_width + self.mw

	def get_total_width(self):
		total_width = 0
		for child in self.children:
			total_width += child.w
		return total_width + self.mw

	def get_h(self):
		if self.is_override or not any(self.children):
			return self.default_h + self.mh
		if self.window_or == WindowOr.VERTICAL:
			return self.get_total_height()
		return self.get_max_height()

	def get_max_height(self):
		max_height = 0
		for child in self.children:
			height = child.h
			if height > max_height:
				max_height = height
		return max_height + self.mh

	def get_total_height(self):
		total_height = 0
		for child in self.children:
			total_height += child.h
		return total_height + self.mh

	def update(self):
		for child in self.children:
			child.update()

	def draw(self, surface):
		for control in self.children:
			control.draw(surface)

class BlankControl (Control):
	def __init__(self, left_top, size):
		super().__init__(left_top, (0, 0), default_size=size)

class SideBar (Control):
	def __init__(self, window_size, side, controls=[], color=Color.SEA_GREEN):
		self.color = color 
		self.is_showing = True
		self.window_side = side 
		self.window_width, self.window_height = self.window_size = window_size
		self.btn_show = Button('', on_click=self.on_click_toggle_bar)
		controls.insert(0, self.btn_show)
		self.rect = go.Rect((0, 0), (0, 0), color=self.color)
		self.set_btn_text()
		super().__init__((0, 0), window_size, controls=controls, default_size=self.btn_show.size, window_or=self.get_windows_or())
		self.wire_events()

	def set_size(self, size):
		super().set_size(size)
		self.rect.set_size(size)

	def set_position(self, left_top):
		super().set_position(left_top)
		left, top = left_top
		w, h = self.btn_show.size 
		button_center = (left + self.w - w // 2, top + h // 2)
		if self.window_side == WindowSide.RIGHT:
			left, top = (left + self.window_width - self.w, top)
			button_center = (left + w // 2, top + h // 2)
		elif self.window_side == WindowSide.TOP:
			button_center = (left + w // 2, top + self.h - h // 2 - 2)
		elif self.window_side == WindowSide.BOTTOM:
			left, top = (left, top + self.window_height - self.h)
			button_center = (left + w // 2, top + h // 2)
		self.rect.set_position((left, top))
		self.btn_show.center_on(button_center)

	def set_default(self, size, is_override=False):
		w, h = size 
		new_size = None
		if self.window_side in [WindowSide.LEFT, WindowSide.RIGHT]:
			new_size = (w - self.mw, h)
		elif self.window_side in [WindowSide.TOP, WindowSide.BOTTOM]:
			new_size = (w, h - self.mh)
		super().set_default(new_size, is_override)

	def set_window_side(self, window_side):
		self.window_side = window_side
		self.set_btn_text()
		self.set_window_or(self.get_windows_or(), (0, 0))

	def get_windows_or(self):
		if self.window_side in [WindowSide.LEFT, WindowSide.RIGHT]:
			return WindowOr.VERTICAL
		else:
			return WindowOr.HORIZONTAL
		
	def wire_events(self):
		imp.IMP().add_listener(events.WindowResizedEvent().listen(self.on_resize))
		imp.IMP().add_listener(events.UserEvent(CustomEvent.REFRESH_SIDEBAR).listen(self.on_refresh_sidebar))

	def on_resize(self, event):
		self.window_width, self.window_height = self.window_size = (event.w, event.h)
		self.set_size(self.assay_size())
		self.set_position((0, 0))

	def on_refresh_sidebar(self, event):
		self.set_size(self.assay_size())
		self.set_position((0, 0))

	def on_click_toggle_bar(self, event):
		self.toggle_bar()

	def toggle_bar(self):
		self.is_showing = not self.is_showing
		self.set_btn_text()
		if self.is_showing:
			self.set_override(False)
			self.show_buttons()
		else:
			self.set_override(True)
			self.show_buttons(is_show=False)	
		self.set_size(self.assay_size())
		self.set_position((0, 0))

	def set_btn_text(self):
		left_btn_text = '<<<'
		right_btn_text = '>>>'
		top_btn_text = '/\\'
		bottom_btn_text = '\\/'
		if not self.is_showing:
			left_btn_text, right_btn_text = right_btn_text, left_btn_text
			top_btn_text, bottom_btn_text = bottom_btn_text, top_btn_text
		if self.window_side == WindowSide.LEFT:
			self.btn_show.set_text(left_btn_text)
		elif self.window_side == WindowSide.RIGHT:
			self.btn_show.set_text(right_btn_text)
		elif self.window_side == WindowSide.TOP:
			self.btn_show.set_text(top_btn_text)
		else: #self.window_side == WindowSide.BOTTOM:
			self.btn_show.set_text(bottom_btn_text)

	def show_buttons(self, is_show=True):
		for btn in self.children:
			btn.set_visibility(is_show)
		self.btn_show.set_visibility(True)

	def enable_buttons(self, is_enabled=True):
		for btn in self.children:
			btn.set_enabled(is_enabled)
		self.btn_show.set_enabled(True)

	def get_w(self):
		if self.window_side in [WindowSide.LEFT, WindowSide.RIGHT]:
			return super().get_w()
		return self.window_width

	def get_h(self):
		if self.window_side in [WindowSide.TOP, WindowSide.BOTTOM]:
			return super().get_h()
		return self.window_height

	def update(self):
		self.rect.update()
		super().update()

	def draw(self, surface):
		self.rect.draw(surface)
		super().draw(surface)

class Button (Control):
	def __init__(self, btn_str, on_click=None, left_top=(0, 0), color=Color.ALICE_BLUE, active_color=Color.RED):
		self.color = color 
		self.is_active = False
		self.is_enabled = True
		self.is_visible = True
		self.on_click = on_click
		self.active_color = active_color
		self.btn_font = go.FontInfo(font_size=10, font_color=Color.BLACK)
		self.btn_text = go.RenderText(btn_str, self.btn_font)
		self.rect = go.Rect(left_top, (0, 0), color=self.color)
		super().__init__(left_top, (0, 0), default_size=self.btn_text.size)
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_listener(events.MouseMotionEvent().listen(self.on_mouse_motion, quell=True))
		imp.IMP().add_listener(events.MouseLeftButtonDownEvent().listen(self.on_mouse_left_button_down))

	def set_size(self, size):
		super().set_size(size)
		self.rect.set_size(size)

	def set_position(self, left_top):
		super().set_position(left_top)
		self.rect.set_position(left_top)
		self.btn_text.center_on(self.center)

	def set_text(self, text):
		self.btn_text.set_text(text)
		self.set_size(tuple(x + 6 for x in self.btn_text.size))
		self.set_default(self.btn_text.size)

	def set_onclick(self, method):
		self.on_click = method 

	def on_mouse_motion(self, event):
		if self.rect.is_within(event.pos):
			self.is_active = True
		else:
			self.is_active = False

	def on_mouse_left_button_down(self, event):
		if self.rect.is_within(event.pos):
			self.click(event)

	def click(self, event):
		if self.is_enabled and self.is_visible:
			if not self.on_click == None:
				self.on_click(event)

	def set_enabled(self, is_enabled):
		self.is_enabled = is_enabled
		if self.is_enabled:
			self.btn_font.font_color = Color.BLACK
		else:
			self.btn_font.font_color = Color.GREY
		self.btn_text.set_font_info(self.btn_font)

	def set_visibility(self, is_visible):
		self.is_visible = is_visible
		self.btn_text.set_visibility(is_visible)
		self.rect.set_visibility(is_visible)

	def get_color(self):
		if self.is_enabled and self.is_active:
			return self.active_color
		else:
			return self.color

	def draw(self, surface):
		self.rect.set_color(self.get_color())
		self.rect.draw(surface)
		self.btn_text.draw(surface)
		super().draw(surface)

class CheckBox (Control):
	def __init__(self, lbl_str, left_top=(0, 0), on_checked=None, is_checked=False, color=Color.TEAL_FELT, checked_color=Color.BLACK):
		self.is_checked = is_checked
		self.color = color 
		self.checked_color = checked_color
		self.is_active = False
		self.is_enabled = True
		self.is_visible = True
		self.on_checked = on_checked
		self.font_info = go.FontInfo(font_size=10, font_color=Color.BLACK)
		self.lbl_text = go.RenderText(lbl_str, self.font_info)
		self.check_box = go.Rect(left_top, (10, 10), color=color, width=1)
		self.fill_box = go.Rect(left_top, (10, 10), color=checked_color)
		super().__init__(left_top, (0, 0), default_size=tuple(x + 10 for x in self.lbl_text.size))
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_listener(events.MouseLeftButtonDownEvent().listen(self.on_mouse_left_button_down))

	def set_position(self, left_top):
		super().set_position(left_top)
		self.check_box.set_position(left_top)
		self.fill_box.set_position(left_top)
		self.lbl_text.set_position((self.left + 12, self.top + self.lbl_text.h // 8))

	def set_text(self, text):
		self.lbl_text.set_text(text)
		self.set_default(tuple(x + 10 for x in self.lbl_text.size))

	def set_onchecked(self, method):
		self.on_checked = method 

	def on_mouse_left_button_down(self, event):
		if self.check_box.is_within(event.pos):			
			self.checked(event)

	def checked(self, event):
		if self.is_enabled and self.is_visible:
			self.is_checked = not self.is_checked
			if not self.on_checked == None:
				self.on_checked(event)

	def set_enabled(self, is_enabled):
		self.is_enabled = is_enabled
		if self.is_enabled:
			self.check_box.set_color(Color.BLACK)
			self.fill_box.set_color(Color.BLACK)
		else:
			self.check_box.set_color(Color.GREY)
			self.fill_box.set_color(Color.GREY)

	def set_visibility(self, is_visible):
		self.is_visible = is_visible
		self.lbl_text.set_visibility(is_visible)
		self.check_box.set_visibility(is_visible)
		self.fill_box.set_visibility(is_visible)

	def draw(self, surface):
		self.check_box.draw(surface)
		if self.is_checked:
			self.fill_box.draw(surface)
		self.lbl_text.draw(surface)
		super().draw(surface)

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