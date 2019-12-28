#controls.py
import go, imp, events
from geo import plottable
from structs import *

@plottable
class Control:
	def __init__(self, left_top, controls=[], window_or=WindowOr.VERTICAL, default_size=(20, 20), is_override=False):
		self.mw, self.mh = self.margin = (8, 8)
		self.window_or = window_or
		self.children = controls
		self.set_default(default_size, is_override)
		self.set_size(self.assay_size())
		self.set_position(left_top)

	def set_size(self, size):
		pass

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

	def draw(self, surface):
		for control in self.children:
			control.draw(surface)

class BlankControl (Control):
	def __init__(self, left_top, size):
		super().__init__(left_top, default_size=size)

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
		super().__init__((0, 0), controls=controls, default_size=self.btn_show.size, window_or=self.get_windows_or())
		self.wire_events()

	def set_size(self, size):
		super().set_size(size)
		self.rect.set_size(size)

	def set_position(self, left_top):
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
		super().set_position((left, top))
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
		imp.IMP().add_delegate(events.WindowResizedEvent().listen(self.on_resize))

	def on_resize(self, event):
		self.window_width, self.window_height = self.window_size = (event.w, event.h)
		self.set_size(self.assay_size())

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
		super().__init__(left_top, default_size=self.btn_text.size)
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_delegate(events.MouseMotionEvent().listen(self.on_mouse_motion, quell=True))
		imp.IMP().add_delegate(events.MouseLeftButtonDownEvent().listen(self.on_mouse_left_button_down))

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

#Grey out checkbox when disabled.
class CheckBox (Control):
	def __init__(self, lbl_str, left_top=(0, 0), on_checked=None, is_checked=False, color=Color.BLACK, checked_color=Color.BLACK):
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
		super().__init__(left_top, default_size=tuple(x + 10 for x in self.lbl_text.size))
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_delegate(events.MouseLeftButtonDownEvent().listen(self.on_mouse_left_button_down))

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

if __name__=='__main__':
	import pygame
	pygame.init()

	def print_hello(event):
		print('Hello World!')

	imp.IMP().event_dispatcher = events.EventDispatcher()
	buttons = []
	buttons.append(Button('Left'))
	buttons.append(Button('Right'))
	buttons.append(Button('Top'))
	buttons.append(Button('Bottom'))
	buttons.append(Button('(Dis/En)able'))
	buttons.append(CheckBox('Checked', on_checked=print_hello))
	side_bar = SideBar((600, 400), WindowSide.LEFT, controls=buttons)

	def on_left_click(event):
		side_bar.set_window_side(WindowSide.LEFT)

	def on_right_click(event):
		side_bar.set_window_side(WindowSide.RIGHT)

	def on_top_click(event):
		side_bar.set_window_side(WindowSide.TOP)

	def on_bottom_click(event):
		side_bar.set_window_side(WindowSide.BOTTOM)

	def toggle_buttons_enabled(event):
		buttons_enabled = not buttons[1].is_enabled
		buttons[1].set_enabled(buttons_enabled)
		buttons[2].set_enabled(buttons_enabled)
		buttons[3].set_enabled(buttons_enabled)
		buttons[4].set_enabled(buttons_enabled)
		buttons[6].set_enabled(buttons_enabled)

	buttons[1].set_onclick(on_left_click)
	buttons[2].set_onclick(on_right_click)
	buttons[3].set_onclick(on_top_click)
	buttons[4].set_onclick(on_bottom_click)
	buttons[5].set_onclick(toggle_buttons_enabled)

	surface = pygame.display.set_mode((600, 400))
	running = True
	while running:
		for event in pygame.event.get():
			imp.IMP().on_event(event)
			if event.type == pygame.QUIT:
				running = False
		surface.fill(Color.TEAL_FELT)
		side_bar.draw(surface)
		pygame.display.flip()
	pygame.quit()