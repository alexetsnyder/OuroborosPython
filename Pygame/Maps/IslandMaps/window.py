#window.py
import controls, go

class Window (controls.Control):
	def __init__(self, left_top, size):
		self.window = go.Rect(left_top, size)
		super().__init__(left_top, size)

	def set_size(self, size):
		super().set_size(size)
		self.window.set_size(self.size)

	def set_position(self, left_top):
		super().set_position(left_top)
		self.window.set_position(self.left_top)


if __name__=='__main__':
	pass