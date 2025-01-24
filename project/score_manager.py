import pygame


class ScoreManager:
    """
    Очки
    """

    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.color = (255, 255, 255)

    def update(self):
        self.score += 1  # Збільшення очок з часом

    def render(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, self.color)
        screen.blit(score_text, (10, 10))
