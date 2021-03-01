#events.py
import pygame

EventToString = {
	pygame.QUIT            : 'QUIT',
	pygame.VIDEORESIZE     : 'VIDEORESIZE',
	pygame.USEREVENT       : 'USEREVENT',
	pygame.KEYDOWN         : 'KEYDOWN',
	pygame.KEYUP           : 'KEYUP',
	pygame.MOUSEMOTION     : 'MOUSEMOTION',
	pygame.MOUSEBUTTONDOWN : 'MOUSEBUTTONDOWN',
	pygame.MOUSEBUTTONUP   : 'MOUSEBUTTONUP'
}

class UserEvents:
	UNIT_TEST = 0

UserEventToString = {
	UserEvents.UNIT_TEST : 'UNIT_TEST'
}

class Function:
	def __init__(self, func):
		self.cls_name = func.__self__.__class__.__name__
		self.func = func

	def __str__(self):
		return '{0}: {1}'.format(self.cls_name, self.func.__name__)

	def call(self, event):
		return self.func(event)

class EventHandler:
	def __init__(self, type, name, funcs):
		self.type = type
		self.name = name 
		self.funcs = [Function(func) for func in funcs]

	def __str__(self):
		funcs_str = ', '.join([str(x) for x in self.funcs])
		if self.is_user_event():
			return '{0} -> {1} -> [{2}]'.format(EventToString[self.type], UserEventToString[self.name], funcs_str)
		else:
			return '{0} -> [{1}]'.format(EventToString[self.type], funcs_str)

	def is_user_event(self):
		return self.type == pygame.USEREVENT

	def merge(self, event_handler):
		self.funcs += event_handler.funcs

	def invoke(self, event):
		for func in self.funcs:
			func.call(event)

class Event:
	def __init__(self, type, name=None):
		self.type = type
		self.name = name

	def create(self, funcs):
		return EventHandler(self.type, self.name, funcs)

	def post(self):
		event = pygame.event.Event(self.type, name=self.name)
		pygame.event.post(event)

class QuitEvent (Event):
	def __init__(self):
		super().__init__(pygame.QUIT)

class VideoResizeEvent (Event):
	def __init__(self):
		super().__init__(pygame.VIDEORESIZE)

class UserEvent (Event):
	def __init__(self, name):
		super().__init__(pygame.USEREVENT, name=name)

class KeyDownEvent (Event):
	def __init__(self):
		super().__init__(pygame.KEYDOWN)

class KeyUpEvent (Event):
	def __init__(self):
		super().__init__(pygame.KEYUP)

class MouseMotionEvent (Event):
	def __init__(self):
		super().__init__(pygame.MOUSEMOTION)

class MouseButtonDownEvent (Event):
	def __init__(self):
		super().__init__(pygame.MOUSEBUTTONDOWN)

class MouseButtonUpEvent (Event):
	def __init__(self):
		super().__init__(pygame.MOUSEBUTTONUP)

class EventManager:
	def __init__(self, is_debug=False):
		self.is_debug = is_debug
		self.events = {}
		self.user_events = {}

	def add_listener(self, event_handler):
		if event_handler.is_user_event():
			user_type = event_handler.name 
			if not user_type in self.user_events:
				self.user_events[user_type] = event_handler
			else:
				self.user_events[name].merge(event_handler)
		else:
			event_type = event_handler.type 
			if not event_type in self.events:
				self.events[event_type] = event_handler
			else:
				self.events[event_type].merge(event_handler)

	def log(self, event):
		if self.is_debug:
			print(event)

	def dispatch(self, event):
		event_handler = None
		if event.type in self.events:
			event_handler = self.events[event.type]
		elif hasattr(event, 'name') and event.name in self.user_events:
			event_handler = self.user_events[event.name]
		if not event_handler == None:
			self.log(event_handler)
			event_handler.invoke(event)


if __name__ == '__main__':
	pass