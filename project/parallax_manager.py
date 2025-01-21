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
        pygame.draw.rect(screen, self.tree_color, (100, 450, 50, 100))  # Дерева
