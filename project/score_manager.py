import os

import pygame


class ScoreManager:
    """
    Class for managing the score of the player.
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE_PATH = os.path.join(BASE_DIR, "best_score.txt")

    def __init__(self):
        """
        Initializes the score manager components
        """
        self.score = 0.0
        self.best_score = 0
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 20)
        self.color = (255, 255, 255)

        # Завантаження найкращого результату з файлу
        self._load_best_score()

    def _load_best_score(self):
        """
        Loads the best score from the file.
        """
        try:
            with open(self.FILE_PATH, "r") as file:
                self.best_score = int(file.read().strip())
        except FileNotFoundError:
            print("File with best score not found. Setting value to 0.")
            self.best_score = 0
        except ValueError:
            print("File with best score is corrupted. Setting value to 0.")
            self.best_score = 0

    def _save_best_score(self):
        """
        Saves the best score to a file.
        """
        try:
            with open(self.FILE_PATH, "w") as file:
                file.write(str(self.best_score))
        except IOError as e:
            print(f"Write to file error: {e}")

    def update(self, car_speed, car_max_speed):
        """
        Updates the score based on the car speed and distance ridden.
        """
        score_increase = (car_speed / car_max_speed) * 0.5
        score_increase = max(0.01, score_increase)

        self.score += score_increase
        if self.score > self.best_score:
            self.best_score = int(self.score)
            self._save_best_score()

    def add_score(self, points):
        """
        Add fixed amount of points to the score.
        """
        self.score += points
        if self.score > self.best_score:
            self.best_score = int(self.score)
            self._save_best_score()

    def render(self, screen):
        """
        Render the current score and the best score on the screen.
        """
        score_text = self.font.render(f"Score: {int(self.score)}", True, self.color)
        best_score_text = self.font.render(f"Best Score: {self.best_score}", True, self.color)
        screen.blit(score_text, (10, 10))  # Current score
        screen.blit(best_score_text, (10, 50))  # Best score
