#ge.py 
import pygame
import go, color

class EventManagerWrapper:
	def __init__(self):
		pass

	def on_event(self, event):
		pass

	def update(self):
		pass

class GameEngine:
	def __init__(self, config, event_manager_cls=EventManagerWrapper):
		self.running = True
		self.config = config
		self.window = Window(self.config.try_get('WINDOW_NAME', 'pygame window'), self.config.try_get('WINDOW_SIZE', (0, 0)))
		self.world_center = self.config.try_get('WORLD_CENTER', (0, 0))
		self.game_objects = go.GameObjects(self.config)
		self.event_manager = event_manager_cls(self.game_objects)
		self.physics_engine = PhysicsEngine(self.world_center, self.window.size, self.game_objects)

	def init():
		pygame.init()

	def on_event(self, event):
		self.running = self.window.on_event(event)
		if self.running:
			self.physics_engine.on_event(event)
			self.event_manager.on_event(event)

	def update(self):
		self.event_manager.update()
		self.physics_engine.update()
		self.game_objects.update()

	def draw(self):
		self.window.clear()
		self.game_objects.draw_to(self.window.surface)
		self.window.switch_buffer()

	def game_loop(self):
		while self.running:
			for event in pygame.event.get():
				self.on_event(event)
			self.update()
			self.draw()
		self.clean_up()

	def clean_up(self):
		pygame.quit()

class Window:
	def __init__(self, name, size):
		self.size = size
		pygame.display.set_caption(name)
		self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)

	def on_event(self, event):
		quit = True
		if event.type == pygame.QUIT:
			quit = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quit = False
		elif event.type == pygame.VIDEORESIZE:
			self.size = (event.w, event.h)
			self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)
		return quit

	def clear(self, color=color.BLACK):
		self.surface.fill(color)

	def switch_buffer(self):
		pygame.display.flip()

class PhysicsEngine:
	def __init__(self, center, bounds, game_objects):
		self.x, self.y = self.center = center
		self.width, self.height = self.bounds = bounds
		self.game_objects = game_objects
		self.frame = 1

	def on_event(self, event):
		if event.type == pygame.VIDEORESIZE:
			self.width, self.height = self.bounds = (event.w, event.h)

	def update(self):
		for game_object in self.game_objects.get_all():
			vx, vy = game_object.get_velocity()
			dx, dy = self.set_bounds(game_object, vx, vy)
			game_object.move(dx, dy)
		self.frame += 1

	def set_bounds(self, object, dx, dy):
		x, y = object.get_center()
		vx, vy = object.get_velocity()
		width_margin, height_margin = tuple(x // 2 for x in object.get_bounds())
		if x + dx + width_margin >= self.width or x + dx - width_margin <= 0:
			vx = -vx
			dx = 0
		if y + dy + height_margin >= self.height or y + dy - height_margin <= 0:
			vy = -vy
			dy = 0
		if x >= self.width or y >= self.height:
			object.set_center((self.width // 2, self.height // 2)) 
		object.set_velocity((vx, vy))
		return (dx, dy)