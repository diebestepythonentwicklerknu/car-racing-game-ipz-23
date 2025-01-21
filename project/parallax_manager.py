import random

import pygame

from project.constants import SCREEN_WIDTH, ROAD_TOP_WIDTH, SCREEN_HEIGHT, ROAD_HORIZON_Y


class ParallaxManager:
    """
    Клас для обробки фону
    """

    def __init__(self):
        self.background_color = (100, 100, 255)  # Блакитне небо
        self.hill_color = (34, 139, 34)  # Зелений (гори)
        self.tree_color = (139, 69, 19)  # Коричневий (дерева)

        # Масив дерев (фоновий об'єкт)
        self.trees = []

    def update(self, player_speed):
        """
        Оновлення фону в залежності від швидкості
        :param player_speed: швидкість авто
        :return:
        """
        for tree in self.trees:
            tree.update(player_speed)

        self.trees = [tree for tree in self.trees if tree.is_visible()]

        # Генерація нових дерев поза межами дороги
        if random.random() < 0.01:  # Шанс появи нового дерева
            position_x = random.choice(
                [random.randint(0, (SCREEN_WIDTH // 2) - (ROAD_TOP_WIDTH // 2)),  # Ліворуч від дороги
                 random.randint((SCREEN_WIDTH // 2) + (ROAD_TOP_WIDTH // 2), SCREEN_WIDTH)  # Праворуч від дороги
                 ])
            self.trees.append(Tree(position_x, random.uniform(0.8, 1.5)))

    def render(self, screen):
        """
        Малювання фону
        """
        screen.fill(self.background_color)  # Небо
        pygame.draw.rect(screen, self.hill_color, (0, 400, 800, 200))  # Гори
        for tree in self.trees:
            tree.render(screen, self.tree_color)


class Tree:
    def __init__(self, x, scale):
        self.x = x
        self.base_y = ROAD_HORIZON_Y  # Рівень горизонту
        self.max_height = 300  # Максимальна висота дерева
        self.max_width = 120  # Максимальна ширина дерева
        self.min_height = 20  # Мінімальна висота дерева
        self.min_width = 10  # Мінімальна ширина дерева
        self.depth = 1  # Глибина дерева (чим ближче до 1, тим ближче до гравця)
        self.direction = -1 if x < SCREEN_WIDTH // 2 else 1

    @property
    def width(self):
        return int(self.min_width + (self.max_width - self.min_width) * (1 - self.depth))

    @property
    def height(self):
        return int(self.min_height + (self.max_height - self.min_height) * (1 - self.depth))

    @property
    def y(self):
        return ROAD_HORIZON_Y - int((SCREEN_HEIGHT - ROAD_HORIZON_Y - 250) * (1 - self.depth))

    def update(self, player_speed):
        self.depth -= 0.0015 * player_speed * 0.1
        if self.depth < 0.1:
            self.depth = 0

        self.x += self.direction * 0.3 * (1 - self.depth) * player_speed

    def is_visible(self):
        return self.x + self.width > 0 and self.x - self.width < SCREEN_WIDTH

    def render(self, screen, color):
        pygame.draw.rect(screen, (139, 69, 19),
                         (self.x + self.width // 3, self.y - self.height, self.width // 4, self.height))  # Стовбур
        pygame.draw.ellipse(screen, color,
                            (self.x, self.y - self.height - self.width // 2, self.width, self.width))  # Крона
