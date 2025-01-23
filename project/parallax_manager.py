import random

import pygame

from constants import SCREEN_WIDTH, ROAD_HORIZON_Y, SCREEN_HEIGHT


class ParallaxManager:
    """
    Class to handle the background (hills and trees).
    """

    def __init__(self):
        self.background_color = (100, 100, 255)  # Sky blue
        self.hill_color = (34, 139, 34)  # Green (hills)
        self.tree_color = (139, 69, 19)  # Brown (trees)

        # Array of trees (background objects)
        self.trees = []

    def update(self, player_speed, road):
        """
        Update the background based on player speed and road state.
        """
        if player_speed > 0:
            # Update existing trees
            for tree in self.trees:
                tree.update(player_speed, road)

            # Remove trees that are no longer visible
            self.trees = [tree for tree in self.trees if tree.is_visible()]

            if len(self.trees) < 5:
                self.generate_trees(road)

    def generate_trees(self, road):
        # Generate new trees randomly if fewer than 5 are visible

        side = random.choice(['left', 'right'])
        if road.next_turn == "hard_left" and side == 'left':
            return
        if road.next_turn == "hard_right" and side == 'right':
            return

        # Generate trees relative to the road's curvature
        depth = random.uniform(1.0, 1.2)
        lane_edges, y_position = road.get_lane_positions(depth)
        if side == 'left':
            position_x = random.randint(0, int(lane_edges[0]))
        else:
            position_x = random.randint(int(lane_edges[-1]), SCREEN_WIDTH)

        print(position_x)
        self.trees.append(Tree(position_x, side, depth, offset=position_x))

    def render(self, screen):
        """
        Малювання фону
        """
        screen.fill(self.background_color)  # Небо
        pygame.draw.rect(screen, self.hill_color, (0, 400, 800, 200))  # Гори
        for tree in self.trees:
            tree.render(screen, self.tree_color)


class Tree:

    def __init__(self, x, side, depth, offset):
        self.x = x
        self.y = ROAD_HORIZON_Y
        self.side = side
        self.base_y = ROAD_HORIZON_Y  # Рівень горизонту
        self.max_height = 300  # Максимальна висота дерева
        self.max_width = 120  # Максимальна ширина дерева
        self.min_height = 20  # Мінімальна висота дерева
        self.min_width = 10  # Мінімальна ширина дерева
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
        speed_factor = 0.005  # Speed scaling factor

        # Update depth based on speed
        self.depth -= speed_factor * (car_speed / 100)
        if self.depth < 0.1:
            self.depth = 0

        # Adjust x position based on road curve and side
        lane_edges, self.y = road.get_lane_positions(self.depth)
        if self.side == 'left':
            self.x = lane_edges[0] - self.offset  # Keep it to the left of the road
        elif self.side == 'right':
            self.x = lane_edges[-1] + self.offset  # Keep it to the right of the road

    def is_visible(self):
        return self.depth > 0 and (0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT)

    def render(self, screen, color):
        pygame.draw.rect(screen, (139, 69, 19),
                         (self.x + self.width // 3, self.y - self.height, self.width // 4, self.height))  # Trunk
        pygame.draw.ellipse(screen, color,
                            (self.x, self.y - self.height - self.width // 2, self.width, self.width))  # Crown
