import os

import pygame

from constants import SCREEN_WIDTH, BUTTON_WIDTH, BUTTON_HEIGHT
from scoreboard import ScoreBoard
from utils.sprite_manager import SpriteManager


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.nickname = None
        pygame.display.set_caption("Menu")
        self.background = SpriteManager.load_image("main_menu.png")
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 16)

        # Fix : added Scoreboard button
        self.buttons = [
            {"text": "Play as Guest", "action": "guest",
             "rect": pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT)},
            {"text": "Login", "action": "nickname",
             "rect": pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, 360, BUTTON_WIDTH, BUTTON_HEIGHT)},
            {"text": "ScoreBoard", "action": "scoreboard",
             "rect": pygame.Rect((SCREEN_WIDTH - 250) // 2, 420, BUTTON_WIDTH, BUTTON_HEIGHT)},
            {"text": "Quit", "action": "quit",
             "rect": pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, 480, BUTTON_WIDTH, BUTTON_HEIGHT)}
        ]

        # # Миготіння тексту
        # self.title_color = (255, 255, 0)  # Жовтий
        # self.title_blink = True
        # self.blink_timer = 0

    def render(self):
        """
        Відображає меню в стилі ретро.
        """
        self.screen.blit(self.background, (0, 0))  # Малюємо фон

        # Відображаємо заголовок з миготінням
        # title_text = self.title_font.render("RETRO RACING", True, self.title_color)
        # self.screen.blit(
        #     title_text,
        #     (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 15, 100)
        # )

        # Малюємо кнопки
        for button in self.buttons:
            pygame.draw.rect(self.screen, (0, 0, 0), button["rect"])
            pygame.draw.rect(self.screen, (255, 255, 255), button["rect"], 3)  # Білий контур навколо кнопки
            text = self.font.render(button["text"], True, (255, 255, 255))
            text_x = button["rect"].x + (button["rect"].width - text.get_width()) // 2  # Текст по центру кнопки
            text_y = button["rect"].y + (button["rect"].height - text.get_height()) // 2
            self.screen.blit(text, (text_x, text_y))

    def handle_event(self, event):
        """
        Обробляє натискання кнопок у меню.
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    if button["action"] == "guest":
                        self.running = False  # Guest mode
                    elif button["action"] == "nickname":
                        self.enter_nickname()
                    elif button["action"] == "quit":
                        pygame.quit()
                        exit()
                    elif button["action"] == "scoreboard":
                        self.show_scoreboard()

    def enter_nickname(self):
        """Дозволяє користувачеві ввести нікнейм перед грою."""
        nickname = ""
        font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 24)

        while True:
            self.screen.fill((0, 0, 0))
            prompt = font.render("Enter your nickname:", True, (255, 255, 255))
            self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 200))

            nickname_surface = font.render(nickname, True, (255, 255, 0))
            self.screen.blit(nickname_surface, (SCREEN_WIDTH // 2 - nickname_surface.get_width() // 2, 250))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and nickname.strip():
                        self.running = False
                        self.nickname = nickname.strip()  # Зберігаємо нікнейм для гри
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    elif event.unicode.isalnum():
                        nickname += event.unicode

    def show_scoreboard(self):
        """Показує топ-10 гравців"""
        scoreboard = ScoreBoard()
        top_scores = scoreboard.get_top_scores()

        font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 24)
        back_button = pygame.Rect(250, 500, 300, 50)

        while True:
            self.screen.fill((0, 0, 0))
            title = font.render("Scoreboard", True, (255, 255, 255))
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

            y_offset = 120
            for i, (name, score) in enumerate(top_scores):
                text = font.render(f"{i + 1}. {name}: {score}", True, (255, 255, 0))
                self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
                y_offset += 40

            pygame.draw.rect(self.screen, (255, 0, 0), back_button)
            back_text = font.render("Back", True, (255, 255, 255))
            self.screen.blit(back_text, (back_button.x + 100, back_button.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        return

    # def update(self):
    #     """
    #     Оновлює стан меню (міготіння тексту).
    #     """
    #     self.blink_timer += 1
    #     if self.blink_timer % 100 == 0:  # Миготіння кожні 100 кадрів
    #         self.title_blink = not self.title_blink
    #         self.title_color = (255, 255, 0) if self.title_blink else (255, 0, 0)

    def run(self):
        """
        Основний цикл меню.
        """
        if self.nickname is None:
            self.nickname = "Guest"

        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            # self.update()
            self.render()
            pygame.display.flip()
