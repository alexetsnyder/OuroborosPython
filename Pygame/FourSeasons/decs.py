#decs.py
import pygame
import imp, events

def singleton(cls):	
	class SingletonWrapper (cls):
		def __init__(self):
			self.cls = cls
			self.instance = None

		def __call__(self, *args, **kargs):
			if self.instance == None:
				self.instance = self.cls(*args, **kargs)
			return self.instance
	return SingletonWrapper()

def undo_enabled():
	pass

def pause_events_class(cls):
	class ClassWrapper (cls):
		def __init__(self, *args, **kargs):
			self.is_paused = False
			super().__init__(*args, **kargs)

		def on_pause(self, event):
			self.is_paused = not self.is_paused

		def wire_events(self):
			super().wire_events()
			imp.IMP().add_delegate(events.KeyDownEvent(pygame.K_ESCAPE).create(self.on_pause))
	return ClassWrapper

def pause_events_method(func):
	def func_wrapper(self, event):
		if not self.is_paused:
			func(self, event)
	return func_wrapper

def plottable(cls):
	class PlottableClass (cls):
		def __init__(self, left_top, size, *args, margins=(0, 0), **kargs):
			self.m_w, self.m_h = margins
			self.set_size(size)
			self.set_position(left_top)
			super().__init__(*args, **kargs)

		def set_size(self, size):
			self.w, self.h = self.size = size
			self.h_w, self.h_h = self.w // 2, self.h // 2
			if hasattr(super(), 'set_size'):
				super().set_size(size)

		def set_position(self, left_top):
			left, top = self.origin = left_top
			self.left, self.right = left + self.m_w, left + self.w - self.m_w 
			self.top, self.bottom = top + self.m_h, top + self.h - self.m_h 
			self.left_top = (self.left, self.top)
			self.left_bottom = (self.left, self.bottom)
			self.right_top = (self.right, self.top)
			self.right_bottom = (self.right, self.bottom) 
			self.x, self.y = self.center = self.left + self.h_w, self.top + self.h_h
			if hasattr(super(), 'set_position'):
				super().set_position(left_top)

		def get_size(self):
			if hasattr(super(), 'get_size'):
				return super().get_size()
			return self.size 

		def center_on(self, position):
			x, y = position
			w, h = self.get_size()
			self.set_position((x - w // 2, y - h // 2))
			return self

		def move(self, dx, dy):
			self.set_position((self.left + dx, self.top + dy))
	return PlottableClass

if __name__=='__main__':
	pass