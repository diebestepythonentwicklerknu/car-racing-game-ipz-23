import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import os


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        pygame.display.set_caption("Menu")

        # Завантаження ретро-фону з файлу (в каталозі проєкту)
        self.background = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "1_retro_background.png"))
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Завантаження ретро-шрифту аналогічно
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 40)
        self.title_font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 36)

        # Кнопки (Поки 2, коли буде скорборд - додамо ще для цього)
        self.buttons = [
            {"text": "Start", "action": "start", "rect": pygame.Rect(250, 300, 300, 50)},
            {"text": "Quit", "action": "quit", "rect": pygame.Rect(250, 400, 300, 50)}
        ]

        # Миготіння тексту
        self.title_color = (255, 255, 0)  # Жовтий
        self.title_blink = True
        self.blink_timer = 0

    def render(self):
        """
        Відображає меню в стилі ретро.
        """
        self.screen.blit(self.background, (0, 0))  # Малюємо фон

        # Відображаємо заголовок з миготінням
        title_text = self.title_font.render("RETRO RACING", True, self.title_color)
        self.screen.blit(
            title_text,
            (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 15, 100)
        )

        # Малюємо кнопки
        for button in self.buttons:

            #  button_rect = button["rect"].move(50, 0)
            pygame.draw.rect(self.screen, (0, 0, 0), button["rect"])  # Чорний фон
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Ліва кнопка миші
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["action"] == "start":
                            self.running = False  # Вихід з меню, початок гри
                        elif button["action"] == "quit":
                            pygame.quit()
                            exit()

    def update(self):
        """
        Оновлює стан меню (міготіння тексту).
        """
        self.blink_timer += 1
        if self.blink_timer % 100 == 0:  # Миготіння кожні 100 кадрів
            self.title_blink = not self.title_blink
            self.title_color = (255, 255, 0) if self.title_blink else (255, 0, 0)

    def run(self):
        """
        Основний цикл меню.
        """
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.update()
            self.render()
            pygame.display.flip()
