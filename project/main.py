import pygame
from game import Game
from menu import Menu
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Показуємо меню
    menu = Menu(screen)
    menu.run()

    # Якщо меню закрите, запускаємо гру
    game = Game()
    game.run()
