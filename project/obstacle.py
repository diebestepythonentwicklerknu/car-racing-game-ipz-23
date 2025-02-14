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
        self.lane = lane
        self.depth = depth  # Horizon
        self.color = (0, 255, 0)
        self.speed_factor = 0.006
        self.sprite = SpriteManager.load_image('obstacle.png')

    def update(self, car_speed):
        """
        Updates the obstacle position based on the car depth and speed
        """
        self.depth -= self.speed_factor * (car_speed / 100)  # The closer to the player the bigger the size

    def compute_rect(self, road, camera_offset_x, scale_factor=1.0):
        lane_edges, y = road.get_lane_positions(self.depth, camera_offset_x)
        width = max((lane_edges[self.lane + 1] - lane_edges[self.lane]) * 0.8 * scale_factor, 15)
        height = width // OBSTACLE_RATIO
        x = (lane_edges[self.lane] + lane_edges[self.lane + 1]) // 2

        return pygame.Rect(x - width // 2, y - height, width, height)

#<<<<<<< car-racing-fix-develop
    #def get_reduced_rect(self, road, camera_offset_x):
        """
        Обчислення хітбоксу, меншого за візуал
        :param road:
        :param camera_offset_x:
        :return:
        """
        #rect = self.get_rect(road, camera_offset_x)
        #reduced_width = int(rect.width * 0.8)
        #reduced_height = int(rect.height * 0.8)
        #return pygame.Rect(
            #rect.x + (rect.width - reduced_width) // 2,
            #rect.y + (rect.height - reduced_height) // 2,
            #reduced_width, reduced_height
        #)

    #def get_increased_rect(self, road, camera_offset_x):
        """
        Обчислення хітбоксу, більшого за візуал
        Використовується для близького обгону
        :param road:
        :param camera_offset_x:
        :return:
        """
        #rect = self.get_rect(road, camera_offset_x)
        #increased_width = rect.width * 1.5
        #increased_height = rect.height
        #new_x = rect.x - (increased_width - rect.width) // 2  # Центрування хітбоксу

        #return pygame.Rect(
            #new_x, rect.y,
            #increased_width, increased_height
        #)
#=======
    def get_rect(self, road, camera_offset_x):
        return self.compute_rect(road, camera_offset_x=camera_offset_x)

    def get_reduced_rect(self, road, camera_offset_x):
        return self.compute_rect(road, camera_offset_x, scale_factor=0.8)

    def get_increased_rect(self, road, camera_offset_x):
        return self.compute_rect(road, camera_offset_x, scale_factor=1.4)  # Fix: made a  size of the bigger hitbox a lil bit smaller
#>>>>>>> new-merge-branch

    def render(self, screen, road, camera_offset_x):
        """
        Renders obstalces on the screen
        """

        rect = self.get_rect(road, camera_offset_x)
        scaled_image = pygame.transform.scale(self.sprite, (rect.width, rect.height))
        screen.blit(scaled_image, rect)

        # Uncomment to test the hitbox
        # reduced_rect = self.get_reduced_rect(road)
        # increased_rect = self.get_increased_rect(road)
        # pygame.draw.rect(screen, (100, 199, 100), reduced_rect, 1)
        # pygame.draw.rect(screen, (255, 0, 0), increased_rect, 1)
