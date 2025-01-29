import os
import pygame


class ScoreBoard:
    """
    Клас для відображення таблиці найкращих результатів.
    """
    def __init__(self, file_path="scoreboard.txt"):
        self.file_path = file_path
        self.top_scores = self._load_scores()
        self.font = pygame.font.Font(None, 36)  # Шрифт для тексту
        self.color = (255, 255, 255)  # Колір тексту

    def _load_scores(self):
        """
        Завантажує найкращі результати з файлу.
        """
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r") as file:
            scores = [int(line.strip()) for line in file.readlines()]
        return sorted(scores, reverse=True)[:5]  # Топ-5 результатів

    def _save_scores(self):
        """
        Зберігає найкращі результати у файл.
        """
        with open(self.file_path, "w") as file:
            for score in self.top_scores:
                file.write(f"{score}\n")

    def add_score(self, score):
        """
        Додає новий результат і оновлює таблицю.
        """
        self.top_scores.append(score)
        self.top_scores = sorted(self.top_scores, reverse=True)[:5]
        self._save_scores()

    def render(self, screen):
        """
        Відображає таблицю найкращих результатів на екрані.
        """
        screen.fill((0, 0, 0))  # Чорний фон
        title = self.font.render("ScoreBoard", True, self.color)
        screen.blit(title, (200, 50))  # Заголовок

        for i, score in enumerate(self.top_scores):
            text = self.font.render(f"{i + 1}. {score}", True, self.color)
            screen.blit(text, (200, 100 + i * 40))  # Відображення кожного результату
