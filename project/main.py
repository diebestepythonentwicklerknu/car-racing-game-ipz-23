import os

import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game
from menu import Menu
from pygame import mixer


'''
Entry point of the game
'''
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Background music
    mixer.init()
    mixer.music.load(os.path.join("project","assets", "sounds", "background_music.wav"))
    mixer.music.set_volume(0.03)
    mixer.music.play(-1)

    # Show menu
    menu = Menu(screen)
    menu.run()

    game = Game(menu.nickname)
    game.run()
