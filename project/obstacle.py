import pygame
import random


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, player, road):
        """
        Оновлює позицію перешкод.
        """
        collision_detected = False
        for obstacle in self.obstacles:
            obstacle.update()
            if obstacle.get_rect(road).colliderect(player.get_rect()):
                collision_detected = True

        # Видалення перешкод
        self.obstacles = [o for o in self.obstacles if o.depth > 0.2]

        # Генерація перешкод
        if random.random() < 0.01:
            lane = random.randint(0, 2)
            self.obstacles.append(Obstacle(lane))

        return collision_detected

    def check_collision(self, player, road):
        """
        Перевіряє, чи є зіткнення між гравцем і будь-якою перешкодою. Не ворк
        """
        for obstacle in self.obstacles:
            if obstacle.get_rect(road).colliderect(player.get_rect()):
                return True
        return False

    def render(self, screen, road):
        """
        Малює всі перешкоди.
        """
        for obstacle in self.obstacles:
            obstacle.render(screen, road)


class Obstacle:
    def __init__(self, lane):
        self.lane = lane
        self.depth = 1  # Початкова глибина (горизонт)
        self.color = (0, 255, 0)  # Зелений колір перешкоди

    def update(self):
        """
        Оновлює глибину перешкоди для наближення.
        """
        self.depth -= 0.006  # Чим ближче до гравця, тим менша глибина
        if self.depth <= 0.1:
            self.depth = 0

    def get_rect(self, road):
        """
        Обчислює позицію і розмір перешкоди на основі перспективи.
        """
        lane_edges, y = road.get_lane_positions(self.depth)
        width = max((lane_edges[self.lane + 1] - lane_edges[self.lane]) * 0.8, 20)
        height = width / 2  # Пропорційна висота
        x = (lane_edges[self.lane] + lane_edges[self.lane + 1]) // 2
        return pygame.Rect(x - width // 2, y - height, width, height)

    def render(self, screen, road):
        """
        Малює перешкоду на екрані.
        """
        rect = self.get_rect(road)
        pygame.draw.rect(screen, self.color, rect)