#controls.py
import time, math
import go, imp, style, events
from structs import *

class Control (go.Rect):
	def __init__(self, left_top=(0, 0), size=(0, 0), is_visible=True, is_enabled=True):
		super().__init__(left_top, size)
		self.mw, self.mh = self.margins = (8, 8)
		Control.set_enabled(self, is_enabled)
		Control.set_visibility(self, is_visible)

	def set_visibility(self, is_visible):
		self.is_visible = is_visible

	def set_enabled(self, is_enabled):
		self.is_enabled = is_enabled

	def get_style(self, key):
		postfix = ''
		if self.is_enabled:
			postfix = 'enabled'
		else:
			postfix = 'disabled'
		return imp.IMP().styles.try_get('{}_{}'.format(key, postfix), style.Style())

	def update(self):
		pass

	def draw(self, surface):
		pass

class Button (Control):
	def __init__(self, text, on_click=None, left_top=(0, 0), min_size=(0, 0), is_visible=True, is_enabled=True):
		super().__init__(left_top, is_enabled=is_enabled, is_visible=is_visible)
		self.is_active = False
		self.on_click = on_click
		self.min_w, self.min_h = self.min_size = min_size
		self.font_style = self.get_text_style()
		self.btn_txt = go.RenderText(text, self.font_style)
		self.btn_bck = go.Rect((0, 0), (0, 0))
		self.set_size(self.get_size())
		self.set_position(self.left_top)
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_listener(events.MouseMotionEvent().create(self.on_mouse_motion, quell=True))
		imp.IMP().add_listener(events.MouseLeftButtonDownEvent().create(self.on_mouse_left_button_down))

	def on_mouse_motion(self, event):
		if self.btn_bck.is_within(event.pos):
			self.is_active = True
		else:
			self.is_active = False

	def on_mouse_left_button_down(self, event):
		if not self.on_click == None:
			if self.is_enabled and self.is_active:
				self.on_click(event)

	def get_style(self):
		if self.is_enabled and self.is_active:
			return imp.IMP().styles.try_get('btn_active', style.Style())
		return super().get_style('default')

	def get_text_style(self):
		return super().get_style('default_text')

	def set_size(self, size):
		w, h = size
		fixed_size = (w + self.mw, h + self.mh)
		super().set_size(fixed_size)
		self.btn_bck.set_size(fixed_size)

	def set_position(self, left_top):
		super().set_position(left_top)
		self.btn_bck.set_position(self.left_top)
		self.btn_txt.center_on(self.center)

	def set_text(self, btn_txt):
		self.btn_txt.set_text(btn_txt)
		self.set_size(self.get_size())
		events.UserEvent(CustomEvent.REFRESH_SIDEBAR).post()

	def get_size(self):
		w, h = self.btn_txt.size 
		if self.min_w > 0:
			w = self.min_w 
		if self.min_h > 0:
			h = self.min_h
		return (w, h)

	def draw(self, surface):
		if self.is_visible:
			self.btn_bck.draw(surface, self.get_style().color)
			self.btn_txt.draw(surface, self.get_text_style().color)

