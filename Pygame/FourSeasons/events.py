#events.py
import pygame
from pygame import freetype
import imp
from structs import *

PYGAME_EVENT_TYPE_TO_STRING = {
	pygame.QUIT            : 'QUIT',
	pygame.MOUSEMOTION     : 'MOUSEMOTION',
	pygame.MOUSEBUTTONUP   : 'MOUSEBUTTONUP',
	pygame.MOUSEBUTTONDOWN : 'MOUSEBUTTONDOWN',
	pygame.KEYDOWN         : 'KEYDOWN',
	pygame.KEYUP           : 'KEYUP',
	pygame.VIDEORESIZE     : 'VIDEORESIZE',
	pygame.USEREVENT       : 'USEREVENT'
}

PYGAME_KEY_TO_STRING = {
	pygame.K_ESCAPE : 'ESCAPE',
	pygame.K_EQUALS : 'EQUALS',
	pygame.K_MINUS  : 'MINUS',
	pygame.K_1 		: '1',
	pygame.K_2 		: '2',
	pygame.K_3 		: '3',
	pygame.K_4 		: '4',
	pygame.K_5 		: '5',
	pygame.K_6 		: '6',
	pygame.K_7 		: '7',
	pygame.K_8 		: '8',
	pygame.K_9 		: '9',
	pygame.K_0 		: '0',
	pygame.K_t      : 't',
	pygame.K_r      : 'r'
}

PYGAME_USEREVENT_NAME_TO_STRING = {
	CustomEvent.CARD_TABLE_RESIZE : 'CARD_TABLE_RESIZE',
	CustomEvent.TILE_CLICKED      : 'TILE_CLICKED',
	CustomEvent.CARD_LAYED        : 'CARD_LAYED',
	CustomEvent.CARD_MOTION       : 'CARD_MOTION',
	CustomEvent.NEW_DEAL          : 'NEW_DEAL',
	CustomEvent.FIRST_CARD        : 'FIRST_CARD',
	CustomEvent.DRAW_ONE          : 'DRAW_ONE',
	CustomEvent.GAME_OVER         : 'GAME_OVER',
	CustomEvent.RE_DEAL           : 'RE_DEAL'
}

PYGAME_MOUSE_BUTTON_TO_STRING = {
	MouseButton.LEFT           : 'LEFT',
	MouseButton.MIDDLE         : 'MIDDLE',
	MouseButton.RIGHT          : 'RIGHT',
	MouseButton.FORWARD_WHEEL  : 'FORWARD_WHEEL',
	MouseButton.BACKWARD_WHEEL : 'BACKWARD_WHEEL'
}

def convert(type, value):
	if type == 'type':
		return PYGAME_EVENT_TYPE_TO_STRING[value]
	elif type == 'key':
		if value in PYGAME_KEY_TO_STRING:
			return PYGAME_KEY_TO_STRING[value]
	elif type == 'button':
		return PYGAME_MOUSE_BUTTON_TO_STRING[value]
	elif type == 'user_event':
		return PYGAME_USEREVENT_NAME_TO_STRING[value]
	print(type, value)

class KeyValueListWrapper:
	def __init__(self, d):
		self.list = [(k, v) for k, v in d.items()]

	def to_dict(self):
		return {k : v for k, v in self.list}

	def any(self):
		return any(self.list)

	def __getattr__(self, attr):
		return self.list.__getattribute__(attr)

def event_wrapper(event):
	event.__dict__['type'] = event.type
	return event

class Tree:
	def __init__(self):
		self.root = None
		self.branches = {}
		self.leaves = []

	def __str__(self):
		return '\n'.join(self.print_tree())

	def print_tree(self):
		paths = []
		current_path = ''
		if not self.root == None:
			current_path += '{0}: '.format(self.root)
		if any(self.leaves):
			paths.append('{0} ({1})'.format(current_path, ', '.join([str(x) for x in self.leaves]))) 
		if any(self.branches):
			paths.extend(['{0}{1} -> {2}'.format(current_path, str(k), ', '.join(v.print_tree())) for k, v in self.branches.items()])
		return paths

	def grow_branch(self, leaf, **kargs):
		key_value_pairs = KeyValueListWrapper(kargs)
		if not key_value_pairs.any():
			self.leaves.append(leaf)
		else: 
			self.root, value = key_value_pairs.pop(0)
			if not value in self.branches:
				self.branches[value] = Tree()
			self.branches[value].grow_branch(leaf, **key_value_pairs.to_dict())

	def get_leaves(self, obj):
		if not self.root == None:
			if self.root in obj.__dict__:
				value = obj.__dict__[self.root]
				if value in self.branches:
					return self.branches[value].get_leaves(obj)
		return self.leaves

	def del_leaf(self, leaf, **kargs):
		if self.root == None:
			self.leaves.remove(leaf)
		else:
			key_value_pairs = KeyValueListWrapper(kargs)
			if key_value_pairs.any():
				key, value = key_value_pairs.pop(0)
				if key == self.root and value in self.branches:
					self.branches[value].del_leaf(leaf, **key_value_pairs.to_dict())

