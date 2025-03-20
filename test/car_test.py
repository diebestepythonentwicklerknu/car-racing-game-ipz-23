import os
import sys

import pygame
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\project')))
print("PYTHONPATH:", sys.path)
from project.car import Ferrari458Italia
from project.obstacle import Obstacle
from project.obstacle_manager import ObstacleManager
from project.road import Road
from project import constants
from unittest.mock import MagicMock


# ================== Fixture for initialization ==================
@pytest.fixture(scope='class', autouse=True)
def init_pygame_display(request):
    """
    Fixture for initializing Pygame display
    """
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    pygame.font.init()

    yield


def obstacle_collision(self, depth, camera_offset_x):
    """
    Helper function to check collision with an obstacle
    """
    obstacle = Obstacle(1, depth)
    obstacleManager = ObstacleManager()
    obstacleManager._ObstacleManager__obstacles.append(obstacle)
    road = Road()
    camera_offset_x = 0
    return obstacleManager._check_collision(self.car, road, camera_offset_x)


class TestCar:
    """
    Test for the Car class
    """

    # ================== Sipmle tests ==================

    def setup_method(self):
        self.car = Ferrari458Italia()

    def test_move_forward(self):
        for i in range(10):
            self.car.increase_throttle()
            self.car._update_speed()
        assert self.car.speed > 0

    def test_stop(self):
        for i in range(10):
            self.car.decrease_throttle()
            self.car._update_speed()
        assert self.car.speed == 0

    def test_car_collision(self):
        assert obstacle_collision(self, 0.1, 0) == True
        assert obstacle_collision(self, 0.5, 0) == False

    # ================== Parametrized tests ==================

    @pytest.mark.parametrize("method, expected_sign", [
        ("move_right", 1),  # Expected steering angle (pos for right/neg for left)
        ("move_left", -1)
    ])
    def test_steering(self, method, expected_sign):
        getattr(self.car, method)()  # Call the method
        assert expected_sign * self.car._Car__steering_angle > 0

    @pytest.mark.parametrize("speed,expected_angle", [
        (0, 20),  # Low speed, max angle
        (100, 18),  # Mid speed
        (200, 16),  # High speed, min angle
    ])
    def test_max_steering_angle(self, speed, expected_angle):
        self.car.speed = speed
        assert self.car._Car__get_max_steering_angle() == expected_angle

        # ================== Markered tests ==================

    @pytest.mark.long
    def test_long_acceleration(self):
        for _ in range(500):
            self.car.increase_throttle()
            self.car._update_speed()

        assert self.car.speed > 200

    @pytest.mark.long
    def test_slow_braking(self):
        for _ in range(5):  # Accelerate
            self.car.increase_throttle()
            self.car._update_speed()

        for i in range(1000):  # Testing speed decrease without breaks, using physics
            self.car.decrease_speed(constants.CAR_INERTIA_FACTOR)

        assert self.car.speed == pytest.approx(0, abs=1e-5)

    # ================== Mocking tests ==================

    def test_apply_road_force(self):
        mock_road = MagicMock()
        mock_road.next_turn = "hard_left"
        initial_x = self.car.x
        self.car.speed = 100

        self.car.apply_road_force(mock_road, 0.016)
        self.car._update_speed()

        assert self.car.x != initial_x  # Ensure position is updated

    def test_update_position(self):
        mock_camera = MagicMock()
        mock_camera.get_position()

        self.car._update_position(mock_camera)

        mock_camera.get_position.assert_called_once()  # Ensure method was called
