import pygame

from project.constants import SCREEN_WIDTH


class Player:
    """
    Клас автомобіля
    """
    def __init__(self):
        self.x = SCREEN_WIDTH // 2  # Початкове положення по горизонталі
        self.y = 500  # Початкове положення по вертикалі
        self.width = 120
        self.height = 60
        self.color = (255, 0, 0)  # Червоний автомобіль
        self.speed = 10  # Початкова швидкість
        self.min_speed = 10
        self.max_speed = 322
        self.move_speed = 10  # Швидкість руху вліво/вправо
        self.target_x = self.x  # Позиція, до якої автомобіль рухається
        self.max_offset = 250  # Максимальна відстань, на яку можна повернути
        self.font = pygame.font.Font(None, 26)

    def move_left(self):
        """
        Переміщує автомобіль вліво.
        """
        self.target_x = max(self.target_x - self.move_speed, 400 - self.max_offset)

    def move_right(self):
        """
        Переміщує автомобіль вправо.
        """
        self.target_x = min(self.target_x + self.move_speed, 400 + self.max_offset)

    def update(self):
        if abs(self.x - self.target_x) > self.move_speed:
            self.x += self.move_speed if self.x < self.target_x else -self.move_speed

    def render(self, screen):
        """
        Малює автомобіль на екрані.
        """
        italic_font = self.font
        italic_font.set_italic(True)
        speed_text = italic_font.render(f"Speed: {self.speed}", True, (102, 10, 5))

        outline_color = (255, 255, 255)
        outline_positions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for offset in outline_positions:
            outline_text = italic_font.render(f"Speed: {self.speed}", True, outline_color)
            screen.blit(outline_text, (10 + offset[0], 580 + offset[1]))

        screen.blit(speed_text, (10, 580))
        pygame.draw.rect(screen, self.color, (self.x - self.width // 2, self.y, self.width, self.height))

    def increase_speed(self):
        """
        Збільшує швидкість.
        """
        if self.speed < self.max_speed:
            self.speed += 10

    def decrease_speed(self):
        """
        Зменшує швидкість.
        """
        if self.speed > self.min_speed:
            self.speed -= 10

    def get_rect(self):
        """
        Повертає прямокутник автомобіля для перевірки зіткнень.
        """
        return pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)

