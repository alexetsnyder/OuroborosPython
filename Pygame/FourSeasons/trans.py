#trans.py

class UndoAction:
	def __init__(self, undo_method, redo_method, *args):
		self.undo_method = undo_method
		self.redo_method = redo_method
		self.args = args 

	def undo(self):
		self.undo_method(*self.args)

	def redo(self):
		self.redo_method(*self.args)

class UndoActions:
	def __init__(self):
		self.undo_stack = []
		self.redo_stack = []

	def post(self, action):
		self.redo_stack.clear()
		self.undo_stack.append(action)

	def clear(self):
		self.redo_stack.clear()
		self.undo_stack.clear()

	def redo(self):
		if any(self.redo_stack):
			redo_action = self.redo_stack.pop()
			redo_action.redo()
			self.undo_stack.append(redo_action)

	def undo(self):
		if any(self.undo_stack):
			undo_action = self.undo_stack.pop()
			undo_action.undo()
			self.redo_stack.append(undo_action)

if __name__=='__main__':
	pass