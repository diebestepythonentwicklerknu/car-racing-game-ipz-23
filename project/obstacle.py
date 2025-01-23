import pygame


class Obstacle:
    def __init__(self, lane, depth=1):
        self.lane = lane
        self.depth = depth  # Початкова глибина (горизонт)
        self.color = (0, 255, 0)  # Зелений колір перешкоди
        self.speed_factor = 0.005

    def update(self, car_speed):
        """
        Оновлює глибину перешкоди для наближення.
        """
        self.depth -= self.speed_factor * (car_speed / 100)  # Чим ближче до гравця, тим менша глибина
        if self.depth <= 0.1:
            self.depth = 0

    def get_rect(self, road):
        """
        Обчислює позицію і розмір перешкоди на основі перспективи.
        """
        lane_edges, y = road.get_lane_positions(self.depth)
        width = max((lane_edges[self.lane + 1] - lane_edges[self.lane]) * 0.8, 15)
        height = width / 2  # Пропорційна висота
        x = (lane_edges[self.lane] + lane_edges[self.lane + 1]) // 2
        return pygame.Rect(x - width // 2, y - height, width, height)

    def get_reduced_rect(self, road):
        """
        Обчислення хітбоксу, меншого за візул
        :param road:
        :return:
        """
        rect = self.get_rect(road)
        reduced_width = rect.width // 2
        reduced_height = rect.height // 2
        return pygame.Rect(
            rect.x + rect.width // 4,
            rect.y + rect.height // 4,
            reduced_width, reduced_height
        )

    def render(self, screen, road):
        """
        Малює перешкоду на екрані.
        """
        rect = self.get_rect(road)
        pygame.draw.rect(screen, self.color, rect)
        # Відмалювання хітбокса (Для тесту розкоментити)
        reduced_rect = self.get_reduced_rect(road)
        pygame.draw.rect(screen, (100, 199, 100), reduced_rect, 1)
