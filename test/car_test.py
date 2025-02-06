import pytest
import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../project')))

from car import Ferrari458Italia
from obstacle import Obstacle
from obstacle_manager import ObstacleManager
from road import Road

@pytest.fixture(scope='class', autouse=True)
def init_pygame_display(request):
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    pygame.font.init()
    
    yield


def obstacle_collision(self, depth):
    obstacle = Obstacle(1, depth)
    obstacleManager = ObstacleManager()
    obstacleManager.obstacles.append(obstacle)
    road = Road()
    return obstacleManager.check_collision(self.car, road)

class TestCar:
    def setup_method(self):
        self.car = Ferrari458Italia()

    def test_move_right(self):
        self.car.move_right()
        assert self.car.steering_angle > 0
        
    def test_move_left(self):
        self.car.move_left()
        assert self.car.steering_angle < 0

    def test_move_forward(self):
        for i in range(10):
            self.car.increase_throttle()
            self.car._update_speed()
        assert self.car.speed > 0

    def test_stop(self):
        for i in range(10):
            self.car.decrease_speed()
            self.car._update_speed()
        assert self.car.speed == 0

    def test_car_collision(self):
        assert obstacle_collision(self, 0.1) == True
        assert obstacle_collision(self, 0.5) == False