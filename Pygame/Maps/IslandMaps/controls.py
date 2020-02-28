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
		self.btn_bck = go.BorderedRect((0, 0), (0, 0))
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
		events.UserEvent(CustomEvent.REFRESH_UI).post(sender=self)

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

class CheckBox (Control):
	def __init__(self, lbl_str, on_checked=None, left_top=(0, 0)):
		super().__init__()
		self.is_active = False
		self.is_checked = False
		self.on_checked = on_checked
		self.font_style = self.get_style('default_text')
		self.lbl_text = go.RenderText(lbl_str, self.font_style)
		self.check_box = go.BorderedRect(left_top, (10, 10))
		self.fill_box = go.Rect(left_top, (10, 10))
		self.set_size(tuple(x + 10 for x in self.lbl_text.size))
		self.set_position(left_top)
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_listener(events.MouseLeftButtonDownEvent().create(self.on_mouse_left_button_down))
		imp.IMP().add_listener(events.MouseMotionEvent().create(self.on_mouse_motion, quell=True))

	def on_mouse_left_button_down(self, event):
		if self.is_enabled and self.is_active:			
			self.checked(event)

	def on_mouse_motion(self, event):
		if self.check_box.is_within(event.pos):
			self.is_active = True
		else:
			self.is_active = False

	def set_position(self, left_top):
		super().set_position(left_top)
		self.check_box.set_position(left_top)
		self.fill_box.set_position(left_top)
		self.lbl_text.set_position((self.left + 12, self.top))
		self.lbl_text.center_on((self.lbl_text.x, self.check_box.y))

	def set_text(self, text):
		self.lbl_text.set_text(text)
		self.set_size(tuple(x + 10 for x in self.lbl_text.size))
		events.UserEvent(CustomEvent.REFRESH_UI).post(sender=self)

	def set_onchecked(self, method):
		self.on_checked = method 

	def get_checkbox_style(self):
		if self.is_enabled and self.is_active:
			return imp.IMP().styles.try_get('btn_active', style.Style())
		return super().get_style('default')

	def checked(self, event):
		if self.is_enabled and self.is_visible:
			self.is_checked = not self.is_checked
			if not self.on_checked == None:
				self.on_checked(event)

	def draw(self, surface):
		if self.is_visible:
			self.check_box.draw(surface, self.get_checkbox_style().color)
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
		self.box = go.BorderedRect(left_top, (0, 0))
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
		self.stop()
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
		self.box = go.BorderedRect(left_top, (0, 0))
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

	def set_counter(self, n):
		self.counter = n

	def get_display_str(self):
		format_str = '{:0' + str(self.digits) + '}'
		return format_str.format(self.counter)

	def post_refresh(self):
		events.UserEvent(CustomEvent.REFRESH_UI).post(sender=self)

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
			self.post_refresh()
		elif self.counter > 0 and self.counter < self.div // 10:
			self.post_update = True
			self.post_refresh()
			self.div //= 10
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

