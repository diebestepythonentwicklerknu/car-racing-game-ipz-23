import os

class ScoreBoard:
    FILE_PATH = os.path.join(os.path.dirname(__file__), "players_scoreboard.txt")

    def __init__(self):
        self.scores = self.load_scores()

    def load_scores(self):
        """
        Завантажує результати з текстового файлу або створює новий файл
        """
        scores = {}

        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 2 and parts[1].isdigit():  # Перевірка правильного формату
                        nickname, score = parts[0], int(parts[1])
                        scores[nickname] = score
        else:
            open(self.FILE_PATH, "w").close()

        return scores

    def save_scores(self):
        """
        Зберігає оновлені результати у текстовий файл.
        """
        with open(self.FILE_PATH, "w", encoding="utf-8") as file:
            for nickname, score in self.scores.items():
                file.write(f"{nickname} {score}\n")


    def update_score(self, nickname, score):
        """
        Оновлює найкращий результат гравця, якщо новий результат більший.
        Якщо гравця ще немає в таблиці, додає його.
        """
        if nickname != "Guest":  # Гравці без нікнейму не зберігаються
            if nickname in self.scores:
                if score > self.scores[nickname]:  
                    self.scores[nickname] = score
            else:
                self.scores[nickname] = score  

            self.save_scores()

    def get_top_scores(self, top_n=10):
        """Повертає список топ-N найкращих результатів."""
        return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
