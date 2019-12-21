#acts.py
import events
from structs import *

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
		events.UserEvent(CustomEvent.REDO_STACK_CLEARED).post()
		events.UserEvent(CustomEvent.UNDO_ENABLED).post()

	def clear(self):
		self.redo_stack.clear()
		self.undo_stack.clear()
		events.UserEvent(CustomEvent.REDO_STACK_CLEARED).post()
		events.UserEvent(CustomEvent.UNDO_STACK_CLEARED).post()

	def can_undo(self):
		return len(self.undo_stack) > 0

	def can_redo(self):
		return len(self.redo_stack) > 0

	def redo(self):
		if any(self.redo_stack):
			redo_action = self.redo_stack.pop()
			redo_action.redo()
			self.undo_stack.append(redo_action)
			events.UserEvent(CustomEvent.UNDO_ENABLED).post()

	def undo(self):
		if any(self.undo_stack):
			undo_action = self.undo_stack.pop()
			undo_action.undo()
			self.redo_stack.append(undo_action)
			events.UserEvent(CustomEvent.REDO_ENABLED).post()

if __name__=='__main__':
	pass