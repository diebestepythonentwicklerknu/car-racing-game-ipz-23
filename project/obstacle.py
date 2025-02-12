import pygame

from utils.sprite_constants import OBSTACLE_RATIO
from utils.sprite_manager import SpriteManager

'''
Class to handle the obstacles on the road
'''


class Obstacle:
    def __init__(self, lane, depth=1):
        """
        Initializes the obstacle components
        """
        self.__lane = lane
        self.depth = depth  # Horizon
        self.__speed_factor = 0.006
        self.__sprite = SpriteManager.load_image('obstacle.png')

    def update(self, car_speed):
        """
        Updates the obstacle position based on the car depth and speed
        """
        self.depth -= self.__speed_factor * (car_speed / 100)  # The closer to the player the bigger the size

    def __compute_rect(self, road, scale_factor=1.0, camera_offset_x=0):
        lane_edges, y = road.get_lane_positions(self.depth, camera_offset_x)
        width = max((lane_edges[self.__lane + 1] - lane_edges[self.__lane]) * 0.8 * scale_factor, 15)
        height = width // OBSTACLE_RATIO
        x = (lane_edges[self.__lane] + lane_edges[self.__lane + 1]) // 2

        return pygame.Rect(x - width // 2, y - height, width, height)

    def get_rect(self, road, camera_offset_x):
        return self.__compute_rect(road, camera_offset_x=camera_offset_x)

    def get_reduced_rect(self, road, camera_offset_x):
        return self.__compute_rect(road, scale_factor=0.8, camera_offset_x=camera_offset_x)

    def get_increased_rect(self, road, camera_offset_x):
        return self.__compute_rect(road, scale_factor=1.4, camera_offset_x=camera_offset_x)  # Fix: made a  size of the bigger hitbox a lil bit smaller

    def render(self, screen, road, camera_offset_x):
        """
        Renders obstalces on the screen
        """

        rect = self.get_rect(road, camera_offset_x)
        scaled_image = pygame.transform.scale(self.__sprite, (rect.width, rect.height))
        screen.blit(scaled_image, rect)

        # Uncomment to test the hitbox
        # reduced_rect = self.get_reduced_rect(road)
        # increased_rect = self.get_increased_rect(road)
        # pygame.draw.rect(screen, (100, 199, 100), reduced_rect, 1)
        # pygame.draw.rect(screen, (255, 0, 0), increased_rect, 1)
