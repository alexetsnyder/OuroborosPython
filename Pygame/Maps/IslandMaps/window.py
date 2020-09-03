#window.py
import controls
import go, imp, events
from structs import *

class Window (controls.Control):
	def __init__(self, title, left_top, size, color=Color.LIGHT_GREY, header_color=Color.DEEP_SKY_BLUE):
		super().__init__()
		self.title = title 
		self.dragging = False	
		self.mouse_pos = (0, 0)
		self.controls = []
		self.fixed_positions = []
		self.title_height = 20
		self.window_border = go.Rect(left_top, tuple(x + 2 for x in size), width=1)
		self.window = go.Rect(left_top, size)
		self.lbl_text = go.RenderText(self.title, self.get_style('default_text'))
		self.header = go.Rect(left_top, size)
		self.line = go.HorizontalLine((0, 0), 0)
		self.set_size(size)
		self.set_position(left_top)
		self.wire_events()

	def wire_events(self):
		imp.IMP().add_listener(events.MouseLeftButtonDownEvent().create(self.on_mouse_left_button_down))
		imp.IMP().add_listener(events.MouseLeftButtonUpEvent().create(self.on_mouse_left_button_up))
		imp.IMP().add_listener(events.MouseMotionEvent().create(self.on_mouse_motion, quell=True))

	def on_mouse_left_button_down(self, event):
		if self.is_within(event.pos):
			self.mouse_pos = event.pos
			self.dragging = True

	def on_mouse_left_button_up(self, event):
		self.dragging = False

	def on_mouse_motion(self, event):
		if self.dragging:
			v = go.Vector(*event.pos) - go.Vector(*self.mouse_pos)
			self.move(v.v0, v.v1)
			self.mouse_pos = event.pos

	def set_size(self, size):
		super().set_size(size)
		self.window.set_size(self.size)
		self.window_border.set_size(tuple(x + 2 for x in self.size))
		self.header.set_size((self.w, self.title_height))
		self.line.set_width(self.header.w)

	def set_position(self, left_top):
		super().set_position(left_top)
		self.window.set_position(self.left_top)
		self.window_border.set_position((self.left - 1, self.top - 1))
		self.header.set_position(self.left_top)
		self.line.set_position(self.header.left_bottom)
		self.lbl_text.center_on(self.header.center)
		self.position_controls()

	def set_enabled(self, is_enabled):
		super().set_enabled(is_enabled)
		for control in self.controls:
			control.set_enabled(is_enabled)

	def set_controls(self, controls):
		self.fixed_positions.clear()
		self.controls = controls
		for control in self.controls:
			self.fixed_positions.append(control.left_top)
		self.position_controls()

	def position_controls(self):
		start_top = self.top + self.title_height
		for i, control in enumerate(self.controls):
			left, top = self.fixed_positions[i]
			control.set_position((self.left + left, start_top + top))

	def update(self):
		for control in self.controls:
			control.update()

	def draw(self, surface):
		border_color = self.get_style('default_border').color
		self.window_border.draw(surface, border_color)
		self.window.draw(surface, self.get_style('window_back').color)
		self.header.draw(surface, self.get_style('header').color)
		self.lbl_text.draw(surface, self.get_style('default_text').color)
		self.line.draw(surface, border_color)
		for control in self.controls:
			control.draw(surface)

if __name__=='__main__':
	import unit_test, pygame
	test = unit_test.UnitTest()
	width, height = unit_test.WINDOW_SIZE
	slider = controls.Slider()
	btn_ok = controls.Button('OK', on_click=lambda event: print('Pressed Ok.'))
	window = Window('Test Window', (width // 2 - 100, height // 2 - 100), (200, 100))
	slider.set_position((10, 15))
	btn_ok.set_position((200 - btn_ok.w - 5, 80 - btn_ok.h - 5)) 
	window.set_controls([slider, btn_ok])
	imp.IMP().add_listener(events.KeyDownEvent(pygame.K_s).create(lambda event : window.set_enabled(not window.is_enabled)))
	test.register([window])
	test.run()