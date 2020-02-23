#controls.py
import go, imp, events
from structs import *

class Control (go.Rect):
	def __init__(self, left_top, size, is_visible=True, is_enabled=True, enabled_color=Color.ALICE_BLUE, disabled_color=Color.LIGHT_GREY):
		self.mw, self.mh = self.margins = (8, 8)
		self.enabled_color = enabled_color
		self.disabled_color = disabled_color
		self.set_enabled(is_enabled)
		self.set_visibility(is_visible)
		super().__init__(left_top, size)
		self.set_size(size)
		self.set_position(left_top)

	def set_visibility(self, is_visible):
		self.is_visible = is_visible

	def set_enabled(self, is_enabled):
		self.is_enabled = is_enabled

	def get_color(self):
		if self.is_enabled:
			return self.enabled_color
		else:
			return self.disabled_color

	def update(self):
		pass

	def draw(self, surface):
		pass

class Button (Control):
	def __init__(self, text, on_click=None, left_top=(0, 0), min_size=(0, 0), text_color=Color.BLACK, text_size=10, active_color=Color.RED, is_visible=True, is_enabled=True):
		self.is_active = False
		self.on_click = on_click
		self.active_color = active_color
		self.text_color = text_color
		self.disabled_text_color = Color.DIM_GREY
		self.min_w, self.min_h = self.min_size = min_size
		self.btn_font = go.FontInfo(font_size=text_size, font_color=text_color)
		self.btn_txt = go.RenderText(text, self.btn_font)
		self.btn_bck = go.Rect((0, 0), (0, 0))
		self.wire_events()
		super().__init__(left_top, self.get_size(), is_enabled=is_enabled, is_visible=is_visible)

	def wire_events(self):
		imp.IMP().add_listener(events.MouseMotionEvent().listen(self.on_mouse_motion, quell=True))
		imp.IMP().add_listener(events.MouseLeftButtonDownEvent().listen(self.on_mouse_left_button_down))

	def on_mouse_motion(self, event):
		if self.btn_bck.is_within(event.pos):
			self.is_active = True
		else:
			self.is_active = False

	def on_mouse_left_button_down(self, event):
		if not self.on_click == None:
			if self.is_enabled and self.is_active:
				self.on_click(event)

	def get_color(self):
		color = super().get_color()
		if self.is_enabled and self.is_active:
			color = self.active_color
		return color 

	def get_text_color(self):
		if self.is_enabled:
			return self.text_color
		else:
			return self.disabled_text_color

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

	def get_size(self):
		w, h = self.btn_txt.size 
		if self.min_w > 0:
			w = self.min_w 
		if self.min_h > 0:
			h = self.min_h
		return (w, h)

	def draw(self, surface):
		if self.is_visible:
			self.btn_bck.set_color(self.get_color())
			self.btn_txt.set_color(self.get_text_color())
			self.btn_bck.draw(surface)
			self.btn_txt.draw(surface)

class SideBar (Control):
	def __init__(self, controls=[], window_side=WindowSide.LEFT):	
		self.is_expanded = True
		self.controls = controls 
		self.window_side = window_side
		self.sidebar_bck = go.Rect((0, 0), (0, 0), color=Color.SEA_GREEN)
		self.btn_expand = Button(self.get_btn_txt(), on_click=self.toggle_expand)
		self.min_w, self.min_h = self.min_size = self.btn_expand.size 
		super().__init__((0, 0), (0, 0), enabled_color=Color.SEA_GREEN)
		self.set_size(self.assay_size())
		self.set_position(self.assay_position())

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

	def draw(self, surface):
		if self.is_visible:
			self.sidebar_bck.draw(surface)
			self.btn_expand.draw(surface)
			for control in self.controls:
				control.draw(surface)

class CheckBox (Control):
	def __init__(self, lbl_str, left_top=(0, 0), on_checked=None, color=Color.TEAL_FELT, checked_color=Color.BLACK):
		self.is_checked = False
		self.checked_color = checked_color
		self.on_checked = on_checked
		self.font_info = go.FontInfo(font_size=10, font_color=Color.BLACK)
		self.lbl_text = go.RenderText(lbl_str, self.font_info)
		self.check_box = go.Rect(left_top, (10, 10), color=color, width=1)
		self.fill_box = go.Rect(left_top, (10, 10), color=checked_color)
		super().__init__(left_top, tuple(x + 10 for x in self.lbl_text.size), enabled_color=color)
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_listener(events.MouseLeftButtonDownEvent().listen(self.on_mouse_left_button_down))

	def set_position(self, left_top):
		super().set_position(left_top)
		self.check_box.set_position(left_top)
		self.fill_box.set_position(left_top)
		self.lbl_text.set_position((self.left + 12, self.top))
		self.lbl_text.center_on((self.lbl_text.x, self.check_box.y))

	def set_text(self, text):
		self.lbl_text.set_text(text)
		self.set_size(tuple(x + 10 for x in self.lbl_text.size))

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
			self.check_box.set_color(self.get_color())
			self.lbl_text.set_color(self.get_color())
			self.check_box.draw(surface)
			if self.is_checked:
				self.fill_box.set_color(self.get_color())
				self.fill_box.draw(surface)
			self.lbl_text.draw(surface)

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

	controls = []
	controls.append(btn_left)
	controls.append(btn_right)
	controls.append(btn_top)
	controls.append(btn_bottom)
	controls.append(btn_enable)
	controls.append(chk_box)
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
	btn_enable.on_click = toggle_enable

	unit_test.register([sidebar])
	unit_test.run()