class Delegate:
	def __init__(self, name, quell=False, **kargs):
		self.name = name 
		self.types = kargs
		self.invocation_list = []
		self.quell = quell

	def __str__(self):
		type_list_str = ', '.join(['{0}: {1}'.format(k, convert(k, v)) for k, v in self.types.items()])
		invocation_list_str = ', '.join(x.__name__ for x in self.invocation_list)
		return '{0} -> ({1}) -> [{2}]'.format(self.name, type_list_str, invocation_list_str)

	def __add__(self, method):
		return self.add(method)

	def __sub__(self, method):
		self.invocation_list.remove(method)
		return self

	def add(self, method):
		self.invocation_list.append(method)
		return self

	def invoke(self, *args, **kargs):
		if imp.IMP().debug and not self.quell:
			print('Invoke -> {0}'.format(self.__str__()))
		ret_list = []
		for m in self.invocation_list:
			ret_list.append(m(*args, **kargs))
		return ret_list

class Event:
	def __init__(self, name, type, **kargs):
		self.name = name
		self.types = {'type': type, **kargs}

	def without_type(self):
		return {k: v for k, v in self.types.items() if not k == 'type'}

	def post(self, **kargs):
		event = pygame.event.Event(self.types['type'], **self.without_type(), **kargs)
		pygame.event.post(event)

	def create(self, *args, quell=False):
		delegate = Delegate(self.name, quell=quell, **self.types)
		for arg in args:
			delegate += arg 
		return delegate

class QuitEvent (Event):
	def __init__(self, **kargs):
		super().__init__('Quit', pygame.QUIT, **kargs)

class WindowResizeEvent (Event):
	def __init__(self, **kargs):
		super().__init__('Window Resize Event', pygame.VIDEORESIZE, **kargs)

class KeyDownEvent (Event):
	def __init__(self, key, **kargs):
		super().__init__('Key Down Event', pygame.KEYDOWN, key=key, **kargs)

class KeyUpEvent (Event):
	def __init__(self, key, **kargs):
		super().__init__('Key Up Event', pygame.KEYUP, key=key, **kargs)

class MouseMotion (Event):
	def __init__(self, **kargs):
		super().__init__('Mouse Motion Event', pygame.MOUSEMOTION, **kargs)

class MouseButtonUpEvent (Event):
	def __init__(self, name='Mouse Button Up Event', **kargs):
		super().__init__(name, pygame.MOUSEBUTTONUP, **kargs)

class MouseButtonDownEvent (Event):
	def __init__(self, name='Mouse Button Down Event', **kargs):
		super().__init__(name, pygame.MOUSEBUTTONDOWN, **kargs)

class MouseLeftButtonUpEvent (MouseButtonUpEvent):
	def __init__(self, **kargs):
		super().__init__('Mouse Left Button Up Event', button=MouseButton.LEFT, **kargs)

class MouseLeftButtonDownEvent (MouseButtonDownEvent):
	def __init__(self, **kargs):
		super().__init__('Mouse Left Button Down Event', button=MouseButton.LEFT, **kargs)

class MouseRightButtonUpEvent (MouseButtonUpEvent):
	def __init__(self, **kargs):
		super().__init__('Mouse Right Button Up Event', button=MouseButton.RIGHT, **kargs)

class MouseRightButtonDownEvent (MouseButtonDownEvent):
	def __init__(self, **kargs):
		super().__init__('Mouse Right Button Down Event', button=MouseButton.RIGHT, **kargs)

class MouseMiddleButtonUpEvent (MouseButtonUpEvent):
	def __init__(self, **kargs):
		super().__init__('Mouse Middle Button Up Event', button=MouseButton.MIDDLE, **kargs)

class MouseMiddleButtonDownEvent (MouseButtonDownEvent):
	def __init__(self, **kargs):
		super().__init__('Mouse Middle Button Down Event', button=MouseButton.MIDDLE, **kargs)

class MouseForwardWheelButtonUpEvent (MouseButtonUpEvent):
	def __init__(self, **kargs):
		super().__init__('Mouse Forward Wheel Up Event', button=MouseButton.FORWARD_WHEEL, **kargs)

class MouseForwardWheelButtonDownEvent (MouseButtonDownEvent):
	def __init__(self, **kargs):
		super().__init__('Mouse Forward Wheel Down Event', button=MouseButton.FORWARD_WHEEL, **kargs)

class MouseBackwardWheelButtonUpEvent (MouseButtonUpEvent):
	def __init__(self, **kargs):
		super().__init__('Mouse Back Wheel Up Event', button=MouseButton.BACKWARD_WHEEL, **kargs)

class MouseBackwardWheelButtonDownEvent (MouseButtonDownEvent):
	def __init__(self, **kargs):
		super().__init__('Mouse Back Wheel Down Event', button=MouseButton.BACKWARD_WHEEL, **kargs)

class UserEvent (Event):
	def __init__(self, name, **kargs):
		super().__init__('User Event', pygame.USEREVENT, user_event=name, **kargs)

class EventDispatcher:
	def __init__(self):
		self.event_dispatch_tree = Tree()

	def __str__(self):
		return self.event_dispatch_tree.__str__()

	def __add__(self, delegate):
		return self.add(delegate)

	def __sub__(self, delegate):
		self.event_dispatch_tree.del_leaf(delegate, **delegate.types)
		return self

	def add(self, delegate):
		self.event_dispatch_tree.grow_branch(delegate, **delegate.types)
		return self

	def invoke(self, event, *args, **kargs):
		delegates = self.event_dispatch_tree.get_leaves(event_wrapper(event))
		for delegate in delegates:
			delegate.invoke(event, *args, **kargs)

if __name__=='__main__':
	pass