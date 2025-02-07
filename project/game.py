import os

import pygame

import constants
from car import Ferrari458Italia
from input_manager import InputManager
from menu import Menu
from obstacle_manager import ObstacleManager
from parallax_manager import ParallaxManager
from road import Road
from score_manager import ScoreManager
from scoreboard import ScoreBoard
from utils.sprite_manager import SpriteManager


class Game:
    """
    Game class is responsible for managing the game components
    """

    def __init__(self, nickname=None):
        """
        Initializes the game
        """
        pygame.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Racing")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.game_over = False
        self.nickname = nickname
        self._initialize_game_components()

    def _initialize_game_components(self):
        """
        Initializes the game components
        """
        sky_sprite = pygame.transform.scale(SpriteManager.load_image('sky.png'), (800, 550))
        hills_sprites = [pygame.transform.scale(SpriteManager.load_image('hills_l.png'), (800, 400)),
                         pygame.transform.scale(SpriteManager.load_image('hills_r.png'), (800, 400)), ]
        tree_sprites = SpriteManager.get_frame_sequence('tree-Sheet.png', 64, 96, 2)
        grass_sprites = SpriteManager.get_frame_sequence('grass-Sheet.png', 300, 200, 3)

        self.car = Ferrari458Italia()
        self.road = Road()
        self.obstacle_manager = ObstacleManager()
        self.input_manager = InputManager()
        self.score_manager = ScoreManager()
        self.parallax_manager = ParallaxManager(grass_sprites, tree_sprites, hills_sprites, sky_sprite)
        self.scoreboard = ScoreBoard()

    def handle_events(self):
        """
        Handles the game events
        Processes the keys pressed by the user
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_q:
                        self.go_to_main_menu()
            else:
                self.input_manager.handle_event(event)

        if not self.game_over and self.input_manager.is_pause_pressed():
            self.paused = not self.paused

    @staticmethod
    def game_state_guard(func):
        """
        Decorator to prevent updating the game state when the game is over or paused.
        """

        def wrapper(self, *args, **kwargs):
            if self.game_over or self.paused:
                return
            return func(self, *args, **kwargs)

        return wrapper

    @game_state_guard
    def update(self):
        """
        Updates the game elements states
        """
        delta_time = self.clock.get_time() / 1000
        self.input_manager.update_car(self.car)
        self.car.update(self.road, delta_time)

        if self.car.speed != 0:
            self.road.update(self.car.speed, delta_time)
            self.parallax_manager.update(self.screen, self.car.speed, self.road)

            if self.obstacle_manager.update(self.car, self.road, self.score_manager, self.car.speed):
                pygame.time.delay(100)
                self.show_game_over_screen()

            self.score_manager.update(self.car.speed, self.car.max_speed)

    def render(self):
        """
        Renders the game elements on the screen
        """
        if self.game_over:
            self.show_game_over_message()
        elif not self.paused:
            self.screen.fill((100, 200, 255))
            self.parallax_manager.render(self.screen)
            self.road.render(self.screen)
            self.obstacle_manager.render(self.screen, self.road)
            self.car.render(self.screen)
            self.score_manager.render(self.screen)
        else:
            pause_font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"),
                                          40)
            pause_text = pause_font.render("Paused", True, (255, 255, 255))
            self.screen.blit(pause_text, (constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 - 50))

    def run(self):
        """
        Runs the game
        Main game loop
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(constants.FPS)

        if self.nickname:
            self.scoreboard.update_score(self.nickname, int(self.score_manager.score))
        pygame.quit()

    def show_game_over_screen(self):
        """
        Flag that the game is over
        """
        self.game_over = True

    def show_game_over_message(self):
        """
        Shows the game over screen
        """
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 30)
        text1 = font.render("Game Over!", True, (255, 0, 0))
        text2 = font.render("Press R to Restart", True, (255, 255, 255))
        text3 = font.render("Press Q for Menu", True, (255, 255, 255))

        center = (constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2)

        self.screen.blit(text1, (center[0] - 150, center[1] - 100))
        self.screen.blit(text2, (center[0] - 250, center[1]))
        self.screen.blit(text3, (center[0] - 230, center[1] + 50))

    def restart_game(self):
        """
        Restarts the game
        """
        self._initialize_game_components()
        self.game_over = False

    def go_to_main_menu(self):
        """
        Goes back to the main menu
        """
        self.scoreboard.update_score(self.nickname, self.score_manager.score)
        menu = Menu(self.screen)
        menu.run()

        if menu.nickname and menu.nickname != "Guest":
            self.__init__(menu.nickname)
        else:
            self.__init__("Guest")

        self.run()
