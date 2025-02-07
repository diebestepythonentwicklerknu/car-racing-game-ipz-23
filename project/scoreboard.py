import os


class ScoreBoard:
    """
    Class for managing the scoreboard.
    Stores and shows the best scores of the players.
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE_PATH = os.path.join(BASE_DIR, "players_scoreboard.txt")

    def __init__(self):
        self.scores = self.load_scores()

    def load_scores(self):
        """
        Loads the scores from the file.
        """
        scores = {}

        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 2 and parts[1].isdigit():  # Check if the line is valid (format)
                        nickname, score = parts[0], int(parts[1])
                        scores[nickname] = score
        else:
            open(self.FILE_PATH, "w").close()

        return scores

    def save_scores(self):
        """
        Saves updated scores to the file.
        """
        with open(self.FILE_PATH, "w", encoding="utf-8") as file:
            for nickname, score in self.scores.items():
                file.write(f"{nickname} {score}\n")

    def update_score(self, nickname, score):
        """
        Updates the best score of the player.
        If the player is not in the scoreboard, adds him.
        """
        rounded_score = round(score)

        if nickname != "Guest":  # If played without nickname, don't save the score
            if nickname in self.scores:
                if score > self.scores[nickname]:
                    self.scores[nickname] = rounded_score
            else:
                self.scores[nickname] = rounded_score

            self.save_scores()

    def get_top_scores(self, top_n=10):
        """
        Returns the top n scores for the scoreboard.
        """
        return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