class SideBar (Control):
	def __init__(self, controls=[], window_side=WindowSide.LEFT):	
		super().__init__()
		self.is_expanded = True
		self.controls = controls 
		self.window_side = window_side
		self.sidebar_bck = go.Rect((0, 0), (0, 0))
		self.btn_expand = Button(self.get_btn_txt(), on_click=self.toggle_expand)
		self.min_w, self.min_h = self.min_size = self.btn_expand.size 	
		self.set_size(self.assay_size())
		self.set_position(self.assay_position())
		self.wire_events()

	def create_styles(self):
		super().create_styles()
		self.styles['default_enabled'].color = Color.SEA_GREEN

	def wire_events(self):
		imp.IMP().add_listener(events.UserEvent(CustomEvent.REFRESH_SIDEBAR).create(self.on_refresh_sidebar))

	def on_refresh_sidebar(self, event):
		self.set_size(self.assay_size())
		self.set_position(self.assay_position())

	def set_enabled(self, is_enabled):
		super().set_enabled(is_enabled)
		self.btn_expand.set_enabled(is_enabled)
		for control in self.controls:
			control.set_enabled(is_enabled)

	def set_btn_txt(self, btn_txt):
		self.btn_expand.set_text(btn_txt)
		self.min_w, self.min_h = self.min_size = self.btn_expand.size 

	def set_window_side(self, window_side):
		self.window_side = window_side
		self.set_btn_txt(self.get_btn_txt())
		self.set_size(self.assay_size())
		self.set_position(self.assay_position())

	def set_size(self, size):
		super().set_size(size)
		self.sidebar_bck.set_size(size)

	def set_position(self, left_top):
		super().set_position(left_top)
		self.btn_expand.set_position(self.get_btn_pos())
		self.sidebar_bck.set_position(left_top)
		self.position_controls()

	def assay_size(self):
		return (self.get_w(), self.get_h())

	def assay_position(self):
		window_w, window_h = imp.IMP().screen.size
		#WindowSide.LEFT and WindowSide.TOP
		left, top = 0, 0
		if self.window_side == WindowSide.RIGHT:
			left = window_w - self.w 
		elif self.window_side == WindowSide.BOTTOM:
			top = window_h - self.h
		return (left, top)

	def get_btn_pos(self):
		if self.window_side == WindowSide.LEFT:
			return (self.right - self.btn_expand.w, self.top)
		elif self.window_side == WindowSide.RIGHT:
			return self.left_top
		elif self.window_side == WindowSide.TOP:
			return (self.left, self.bottom - self.btn_expand.h)
		else: #self.window_side == WindowSide.BOTTOM:
			return self.left_top

	def get_btn_txt(self):
		left_btn_text = '<<<'
		right_btn_text = '>>>'
		top_btn_text = '/\\'
		bottom_btn_text = '\\/'
		if not self.is_expanded:
			left_btn_text, right_btn_text = right_btn_text, left_btn_text
			top_btn_text, bottom_btn_text = bottom_btn_text, top_btn_text
		if self.window_side == WindowSide.LEFT:
			return left_btn_text
		elif self.window_side == WindowSide.RIGHT:
			return right_btn_text
		elif self.window_side == WindowSide.TOP:
			return top_btn_text
		else: #self.window_side == WindowSide.BOTTOM:
			return bottom_btn_text

	def toggle_expand(self, event):
		self.is_expanded = not self.is_expanded
		if self.is_expanded:
			self.show_controls()
		else:
			self.hide_controls()
		self.set_btn_txt(self.get_btn_txt())
		self.set_size(self.assay_size())
		self.set_position(self.assay_position())

	def hide_controls(self):
		for control in self.controls:
			control.set_visibility(False)

	def show_controls(self):
		for control in self.controls:
			control.set_visibility(True)

	def is_horizontal(self):
		return self.window_side in [WindowSide.TOP, WindowSide.BOTTOM]

	def is_vertical(self):
		return self.window_side in [WindowSide.LEFT, WindowSide.RIGHT]

	def position_controls(self):
		if self.is_vertical():
			x = self.x
			y = self.top + self.btn_expand.h + self.mh
			for control in self.controls:
				control.center_on((x, y + control.h // 2))
				y += control.h + self.mh
		else:
			x = self.left + self.btn_expand.w + self.mw 
			y = self.top
			for control in self.controls:
				control.center_on((x + control.w // 2, y + 3 * control.h // 4))
				x += control.w + self.mw

	def get_w(self):
		if not self.is_vertical():
			return imp.IMP().screen.w
		if not self.is_expanded or not any(self.controls):
			return self.min_w
		return self.get_max_width()	

	def get_max_width(self):
		max_width = 0
		for control in self.controls:
			width = control.w
			if width > max_width:
				max_width = width 
		return max_width + self.mw

	def get_h(self):
		if not self.is_horizontal():
			return imp.IMP().screen.h
		if not self.is_expanded or not any(self.controls):
			return self.min_h
		return self.get_max_height()

	def get_max_height(self):
		max_height = 0
		for control in self.controls:
			height = control.h
			if height > max_height:
				max_height = height
		return max_height + self.mh

	def update(self):
		for control in self.controls:
			control.update()

	def draw(self, surface):
		if self.is_visible:
			self.sidebar_bck.draw(surface, self.get_style('sidebar').color)
			self.btn_expand.draw(surface)
			for control in self.controls:
				control.draw(surface)

class CheckBox (Control):
	def __init__(self, lbl_str, on_checked=None, left_top=(0, 0)):
		super().__init__()
		self.is_checked = False
		self.on_checked = on_checked
		self.font_style = self.get_style('default_text')
		self.lbl_text = go.RenderText(lbl_str, self.font_style)
		self.check_box = go.Rect(left_top, (10, 10), width=1)
		self.fill_box = go.Rect(left_top, (10, 10))
		self.set_size(tuple(x + 10 for x in self.lbl_text.size))
		self.set_position(left_top)
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_listener(events.MouseLeftButtonDownEvent().create(self.on_mouse_left_button_down))

	def set_position(self, left_top):
		super().set_position(left_top)
		self.check_box.set_position(left_top)
		self.fill_box.set_position(left_top)
		self.lbl_text.set_position((self.left + 12, self.top))
		self.lbl_text.center_on((self.lbl_text.x, self.check_box.y))

	def set_text(self, text):
		self.lbl_text.set_text(text)
		self.set_size(tuple(x + 10 for x in self.lbl_text.size))
		events.UserEvent(CustomEvent.REFRESH_SIDEBAR).post()

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

	def draw(self, surface):
		if self.is_visible:
			self.check_box.draw(surface, self.get_style('default').color)
			if self.is_checked:
				self.fill_box.draw(surface, self.get_style('check_mark').color)
			self.lbl_text.draw(surface, self.get_style('default_text').color)

class StopWatch (Control):
	def __init__(self, left_top=(0, 0), digit_color=Color.RED):
		super().__init__()
		self.time = 0
		self.prv_time = 0
		self.padding = 4
		self.is_running = False
		self.font_style = self.get_style('digit_text')
		self.seperator_txt = go.RenderText(':', self.font_style)
		self.seconds_txt = go.RenderText(self.display_format(0), self.font_style)
		self.minutes_txt = go.RenderText(self.display_format(0), self.font_style)
		self.hours_txt = go.RenderText(self.display_format(0), self.font_style)
		self.box = go.Rect(left_top, (0, 0))
		self.set_size(self.get_clock_size())
		self.set_position(left_top)

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
		left = self.left + self.padding
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
		return (clock_width, self.seconds_txt.h + self.padding + 2)

	def get_time(self):
		r_time = math.ceil(self.time)
		return ((r_time//60//60), (r_time//60)%60, r_time%60)

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
		self.set_position(self.left_top)

	def draw_clock(self, surface):
		digit_color = self.get_style('digit_text').color
		left = self.left
		self.hours_txt.draw(surface, digit_color)
		left += self.hours_txt.w + self.padding
		self.seperator_txt.draw_at(surface, digit_color, (left + 2, self.top + self.h // 4))
		left += self.seperator_txt.w + self.padding // 2
		self.minutes_txt.draw(surface, digit_color)
		left += self.minutes_txt.w + 2
		self.seperator_txt.draw_at(surface, digit_color, (left + 2, self.top + self.h // 4))
		self.seconds_txt.draw(surface, digit_color)

	def draw(self, surface):
		if self.is_visible:
			self.box.draw(surface, self.get_style('clockback').color)
			self.draw_clock(surface)

class CounterBox (Control):
	def __init__(self, digits, can_grow=False, limit=100, left_top=(0, 0)):
		super().__init__()
		self.limit = limit
		self.can_grow = can_grow
		self.digits = digits
		self.post_update = False
		self.div = 10 * int('{}{}'.format(1, ''.join(['0' for i in range(self.digits-1)])))
		self.counter = 0
		self.padding = 10
		self.box = go.Rect(left_top, (0, 0))
		self.font_style = self.get_style('digit_text')
		self.display_text = go.RenderText(self.get_display_str(), font_style=self.font_style)
		self.set_size(tuple(x + self.padding for x in self.display_text.size))
		self.set_position(left_top)

	def set_size(self, size):
		super().set_size(size)
		self.box.set_size(size)

	def set_position(self, left_top):
		super().set_position(left_top)
		self.box.set_position(self.left_top)
		self.display_text.center_on(self.center)

	def get_display_str(self):
		format_str = '{:0' + str(self.digits) + '}'
		return format_str.format(self.counter)

	def post_sidebar_refresh(self):
		events.UserEvent(CustomEvent.REFRESH_SIDEBAR).post()

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
			self.set_position(self.left_top)
			self.post_update = False

	def draw(self, surface):
		if self.is_visible:
			self.box.draw(surface, self.get_style('clockback').color)
			self.display_text.draw(surface, self.get_style('digit_text').color)

class Slider (Control):
	def __init__(self, length=80, measure=10, left_top=(0, 0)):
		super().__init__()
		self.is_dragging = False
		self.fixed_height = 5
		self.sw, self.sh = self.slider_size = (10, 4 * self.fixed_height)
		self.length = length
		self.measure = measure
		self.bar = go.Rect((0, 0), (length, self.fixed_height))
		self.slider_border = go.Rect((0, 0), tuple(x + 2 for x in self.slider_size), width=1)
		self.slider = go.Rect((0, 0), self.slider_size)
		self.set_size((length, self.sh))
		self.set_position(left_top)
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_listener(events.MouseLeftButtonDownEvent().create(self.on_mouse_left_button_down))
		imp.IMP().add_listener(events.MouseLeftButtonUpEvent().create(self.on_mouse_left_button_up))
		imp.IMP().add_listener(events.MouseMotionEvent().create(self.on_mouse_motion, quell=True))

	def on_mouse_left_button_down(self, event):
		if self.slider.is_within(event.pos):
			self.is_dragging = True

	def on_mouse_left_button_up(self, event):
		self.is_dragging = False

	def on_mouse_motion(self, event):
		if self.is_enabled and self.is_dragging:
			x, y = event.pos 
			if x - self.slider.w // 2 < self.bar.left:
				x = self.bar.left + self.slider.w // 2
			if x + self.slider.w // 2 > self.bar.right:
				x = self.bar.right - self.slider.w // 2
			self.slider_border.center_on((x, self.slider_border.y))
			self.slider.center_on((x, self.slider_border.y))

	def set_position(self, left_top):
		super().set_position(left_top)
		self.bar.set_position(left_top)
		self.slider_border.center_on((self.left + self.slider.w // 2, self.bar.y)) 
		self.slider.center_on((self.left + self.slider.w // 2, self.bar.y))

	def draw(self, surface):
		color = self.get_style('default').color
		if self.is_visible:
			self.bar.draw(surface, color)
			self.slider_border.draw(surface, self.get_style('default_border').color)
			self.slider.draw(surface, color)
			
if __name__=='__main__':
	import pygame
	import unit_test as ut

	unit_test = ut.UnitTest()

	btn_left = Button('LEFT')
	btn_right = Button('RIGHT')
	btn_top = Button('TOP')
	btn_bottom = Button('BOTTOM')
	btn_enable = Button('DISABLE')
	chk_box = CheckBox('IS CHECKED', on_checked=lambda event: print('OnChecked'))
	counter_box = CounterBox(2, can_grow=True)
	btn_inc = Button('INCREMENT', lambda event : counter_box.increment(5))
	stop_watch = StopWatch()
	btn_start = Button('START')
	btn_reset = Button('RESET', lambda event : stop_watch.reset())
	slider = Slider()

	controls = []
	controls.append(btn_left)
	controls.append(btn_right)
	controls.append(btn_top)
	controls.append(btn_bottom)
	controls.append(btn_enable)
	controls.append(chk_box)
	controls.append(slider)
	controls.append(counter_box)
	controls.append(btn_inc)
	controls.append(stop_watch)
	controls.append(btn_start)
	controls.append(btn_reset)
	sidebar = SideBar(controls, WindowSide.LEFT)

	def set_left(event):
		sidebar.set_window_side(WindowSide.LEFT)
	btn_left.on_click = set_left

	def set_right(event):
		sidebar.set_window_side(WindowSide.RIGHT)
	btn_right.on_click = set_right

	def set_top(event):
		sidebar.set_window_side(WindowSide.TOP)
	btn_top.on_click = set_top

	def set_bottom(event):
		sidebar.set_window_side(WindowSide.BOTTOM)
	btn_bottom.on_click = set_bottom

	def toggle_enable(event):
		btn_left.set_enabled(not btn_left.is_enabled)
		btn_right.set_enabled(not btn_right.is_enabled)
		btn_top.set_enabled(not btn_top.is_enabled)
		btn_bottom.set_enabled(not btn_bottom.is_enabled)
		btn_enable.set_text('ENABLE' if not btn_left.is_enabled else 'DISABLE')
		chk_box.set_enabled(not chk_box.is_enabled)
		slider.set_enabled(not slider.is_enabled)
		counter_box.set_enabled(not counter_box.is_enabled)
		btn_inc.set_enabled(not btn_inc.is_enabled)
		stop_watch.set_enabled(not stop_watch.is_enabled)
		btn_start.set_enabled(not btn_start.is_enabled)
		btn_reset.set_enabled(not btn_reset.is_enabled)
	btn_enable.on_click = toggle_enable

	def start_stop(event):
		if stop_watch.is_running:
			btn_start.set_text('START')
			stop_watch.stop()
		else:
			btn_start.set_text('STOP')
			stop_watch.start()
	btn_start.on_click = start_stop

	imp.IMP().add_listener(events.KeyDownEvent(pygame.K_s).create(lambda event : sidebar.set_enabled(not sidebar.is_enabled)))

	unit_test.register([sidebar])
	unit_test.run()
