#main.py
import sys
import pygame
from enums import *
import ge, helio, config

class Game:
	def __init__(self, config_file):
		ge.GameEngine.init()
		self.config = config.Data(config_file, helio)
		self.game_engine = ge.GameEngine(self.config, helio.EventManager)

	def run(self):
		self.game_engine.game_loop()

if __name__=='__main__':
	config_file = sys.argv[1].strip()
	game = Game(config_file)
	game.run()