import pygame
from constants import SCREEN_WIDTH, ROAD_HORIZON_Y, SCREEN_HEIGHT
from utils.sprite_constants import  MIN_TREE_HEIGHT, MIN_TREE_WIDTH

class Tree:

    def __init__(self, tree_sprites, x, side, depth, offset):
        self.x = x
        self.y = ROAD_HORIZON_Y
        self.sprites = tree_sprites
        self.current_sprite = tree_sprites[0]
        self.side = side
        self.base_y = ROAD_HORIZON_Y  # Рівень горизонту
        self.max_height = tree_sprites[0].get_height() * 3  # Максимальна висота дерева
        self.max_width = tree_sprites[0].get_width() * 3  # Максимальна ширина дерева
        self.min_height = MIN_TREE_HEIGHT  # Мінімальна висота дерева
        self.min_width = MIN_TREE_WIDTH  # Мінімальна ширина дерева
        self.depth = depth  # Глибина дерева (чим ближче до 1, тим ближче до гравця)
        self.offset = offset

    @property
    def width(self):
        return int(self.min_width + (self.max_width - self.min_width) * (1 - self.depth))

    @property
    def height(self):
        return int(self.min_height + (self.max_height - self.min_height) * (1 - self.depth))

    def update(self, car_speed, road):
        '''
        Update tree position and depth based on player speed and road curvature.
        '''
        speed_factor = 0.0125  # Factor to adjust depth based on speed

        self.depth -= speed_factor * (car_speed / 200)
        if self.depth < 0.05:
            self.depth = 0

        # Adjust x position based on road curve and side
        lane_edges, self.y = road.get_lane_positions(self.depth)
        if self.side == 'left':
            self.x = lane_edges[0] - self.offset  # Keep it to the left of the road
            self.current_sprite = self.sprites[0]
            if road.next_turn == 'long_left' or 'hard_left':
                self.x -= 50
        elif self.side == 'right':
            if road.next_turn == 'long_right' or 'hard_right':
                self.x += 50
            self.current_sprite = self.sprites[1]
            self.x = lane_edges[-1] + self.offset  # Keep it to the right of the road

    def is_visible(self):
        return self.depth > 0 and (0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT)

    def render(self, screen):
        scaledImage = pygame.transform.scale(self.current_sprite, (self.width, self.height))
        scaledImage.set_colorkey((0, 0, 0))
        screen.blit(scaledImage, (self.x, self.y - self.height));