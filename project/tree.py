import pygame

from constants import SCREEN_WIDTH, ROAD_HORIZON_Y, SCREEN_HEIGHT
from utils.sprite_constants import MIN_TREE_HEIGHT, MIN_TREE_WIDTH


class Tree:
    """
    Class to represent a tree on the side of the road.
    """

    def __init__(self, tree_sprites, x, side, depth, offset):
        self.__x = x
        self.__y = ROAD_HORIZON_Y
        self.__sprites = tree_sprites
        self.__current_sprite = tree_sprites[0]
        self.__side = side
        self.__base_y = ROAD_HORIZON_Y  
        self.__max_height = tree_sprites[0].get_height() * 3  
        self.__max_width = tree_sprites[0].get_width() * 3  
        self.__min_height = MIN_TREE_HEIGHT  
        self.__min_width = MIN_TREE_WIDTH  
        self.depth = depth  # The closer to the player (1) the bigger the size
        self.__offset = offset

    @property
    def width(self):
        return int(self.__min_width + (self.__max_width - self.__min_width) * (1 - self.depth))

    @property
    def height(self):
        return int(self.__min_height + (self.__max_height - self.__min_height) * (1 - self.depth))

    def update(self, car_speed, road, camera_offset_x):
        """
        Update tree position and depth based on player speed and road curvature.
        """
        speed_factor = 0.0125  # Factor to adjust depth based on speed

        self.depth -= speed_factor * (car_speed / 200)
        if self.depth < 0.05:
            self.depth = 0

        # Adjust x position based on road curve and side
        lane_edges, self.__y = road.get_lane_positions(self.depth, camera_offset_x)
        if self.__side == 'left':
            self.__x = lane_edges[0] - self.__offset  # Keep it to the left of the road
            self.__current_sprite = self.__sprites[0]
            if road.next_turn == 'long_left' or 'hard_left':
                self.__x -= 50
        elif self.__side == 'right':
            if road.next_turn == 'long_right' or 'hard_right':
                self.__x += 50
            self.__current_sprite = self.__sprites[1]
            self.__x = lane_edges[-1] + self.__offset  # Keep it to the right of the road

    def is_visible(self):
        """
        Returns True if the tree is visible on the screen.
        """
        return self.depth > 0 and (0 <= self.__x <= SCREEN_WIDTH and 0 <= self.__y <= SCREEN_HEIGHT)

    def render(self, screen):
        """
        Render the tree on the screen.
        """
        scaled_image = pygame.transform.scale(self.__current_sprite, (self.width, self.height))
        scaled_image.set_colorkey((0, 0, 0))
        screen.blit(scaled_image, (self.__x, self.__y - self.height))
