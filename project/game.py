import pygame
import os

from car import LamborghiniDiablo
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from input_manager import InputManager
from parallax_manager import ParallaxManager
from obstacle_manager import ObstacleManager  # FIX: Obstacle Manager was moved to a separate file
from road import Road
from score_manager import ScoreManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racing")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False  # Додаємо флаг для паузи
        self.show_scoreboard = False
        self._initialize_game_components()

    def _initialize_game_components(self):
        self.car = LamborghiniDiablo()
        self.car.speed = 0
        self.road = Road()
        self.obstacle_manager = ObstacleManager()
        self.input_manager = InputManager()
        self.score_manager = ScoreManager()
        self.parallax_manager = ParallaxManager()
        #  self.scoreboard = ScoreBoard()  # Додаємо ScoreBoard

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.input_manager.handle_event(event)

        # Перемикаємо стан паузи
        if self.input_manager.is_pause_pressed():
            self.paused = not self.paused

    def update(self):
        if not self.paused:  # Оновлюємо гру лише якщо не пауза
            delta_time = self.clock.get_time() / 1000
            self.input_manager.update_car(self.car)
            self.car.update(self.road, delta_time)

            if self.car.speed != 0:  # FIX: if the speed is set to 0, than do not update parallax & score
                self.road.update(self.car.speed, delta_time)
                self.parallax_manager.update(self.car.speed, self.road)

                if self.obstacle_manager.update(self.car, self.road, self.score_manager, self.car.speed):
                    pygame.time.delay(100)  # Затримка після аварії
                    self._initialize_game_components()
                self.score_manager.update()

    def render(self):
        if not self.paused:  # Малюємо гру лише якщо не пауза
            self.screen.fill((100, 200, 255))  # Блакитне небо
            self.parallax_manager.render(self.screen)
            self.road.render(self.screen)
            self.obstacle_manager.render(self.screen, self.road)
            self.car.render(self.screen)
            self.score_manager.render(self.screen)
        else:  # Якщо пауза, відображаємо відповідне повідомлення
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
        pygame.quit()
