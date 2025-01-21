import pygame

from input_manager import InputManager
from obstacle import ObstacleManager
from parallax_manager import ParallaxManager
from player import Player
from road import Road
from score_manager import ScoreManager

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racing")
        self.clock = pygame.time.Clock()
        self.running = True

        self.reset()

        # Змінні для обробки зіткнення
        self.collision_detected = False  # Флаг, чи є активне зіткнення
        self.collision_time = 0  # Час початку зіткнення

    def reset(self):
        self.player = Player()
        self.road = Road()
        self.obstacle_manager = ObstacleManager()
        self.input_manager = InputManager()
        self.parallax_manager = ParallaxManager()
        self.score_manager = ScoreManager()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.input_manager.handle_event(event)

    def update(self):
        """
        Оновлює стан гри.
        """
        self.input_manager.update_player(self.player)
        self.player.update()
        self.road.update(self.player.speed)

        if self.obstacle_manager.update(self.player, self.road):
            pygame.time.delay(500)  # Затримка в 500 мс
            self.reset()

        self.parallax_manager.update(self.player.speed)
        self.score_manager.update()

    def render(self):
        self.screen.fill((100, 200, 255))  # Блакитне небо
        self.parallax_manager.render(self.screen)
        self.road.render(self.screen)
        self.obstacle_manager.render(self.screen, self.road)
        self.player.render(self.screen)
        self.score_manager.render(self.screen)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
