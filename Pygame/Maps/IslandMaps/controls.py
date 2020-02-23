#controls.py
import go, imp, events
from structs import *

class Control:
	def __init__(self, left_top, size, is_visible=True, is_enabled=True, enabled_color=Color.ALICE_BLUE, disabled_color=Color.LIGHT_GREY):
		self.enabled_color = enabled_color
		self.disabled_color = disabled_color
		self.set_enabled(is_enabled)
		self.set_visibility(is_visible)
		self.set_size(size)
		self.set_position(left_top)

	def set_size(self, size):
		self.w, self.h = self.size = size 

	def set_position(self, left_top):
		self.left, self.top = self.left_top = left_top
		self.right, self.bottom = self.right_bottom = self.left + self.w, self.top + self.h 
		self.x, self.y = self.center = self.left + self.w // 2, self.top + self.h // 2

	def set_visibility(self, is_visible):
		self.is_visible = is_visible

	def set_enabled(self, is_enabled):
		self.is_enabled = is_enabled

	def center_on(self, pos):
		x, y = pos 
		self.set_position((x - self.w // 2, y - self.h // 2))

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
		self.margin_w, self.margin_h = (8, 8)
		self.is_active = False
		self.on_click = on_click
		self.active_color = active_color
		self.text_color = text_color
		self.disabled_text_color = Color.DIM_GREY
		self.mw, self.mh = self.min_size = min_size
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
		fixed_size = (w + self.margin_w, h + self.margin_h)
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
		if self.mw > 0:
			w = self.mw 
		if self.mh > 0:
			h = self.mh
		return (w, h)

	def draw(self, surface):
		if self.is_visible:
			self.btn_bck.set_color(self.get_color())
			self.btn_txt.set_color(self.get_text_color())
			self.btn_bck.draw(surface)
			self.btn_txt.draw(surface)

class SidBar (Control):
	def __init__(self, left_top, controls=[]):
		super().__init__(left_top, (0, 0))


# class SideBar (Control):
# 	def __init__(self, left_top, window_size, window_side, controls=[], color=Color.SEA_GREEN):
# 		self.color = color 
# 		self.is_showing = True
# 		self.window_side = window_side 
# 		self.window_width, self.window_height = self.window_size = window_size
# 		self.rect = go.Rect((0, 0), (0, 0), color=self.color)
# 		self.create_button(controls)
# 		self.set_btn_text()
# 		super().__init__((0, 0), controls=controls, default_size=self.btn_show.size, window_or=self.get_windows_or())
# 		self.wire_events()

# 	def create_button(self, controls):
# 		self.btn_show = Button('', on_click=self.on_click_toggle_bar)
# 		controls.insert(0, self.btn_show)

# 	def assay_size(self):
# 		super().assay_size()
# 		self.rect.set_size(self.size)

# 	def set_position(self, left_top):
# 		super().set_position(left_top)
# 		left, top = left_top
# 		w, h = self.btn_show.size 
# 		button_center = (left + self.w - w // 2, top + h // 2)
# 		if self.window_side == WindowSide.RIGHT:
# 			left, top = (left + self.window_width - self.w, top)
# 			button_center = (left + w // 2, top + h // 2)
# 		elif self.window_side == WindowSide.TOP:
# 			button_center = (left + w // 2, top + self.h - h // 2 - 2)
# 		elif self.window_side == WindowSide.BOTTOM:
# 			left, top = (left, top + self.window_height - self.h)
# 			button_center = (left + w // 2, top + h // 2)
# 		self.rect.set_position((left, top))
# 		self.btn_show.center_on(button_center)

# 	def set_default(self, size, is_override=False):
# 		w, h = size 
# 		new_size = None
# 		if self.window_side in [WindowSide.LEFT, WindowSide.RIGHT]:
# 			new_size = (w - self.mw, h)
# 		elif self.window_side in [WindowSide.TOP, WindowSide.BOTTOM]:
# 			new_size = (w, h - self.mh)
# 		super().set_default(new_size, is_override)

# 	def set_window_side(self, window_side):
# 		self.window_side = window_side
# 		self.set_btn_text()
# 		self.set_window_or(self.get_windows_or(), (0, 0))

# 	def get_windows_or(self):
# 		if self.window_side in [WindowSide.LEFT, WindowSide.RIGHT]:
# 			return WindowOr.VERTICAL
# 		else:
# 			return WindowOr.HORIZONTAL
		
# 	def wire_events(self):
# 		imp.IMP().add_listener(events.WindowResizedEvent().listen(self.on_resize))
# 		imp.IMP().add_listener(events.UserEvent(CustomEvent.REFRESH_SIDEBAR).listen(self.on_refresh_sidebar))

# 	def on_resize(self, event):
# 		self.window_width, self.window_height = self.window_size = (event.w, event.h)
# 		self.assay_size()
# 		self.set_position((0, 0))

# 	def on_refresh_sidebar(self, event):
# 		self.assay_size()
# 		self.set_position((0, 0))

# 	def on_click_toggle_bar(self, event):
# 		self.toggle_bar()

# 	def toggle_bar(self):
# 		self.is_showing = not self.is_showing
# 		self.set_btn_text()
# 		if self.is_showing:
# 			self.set_override(False)
# 			self.show_buttons()
# 		else:
# 			self.set_override(True)
# 			self.show_buttons(is_show=False)	
# 		self.assay_size()
# 		self.set_position((0, 0))

# 	def set_btn_text(self):
# 		left_btn_text = '<<<'
# 		right_btn_text = '>>>'
# 		top_btn_text = '/\\'
# 		bottom_btn_text = '\\/'
# 		if not self.is_showing:
# 			left_btn_text, right_btn_text = right_btn_text, left_btn_text
# 			top_btn_text, bottom_btn_text = bottom_btn_text, top_btn_text
# 		if self.window_side == WindowSide.LEFT:
# 			self.btn_show.set_text(left_btn_text)
# 		elif self.window_side == WindowSide.RIGHT:
# 			self.btn_show.set_text(right_btn_text)
# 		elif self.window_side == WindowSide.TOP:
# 			self.btn_show.set_text(top_btn_text)
# 		else: #self.window_side == WindowSide.BOTTOM:
# 			self.btn_show.set_text(bottom_btn_text)

# 	def show_buttons(self, is_show=True):
# 		for btn in self.children:
# 			btn.set_visibility(is_show)
# 		self.btn_show.set_visibility(True)

# 	def enable_buttons(self, is_enabled=True):
# 		for btn in self.children:
# 			btn.set_enabled(is_enabled)
# 		self.btn_show.set_enabled(True)

# 	def get_w(self):
# 		if self.window_side in [WindowSide.LEFT, WindowSide.RIGHT]:
# 			return super().get_w()
# 		return self.window_width

# 	def get_h(self):
# 		if self.window_side in [WindowSide.TOP, WindowSide.BOTTOM]:
# 			return super().get_h()
# 		return self.window_height

# 	def update(self):
# 		self.rect.update()
# 		super().update()

# 	def draw(self, surface):
# 		self.rect.draw(surface)
# 		super().draw(surface)


# class Control:
# 	def __init__(self, left_top, controls=[], window_or=WindowOr.VERTICAL, default_size=(20, 20), is_override=False):
# 		self.mw, self.mh = self.margin = (8, 8)
# 		self.window_or = window_or
# 		self.children = controls
# 		self.set_default(default_size, is_override)
# 		self.assay_size()
# 		self.set_position(left_top)

# 	def assay_size(self):
# 		self.w, self.h = self.size =  self.get_w(), self.get_h()
# 		print('w: {}, h: {}, size: {}'.format(self.w, self.h, self.size))

# 	def set_position(self, left_top):
# 		self.left, self.top = self.left_top = left_top
# 		self.right, self.bottom = self.right_bottom = self.left + self.w, self.top + self.h 
# 		self.x, self.y = self.center = self.left + self.w // 2, self.top + self.h // 2
# 		self.position_children()

# 	def center_on(self, center):
# 		self.x, self.y = self.center = center 
# 		self.left, self.top = self.left_top = self.x - self.w // 2, self.y - self.h // 2
# 		self.right, self.bottom = self.right_bottom = self.left + self.w // 2, self.top + self.h // 2
# 		self.position_children() 

# 	def set_window_or(self, window_or, left_top):
# 		self.window_or = window_or
# 		self.assay_size()

# 	def set_default(self, default_size, is_override=False):
# 		self.set_override(is_override)
# 		self.default_w, self.default_h = self.default_size = default_size

# 	def set_override(self, is_override):
# 		self.is_override = is_override

# 	def position_children(self):
# 		if self.window_or == WindowOr.VERTICAL:
# 			x = self.x
# 			y = self.top 
# 			for child in self.children:
# 				child.center_on((x, y + child.h // 2))
# 				y += child.h + self.mh
# 		else:
# 			x = self.left
# 			y = self.top
# 			for child in self.children:
# 				child.center_on((x + child.w // 2, y + 3 * child.h // 4))
# 				x += child.w + self.mw

# 	def get_w(self):
# 		if self.is_override or not any(self.children):
# 			return self.default_w + self.mw
# 		if self.window_or == WindowOr.VERTICAL:
# 			return self.get_max_width()	
# 		return self.get_total_width()

# 	def get_max_width(self):
# 		max_width = 0
# 		for child in self.children:
# 			width = child.w
# 			if width > max_width:
# 				max_width = width 
# 		return max_width + self.mw

# 	def get_total_width(self):
# 		total_width = 0
# 		for child in self.children:
# 			total_width += child.w
# 		return total_width + self.mw

# 	def get_h(self):
# 		if self.is_override or not any(self.children):
# 			return self.default_h + self.mh
# 		if self.window_or == WindowOr.VERTICAL:
# 			return self.get_total_height()
# 		return self.get_max_height()

# 	def get_max_height(self):
# 		max_height = 0
# 		for child in self.children:
# 			height = child.h
# 			if height > max_height:
# 				max_height = height
# 		return max_height + self.mh

# 	def get_total_height(self):
# 		total_height = 0
# 		for child in self.children:
# 			total_height += child.h
# 		return total_height + self.mh

# 	def update(self):
# 		for child in self.children:
# 			child.update()

# 	def draw(self, surface):
# 		for control in self.children:
# 			control.draw(surface)

# class BlankControl (Control):
# 	def __init__(self, left_top, size):
# 		super().__init__(default_size=size)
# 		self.set_position(left_top)

if __name__=='__main__':
	import pygame
	import unit_test

	test = unit_test.UnitTest()
	btn = Button('Hello World!', on_click=(lambda event : print('OnClick!!!')))
	btn.center_on(tuple(x // 2 for x in unit_test.WINDOW_SIZE))

	def toggle_enabled(event):
		btn.set_enabled(not btn.is_enabled)

	def toggle_visibility(event):
		btn.set_visibility(not btn.is_visible)

	imp.IMP().add_listener(events.KeyDownEvent(pygame.K_e).listen(toggle_enabled))
	imp.IMP().add_listener(events.KeyDownEvent(pygame.K_v).listen(toggle_visibility))

	test.register([btn])
	test.run()
