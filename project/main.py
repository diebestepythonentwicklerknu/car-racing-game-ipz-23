import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game
from menu import Menu

'''
Entry point of the game
'''
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Show menu
    menu = Menu(screen)
    menu.run()

    game = Game(menu.nickname)
    game.run()
