import os

import pygame

from camera import Camera
from car import Ferrari458Italia
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from input_manager import InputManager
from menu import Menu
from obstacle_manager import ObstacleManager
from parallax_manager import ParallaxManager
from road import Road
from score_manager import ScoreManager
from scoreboard import ScoreBoard
from utils.sprite_manager import SpriteManager


class Game:
    def __init__(self, nickname=None):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racing")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.game_over = False  # FIX: Додаємо флаг для екрану завершення гри
        self.nickname = nickname
        self._initialize_game_components()

    def _initialize_game_components(self):
        sky_sprite = pygame.transform.scale(SpriteManager.load_image('sky.png'), (800, 550))
        hills_sprites = [
            pygame.transform.scale(SpriteManager.load_image('hills_l.png'), (800, 400)),
            pygame.transform.scale(SpriteManager.load_image('hills_r.png'), (800, 400)),
        ]
        tree_sprites = SpriteManager.get_frame_sequence('tree-Sheet.png', 64, 96, 2)
        grass_sprites = SpriteManager.get_frame_sequence('grass-Sheet.png', 300, 200, 3)

        self.camera = Camera()
        self.car = Ferrari458Italia()
        self.car.speed = 0
        self.road = Road()
        self.obstacle_manager = ObstacleManager()
        self.input_manager = InputManager()
        self.score_manager = ScoreManager()
        self.parallax_manager = ParallaxManager(grass_sprites, tree_sprites, hills_sprites, sky_sprite)
        self.scoreboard = ScoreBoard()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif self.game_over:  # Якщо гра закінчена, перевіряємо натискання R або Q
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()  # R for restart Q for quit
                    elif event.key == pygame.K_q:
                        self.go_to_main_menu()
            else:
                self.input_manager.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    self.camera.switch_mode(self.car)  # Переключення режиму камери

        if not self.game_over and self.input_manager.is_pause_pressed():
            self.paused = not self.paused

    def update(self):
        if self.game_over or self.paused:
            return

        delta_time = self.clock.get_time() / 1000
        self.input_manager.update_car(self.car)
        self.car.update(self.road, delta_time, self.camera)
        self.camera.update(self.car)

        if self.car.speed != 0:  # FIX: if the speed is set to 0, then do not update parallax & score
            self.road.update(self.car.speed, delta_time)
            self.parallax_manager.update(self.screen, self.car.speed, self.road, self.camera.camera_offset_x)

            if self.obstacle_manager.update(self.car, self.road, self.score_manager, self.car.speed,
                                            self.camera.camera_offset_x):
                pygame.time.delay(100)
                self.show_game_over_screen()

            self.score_manager.update(self.car.speed, self.car.max_speed)

    def render(self):
        if self.game_over:
            self.show_game_over_message()  # FIX: Відображаємо екран завершення гри
        elif not self.paused:
            self.screen.fill((100, 200, 255))
            self.parallax_manager.render(self.screen)
            self.road.render(self.screen, self.camera)
            self.obstacle_manager.render(self.screen, self.road, self.camera.camera_offset_x)
            self.car.render(self.screen)
            self.score_manager.render(self.screen)
        else:
            pause_font = pygame.font.Font(os.path.join(os.path.dirname(__file__),
                                                       "assets", "PressStart2P-Regular.ttf"), 40)
            pause_text = pause_font.render("Paused", True, (255, 255, 255))
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(FPS)

        if self.nickname:
            self.scoreboard.update_score(self.nickname, int(self.score_manager.score))
        pygame.quit()

    def show_game_over_screen(self):
        """ 
        Встановлює флаг завершення гри і очікує натискання R або Q 
        """
        self.game_over = True

    def show_game_over_message(self):
        """ 
        Малює екран завершення гри 
        """
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(os.path.join(os.path.dirname(__file__),
                                             "assets", "PressStart2P-Regular.ttf"), 30)
        text1 = font.render("Game Over!", True, (255, 0, 0))
        text2 = font.render("Press R to Restart", True, (255, 255, 255))
        text3 = font.render("Press Q for Menu", True, (255, 255, 255))

        self.screen.blit(text1, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(text2, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2))
        self.screen.blit(text3, (SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 + 50))

    def restart_game(self):
        """ 
        Скидає гру без виходу в головне меню
        """
        self._initialize_game_components()
        self.game_over = False

    def go_to_main_menu(self):
        """
        Повертає в меню після завершення гри
        """
        self.scoreboard.update_score(self.nickname, int(self.score_manager.score))

        menu = Menu(self.screen)
        menu.run()

        if menu.nickname and menu.nickname != "Guest":
            self.__init__(menu.nickname)
            self.run()
        else:
            self.__init__("Guest")
            self.run()