class Ruler (Control):
	def __init__(self, left_top, size):
		super().__init__(left_top, size)
		self.lines = []
		self.generate()

	def set_position(self, left_top):
		super().set_position(left_top)
		if len(self.lines) == 5:
			self.lines[0].set_position((self.left, self.top))
			self.lines[1].set_position((self.left + self.w // 4, self.top))
			self.lines[2].set_position((self.x, self.top))
			self.lines[3].set_position((self.x + self.w // 4, self.top))
			self.lines[4].set_position((self.right - 1, self.top))

	def generate(self):
		self.lines.append(go.VerticalLine((self.left, self.top), 2 * self.h))
		self.lines.append(go.VerticalLine((self.left + self.w // 4, self.top), self.h + self.h // 2))
		self.lines.append(go.VerticalLine((self.x, self.top), 2 * self.h))
		self.lines.append(go.VerticalLine((self.x + self.w // 4, self.top), self.h + self.h // 2))
		self.lines.append(go.VerticalLine((self.right - 1, self.top), 2 * self.h))

	def draw(self, surface):
		color = self.get_style('default_border').color 
		for line in self.lines:
			line.draw(surface, color)

class Slider (Control):
	def __init__(self, slider_width=8, length=100, left_top=(0, 0)):
		super().__init__()
		self.ruler = None
		self.tick_value = 0
		self.length = length
		self.fixed_height = 6
		self.is_dragging = False	
		self.slider_width = slider_width
		self.sw, self.sh = self.slider_size = (slider_width, 2 * self.fixed_height + 10)	
		self.bar = go.BorderedRect((0, 0), (length, self.fixed_height))
		self.slider = go.BorderedRect((0, 0), self.slider_size)
		self.set_size((length, self.sh))
		self.set_position(left_top)
		self.tick_length = (self.bar.right - self.bar.left) / 100
		self.ruler = Ruler(self.bar.left_top, self.bar.size)
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
				x = self.bar.left
			if x + self.slider.w // 2 > self.bar.right:
				x = self.bar.right
			self.slider.set_position((x - self.slider.w // 2, self.bar.y - self.h // 2))
			self.post_tick_event()

	def post_tick_event(self):
		self.tick_value = self.slider.x - self.bar.left
		events.UserEvent(CustomEvent.SLIDER_TICK).post(value=round(self.tick_value / self.tick_length))

	def set_position(self, left_top):
		super().set_position(left_top)
		slider_x = self.tick_value + self.left
		self.bar.set_position((self.left, self.y - self.bar.h // 2))
		self.slider.set_position((slider_x - self.slider.w // 2, self.bar.y - self.h // 2))	
		if not self.ruler == None:
			self.ruler.set_position(self.bar.left_top)

	def draw(self, surface):
		color = self.get_style('default').color
		if self.is_visible:
			self.bar.draw(surface, color)
			self.ruler.draw(surface)
			self.slider.draw(surface, color)
			
if __name__=='__main__':
	import pygame
	import unit_test as ut

	unit_test = ut.UnitTest()
	w, h = ut.WINDOW_SIZE

	btn_enable = Button('DISABLE')
	chk_box = CheckBox('IS CHECKED', on_checked=lambda event: print('OnChecked'))
	counter_box = CounterBox(2, can_grow=True)
	btn_inc = Button('INCREMENT', lambda event : counter_box.increment(5))
	stop_watch = StopWatch()
	btn_start = Button('START')
	btn_reset = Button('RESET')
	slider_value = CounterBox(2, can_grow=True)
	slider = Slider()

	controls = []
	controls.append(btn_enable)
	controls.append(chk_box)
	controls.append(slider_value)
	controls.append(slider)
	controls.append(counter_box)
	controls.append(btn_inc)
	controls.append(stop_watch)
	controls.append(btn_start)
	controls.append(btn_reset)
	
	def position_controls(event):
		total_height = -10
		for control in controls:
			total_height += control.h + 10

		left, top = (w // 2, h // 2 - total_height // 2)
		for control in controls:
			control.center_on((left, top))
			top += control.h + 10
	position_controls(None)

	def toggle_enable(event):		
		chk_box.set_enabled(not chk_box.is_enabled)
		slider_value.set_enabled(not slider_value.is_enabled)
		slider.set_enabled(not slider.is_enabled)
		counter_box.set_enabled(not counter_box.is_enabled)
		btn_inc.set_enabled(not btn_inc.is_enabled)
		stop_watch.set_enabled(not stop_watch.is_enabled)
		btn_start.set_enabled(not btn_start.is_enabled)
		btn_reset.set_enabled(not btn_reset.is_enabled)
		btn_enable.set_text('ENABLE' if not chk_box.is_enabled else 'DISABLE')
	btn_enable.on_click = toggle_enable

	def reset(event):
		if stop_watch.is_running:
			btn_start.set_text('START')
		stop_watch.reset()
	btn_reset.on_click = reset

	def start_stop(event):
		if stop_watch.is_running:
			btn_start.set_text('START')
			stop_watch.stop()
		else:
			btn_start.set_text('STOP')
			stop_watch.start()
	btn_start.on_click = start_stop

	imp.IMP().add_listener(events.UserEvent(CustomEvent.SLIDER_TICK).create(lambda event : slider_value.set_counter(event.value)))
	imp.IMP().add_listener(events.UserEvent(CustomEvent.REFRESH_UI).create(position_controls))

	unit_test.register(controls)
	unit_test.run()
