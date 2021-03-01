#events.py
import pygame

class Delegate:
	def __init__(self, type, name=None, func=None):
		self.type = type
		self.name = name
		self.func = func

	def invoke(self, event, *args, **kargs):
		return self.func(event, *args, **kargs)

class Event:
	def __init__(self, type, name=None):
		self.type = type
		self.name = name

	def create(self, func):
		return Delegate(self.type, self.name, func)

	def post(self, **kargs):
		event = None
		if not self.name == None:
			event = pygame.event.Event(self.type, name=self.name, **kargs)
		else:
			event = pygame.event.Event(self.type, **kargs)
		pygame.event.post(event)

class QuitEvent (Event):
	def __init__(self):
		super().__init__(pygame.QUIT)

class KeyDownEvent (Event):
	def __init__(self):
		super().__init__(pygame.KEYDOWN)

class VideoResizeEvent (Event):
	def __init__(self):
		super().__init__(pygame.VIDEORESIZE)

class UserEvent (Event):
	def __init__(self, name):
		super().__init__(pygame.USEREVENT, name=name)

class EventDispatcher:
	def __init__(self): 
		self.events = {}
		self.user_events = {}

	def add_listener(self, delegate):
		if delegate.type == pygame.USEREVENT:
			if not delegate.name in self.user_events:
				self.user_events[event_name] = []
			self.user_events[event.name].append(delegate) 
		else:
			if not delegate.type in self.events:
				self.events[delegate.type] = []
			self.events[delegate.type].append(delegate)

	def invoke(self, event, *args, **kargs):
		ret_list = []
		if event.type == pygame.USEREVENT:
			if event.name in self.user_events:
				for delegate in self.user_events[event.name]:
					ret_list.append(delegate.invoke(event, *args, **kargs))
		else:
			if event.type in self.events:
				for delegate in self.events[event.type]:
					ret_list.append(delegate.invoke(event, *args, **kargs))
		return ret_list

if __name__=='__main__':
	pass