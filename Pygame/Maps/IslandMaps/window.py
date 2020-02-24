#window.py
import controls
import go, imp, events
from structs import *

class Window (controls.Control):
	def __init__(self, left_top, size, controls=[], color=Color.LIGHT_GREY):
		self.prv_pos = (0, 0)
		self.dragging = False
		self.controls = controls
		self.window = go.Rect(left_top, size)
		self.wire_events()
		super().__init__(left_top, size, enabled_color=color)

	def wire_events(self):
		imp.IMP().add_listener(events.MouseLeftButtonDownEvent().create(self.on_mouse_left_button_down))
		imp.IMP().add_listener(events.MouseLeftButtonUpEvent().create(self.on_mouse_left_button_up))
		imp.IMP().add_listener(events.MouseMotionEvent().create(self.on_mouse_motion, quell=True))

	def on_mouse_left_button_down(self, event):
		if self.is_within(event.pos):
			self.prv_pos = event.pos
			self.dragging = True

	def on_mouse_left_button_up(self, event):
		self.dragging = False

	def on_mouse_motion(self, event):
		if self.dragging:
			v = go.Vector(*event.pos) - go.Vector(*self.prv_pos)
			self.move(v.v0, v.v1)
			self.prv_pos = event.pos

	def set_size(self, size):
		super().set_size(size)
		self.window.set_size(self.size)

	def set_position(self, left_top):
		super().set_position(left_top)
		self.window.set_position(self.left_top)

	def update(self):
		for control in self.controls:
			control.update()

	def draw(self, surface):
		self.window.draw(surface, self.get_color())
		for control in self.controls:
			control.draw(surface)

if __name__=='__main__':
	import unit_test
	test = unit_test.UnitTest()
	width, height = unit_test.WINDOW_SIZE
	window = Window((width // 2 - 100, height // 2 - 100), (200, 200))
	test.register([window])
	test.run()