import pygame

from input_manager import InputManager
from pygame.locals import KEYDOWN, KEYUP
from parallax_manager import ParallaxManager
from car import LamborghiniDiablo
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from road import Road
from score_manager import ScoreManager
from obstacle_manage import ObstacleManager # FIX: Obstacle Manager was moved to a separate file

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racing")
        self.clock = pygame.time.Clock()
        self.running = True
        self._initialize_game_components()

    def _initialize_game_components(self):
        self.car = LamborghiniDiablo()
        self.car.speed = 0
        self.road = Road()
        self.obstacle_manager = ObstacleManager()
        self.input_manager = InputManager()
        self.score_manager = ScoreManager()
        self.parallax_manager = ParallaxManager()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.input_manager.handle_event(event)

    def update(self):
        self.input_manager.update_car(self.car)
        self.car.update()
        
        if self.car.speed != 0: # FIX: if the speed is set to 0, than do not update parallax & score
            self.road.update(self.car.speed)
            self.parallax_manager.update(self.car.speed)
            
            if self.obstacle_manager.update(self.car, self.road):
                pygame.time.delay(100)  # Lowered the delay, 'cause feel like we need some hardcore on the road >:3
                self._initialize_game_components()
            self.score_manager.update()

    def render(self):
        self.screen.fill((100, 200, 255))  # Блакитне небо
        self.parallax_manager.render(self.screen)
        self.road.render(self.screen)
        self.obstacle_manager.render(self.screen, self.road)
        self.car.render(self.screen)
        self.score_manager.render(self.screen)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
