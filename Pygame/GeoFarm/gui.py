#gui.py
from geo import BorderedRect

class GUISurface (BorderedRect):
	ID = 0

	def __init__(self, left_top, size, color):
		super().__init__(left_top, size, color)
		self.id = GUISurface.ID 
		GUISurface.ID += 1

class ToolBar (GUISurface):
	def __init__(self, left_top, size, color):
		super().__init__(left_top, size, color)

	


if __name__=='__main__':
	pass