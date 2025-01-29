import pygame


class ParallaxManager:

    """
    Не зроблено, мертвий клас
    """
    def __init__(self):
        self.background_color = (100, 100, 255)  # Блакитне небо
        self.hill_color = (34, 139, 34)  # Зелений (гори)
        self.tree_color = (139, 69, 19)  # Коричневий (дерева)

    def update(self, player_speed):
        pass  # Простий фон, немає оновлення в цьому прикладі

    def render(self, screen):
        screen.fill(self.background_color)  # Небо
        pygame.draw.rect(screen, self.hill_color, (0, 400, 800, 200))  # Гори
<<<<<<< Updated upstream
        pygame.draw.rect(screen, self.tree_color, (100, 450, 50, 100))  # Дерева
=======
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
        speed_factor = 0.012  # Speed scaling factor

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

    def render(self, screen, color):
        pygame.draw.rect(screen, (139, 69, 19),
                         (self.x + self.width // 3, self.y - self.height, self.width // 4, self.height))  # Trunk
        pygame.draw.ellipse(screen, color,
                            (self.x, self.y - self.height - self.width // 2, self.width, self.width))  # Crown
>>>>>>> Stashed changes
