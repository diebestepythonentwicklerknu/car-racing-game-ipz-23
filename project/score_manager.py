import os

import pygame


class ScoreManager:
    """
    Клас для управління очками та збереження найкращого результату.
    """

    def __init__(self, best_score_file="best_score.txt"):
        self.score = 0.0
        self.best_score = 0
        self.best_score_file = best_score_file
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 20)
        self.color = (255, 255, 255)

        # Завантаження найкращого результату з файлу
        self._load_best_score()

    def _load_best_score(self):
        """
        Завантажує найкращий результат з файлу.
        """
        try:
            with open(self.best_score_file, "r") as file:
                self.best_score = int(file.read().strip())
        except FileNotFoundError:
            print("Файл з найкращим результатом не знайдено, створюється новий.")
            self.best_score = 0
        except ValueError:
            print("Файл найкращого результату пошкоджений. Встановлено значення 0.")
            self.best_score = 0

    def _save_best_score(self):
        """Зберігає найкращий результат у файл."""
        try:
            with open(self.best_score_file, "w") as file:
                file.write(str(self.best_score))
        except IOError as e:
            print(f"Помилка запису найкращого результату у файл: {e}")

    def update(self, car_speed, car_max_speed):
        """
        Оновлює поточний рахунок та перевіряє найкращий результат.
        """
        score_increase = (car_speed / car_max_speed) * 0.5
        score_increase = max(0.01, score_increase)

        self.score += score_increase  # Збільшення очок
        if self.score > self.best_score:
            self.best_score = int(self.score)
            self._save_best_score()

    def add_score(self, points):
        """Додає задану параметром к-сть очок до поточного рахунку."""
        self.score += points
        if self.score > self.best_score:
            self.best_score = int(self.score)
            self._save_best_score()

    def render(self, screen):
        """
        Відображає поточний рахунок та найкращий результат.
        """
        score_text = self.font.render(f"Score: {int(self.score)}", True, self.color)
        best_score_text = self.font.render(f"Best Score: {self.best_score}", True, self.color)
        screen.blit(score_text, (10, 10))  # Поточний рахунок
        screen.blit(best_score_text, (10, 50))  # Найкращий результат