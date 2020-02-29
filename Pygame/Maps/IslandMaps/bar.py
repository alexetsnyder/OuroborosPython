#bar.py
import go, imp, events
from controls import Button, Control
from structs import *

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

	def wire_events(self):
		imp.IMP().add_listener(events.UserEvent(CustomEvent.REFRESH_UI).create(self.on_refresh_sidebar))
		imp.IMP().add_listener(events.WindowResizedEvent().create(self.on_resize))

	def on_resize(self, event):
		self.on_refresh_sidebar(event)

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


if __name__=='__main__':
	import pygame
	import controls as c
	import unit_test as ut

	unit_test = ut.UnitTest(debug=False)

	btn_left = c.Button('LEFT')
	btn_right = c.Button('RIGHT')
	btn_top = c.Button('TOP')
	btn_bottom = c.Button('BOTTOM')
	stop_watch = c.StopWatch()
	btn_start = c.Button('START')
	btn_reset = c.Button('RESET')
	slider_value = c.CounterBox(2, can_grow=True)
	slider = c.Slider()

	controls = []
	controls.append(btn_left)
	controls.append(btn_right)
	controls.append(btn_top)
	controls.append(btn_bottom)
	controls.append(slider_value)
	controls.append(slider)
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
	imp.IMP().add_listener(events.KeyDownEvent(pygame.K_s).create(lambda event : sidebar.set_enabled(not sidebar.is_enabled)))

	unit_test.register([sidebar])
	unit_test.run()