#controls.py
import go, imp, events
from geo import plottable
from structs import *

@plottable
class Control:
	def __init__(self, left_top, controls=[], default_size=(20, 20), is_override=False):
		self.mw, self.mh = self.margin = (8, 8)
		self.set_default(default_size, is_override)
		self.children = controls
		self.set_size(self.assay_size())
		self.set_position(left_top)

	def set_size(self, size):
		pass

	def set_position(self, left_top):
		self.position_children()

	def set_default(self, default_size, is_override=False):
		self.set_override(is_override)
		self.default_w, self.default_h = self.default_size = default_size

	def set_override(self, is_override):
		self.is_override = is_override

	def assay_size(self):
		return (self.get_w(), self.get_h())

	def position_children(self):
		x = self.x
		y = self.top 
		for child in self.children:
			child.center_on((x, y))
			y += child.h + self.mh

	def get_w(self):
		if self.is_override or not any(self.children):
			return self.default_w + self.mw
		return self.get_max_width()	

	def get_max_width(self):
		max_width = 0
		for child in self.children:
			width = child.w
			if width > max_width:
				max_width = width 
		return max_width + self.mw

	def get_h(self):
		if self.is_override or not any(self.children):
			return self.default_h + self.mh
		return self.get_total_height()

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
	def __init__(self, window_height, controls=[], color=Color.SEA_GREEN):
		self.color = color 
		self.is_showing = True
		self.window_height = window_height
		self.btn_show = Button('<<<', on_click=self.on_click_toggle_bar)
		controls.insert(0, self.btn_show)
		self.rect = go.Rect((0, 0), (0, 0), color=self.color)
		super().__init__((0, 0), controls=controls, default_size=self.btn_show.size)
		self.wire_events()

	def set_size(self, size):
		super().set_size(size)
		self.rect.set_size(size)

	def set_position(self, left_top):
		left, top = left_top
		w, h = self.btn_show.size 	
		super().set_position((left, top + h))
		self.btn_show.center_on((self.right - w // 2, top + h // 2))

	def wire_events(self):
		imp.IMP().add_delegate(events.WindowResizedEvent().listen(self.on_resize))

	def on_resize(self, event):
		self.window_height = event.h
		self.set_size(self.assay_size())

	def on_click_toggle_bar(self, event):
		self.toggle_bar()

	def toggle_bar(self):
		self.is_showing = not self.is_showing
		if self.is_showing:
			self.btn_show.set_text('<<<')
			self.set_override(False)
			self.show_buttons()
		else:
			self.btn_show.set_text('>>>')
			self.set_override(True)
			self.show_buttons(is_show=False)	
		self.set_size(self.assay_size())
		self.set_position((0, 0))

	def show_buttons(self, is_show=True):
		for btn in self.children:
			btn.set_visibility(is_show)
		self.btn_show.set_visibility(True)

	def enable_buttons(self, is_enabled=True):
		for btn in self.children:
			btn.set_enabled(is_enabled)
		self.btn_show.set_enabled(True)

	def get_h(self):
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

	def set_size(self, size):
		super().set_size(size)
		self.rect.set_size(size)

	def set_position(self, left_top):
		super().set_position(left_top)
		self.rect.set_position(left_top)
		self.btn_text.center_on(self.center)

	def set_text(self, text):
		self.btn_text.set_text(text)
		self.set_default(self.btn_text.size)

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

	def set_on_click(self, method):
		self.on_click = method 

	def wire_events(self):
		imp.IMP().add_delegate(events.MouseMotionEvent().listen(self.on_mouse_motion, quell=True))
		imp.IMP().add_delegate(events.MouseLeftButtonDownEvent().listen(self.on_mouse_left_button_down))

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

if __name__=='__main__':
	import pygame
	pygame.init()

	def test_method(event):
		print('Test!')

	imp.IMP().event_dispatcher = events.EventDispatcher()
	buttons = []
	buttons.append(Button('Restart', test_method))
	buttons.append(Button('New Game', test_method))
	buttons.append(Button('Undo', test_method))
	buttons.append(Button('Redo', test_method))
	buttons.append(Button('Pause', test_method))
	side_bar = SideBar(400, controls=buttons)
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