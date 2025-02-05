import random

import pygame

from constants import SCREEN_WIDTH, ROAD_HORIZON_Y, SCREEN_HEIGHT
from utils.sprite_manager import SpriteManager
from utils.sprite_constants import MAX_TREE_HEIGHT, MAX_TREE_WIDTH, MIN_TREE_HEIGHT, MIN_TREE_WIDTH


class ParallaxManager:
    """
    Class to handle the background (hills and trees).
    """

    def __init__(self):
        self.background_color = (100, 100, 255)  # Sky blue
        self.hill_color = (34, 139, 34)  # Green (hills)
        self.leftOffset = 0
        self.rightOffset = 0
        self.skySprites = pygame.transform.scale(SpriteManager.loadImage('sky.png'), (800, 550));
        self.grassSprites = pygame.transform.scale(SpriteManager.loadImage('grass.png'), (800, 400));
        self.mountainsSprites = [
            pygame.transform.scale(SpriteManager.loadImage('hills_l.png'), (800, 400)),
            pygame.transform.scale(SpriteManager.loadImage('hills_r.png'), (800, 400)),
        ]

        # Array of trees (background objects)
        self.trees = []

    def update(self, screen, player_speed, road):
        """
        Update the background based on player speed and road state.
        """
        if player_speed > 0:
            # Update existing trees
            
            for tree in self.trees:
                tree.update(player_speed, road)

            # Remove trees that are no longer visible
            self.trees = [tree for tree in self.trees if tree.is_visible()]

            if len(self.trees) < 3:
                self.generate_trees(road)
            
            maxLeftOffset = (road.calculate_control_points(road.next_turn)['left'][1][0] - 
                             road.calculate_control_points('straight')['left'][1][0]) * -1;
            maxRightOffset = (road.calculate_control_points(road.next_turn)['right'][1][0] -
                              road.calculate_control_points('straight')['right'][1][0]) * -1;
            
            if (self.leftOffset > maxLeftOffset):
                self.leftOffset -= 1;
            elif (self.leftOffset < maxLeftOffset):
                self.leftOffset += 1;

            if (self.rightOffset < maxRightOffset):
                self.rightOffset += 1;
            elif (self.rightOffset > maxRightOffset):
                self.rightOffset -= 1;
            
            self.update_mountains(screen);

    def generate_trees(self, road):
        # Generate new trees randomly if fewer than 3 are visible

        side = random.choice(['left', 'right'])
        if road.next_turn == "hard_left" and side == 'left':
            return
        if road.next_turn == "hard_right" and side == 'right':
            return

        # Generate trees relative to the road's curvature
        depth = random.uniform(1.0, 1.2)
        lane_edges, y_position = road.get_lane_positions(depth)
        offset = random.randint(10, 200)  # Fixed offset range

        if side == 'left':
            if int(lane_edges[0]) - offset > 0:
                position_x = random.randint(0, int(lane_edges[0]) - offset)
            else:
                return
        elif int(lane_edges[-1]) + offset < SCREEN_WIDTH - 1:
            position_x = random.randint(int(lane_edges[-1]) + offset, SCREEN_WIDTH)
        else:
            return

        self.trees.append(Tree(position_x, side, depth, offset))

    def update_mountains(self, screen):
        screen.blit(self.mountainsSprites[0], (self.leftOffset, 10))
        screen.blit(self.mountainsSprites[1], (self.rightOffset, 10))
    
    def render(self, screen):
        """
        Малювання фону
        """
        screen.blit(self.skySprites, (0, 0)) 
        self.update_mountains(screen);
        screen.blit(self.grassSprites, (0, 220))
        # pygame.draw.rect(screen, self.hill_color, (0, 400, 800, 200))  # Гори
        for tree in self.trees:
            tree.render(screen)


class Tree:

    def __init__(self, x, side, depth, offset):
        self.x = x
        self.y = ROAD_HORIZON_Y
        self.sprite = SpriteManager.loadImage('tree.png');
        self.side = side
        self.base_y = ROAD_HORIZON_Y  # Рівень горизонту
        self.max_height = MAX_TREE_HEIGHT  # Максимальна висота дерева
        self.max_width = MAX_TREE_WIDTH  # Максимальна ширина дерева
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
        """
        Update tree position and depth based on player speed and road curvature.
        """
        speed_factor = 0.008  # Speed scaling factor

        # Update depth based on speed
        self.depth -= speed_factor * (car_speed / 100)
        if self.depth < 0.1:
            self.depth = 0

        # Adjust x position based on road curve and side
        lane_edges, self.y = road.get_lane_positions(self.depth)
        if self.side == 'left':
            self.x = lane_edges[0] - self.offset  # Keep it to the left of the road
            if road.next_turn == 'long_left' or 'hard_left':
                self.x -= 50
        elif self.side == 'right':
            if road.next_turn == 'long_right' or 'hard_right':
                self.x += 50
            self.x = lane_edges[-1] + self.offset  # Keep it to the right of the road

    def is_visible(self):
        return self.depth > 0 and (0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT)

    def render(self, screen):   
        scaledImage = pygame.transform.scale(self.sprite, (self.width, self.height))
        screen.blit(scaledImage, (self.x, self.y - self.height));
