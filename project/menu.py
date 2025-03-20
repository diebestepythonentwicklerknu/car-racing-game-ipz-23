import sys
import os
import pygame
import constants
from scoreboard import ScoreBoard
from utils.sprite_manager import SpriteManager
from tutorial import Tutorial

'''
Menu class renders and handles the main menu
'''


class Menu:
    def __init__(self, screen):
        """
        Initialization of the menu components
        """
        self.__screen = screen
        self.__running: bool = True
        self.nickname: str = ""
        pygame.display.set_caption("Menu")
        self.__background = SpriteManager.load_image("main_menu.png")
        self.__font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"),
                                       16)

        button_position = (constants.SCREEN_WIDTH - constants.BUTTON_WIDTH) // 2
        tutorial_position = (constants.SCREEN_WIDTH - constants.BUTTON_WIDTH) // 0.75
        self.__buttons = [{"text": "Play as Guest", "action": "guest",
                           "rect": pygame.Rect(button_position, 300, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)},
                          {"text": "Login", "action": "nickname",
                           "rect": pygame.Rect(button_position, 360, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)},
                          {"text": "ScoreBoard", "action": "scoreboard",
                           "rect": pygame.Rect(button_position, 420, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)},
                          {"text": "Quit", "action": "quit",
                           "rect": pygame.Rect(button_position, 480, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)},
                          {"text": "?", "action": "tutorial",
                           "rect": pygame.Rect(tutorial_position, 20, constants.T_SQUARE_BUTTON_SIZE,
                                               constants.T_SQUARE_BUTTON_SIZE)}]

        # Constants for music (probably should be in different place)
        self.volume = 0.05
        self.slider_rect = pygame.Rect(60, constants.SCREEN_HEIGHT - 48, 100, 6)
        self.slider_handle_radius = 8

    def render(self):
        """
        Renders buttons
        """
        self.__screen.blit(self.__background, (0, 0))

        # Draw buttons
        for button in self.__buttons:
            BACKGROUND_COLOR = (35, 20, 55)
            BORDER_COLOR = (242, 102, 150)
            TEXT_COLOR = (242, 102, 150)

            pygame.draw.rect(self.__screen, BACKGROUND_COLOR, button["rect"])
            pygame.draw.rect(self.__screen, BORDER_COLOR, button["rect"], 3)
            text = self.__font.render(button["text"], True, TEXT_COLOR)

            text_x = button["rect"].x + (button["rect"].width - text.get_width()) // 2  # Text centering
            text_y = button["rect"].y + (button["rect"].height - text.get_height()) // 2
            self.__screen.blit(text, (text_x, text_y))

        # Draw sound icon
        self.sound_icon = pygame.image.load(os.path.join("assets", "sprites", "sound_icon.png"))
        self.sound_icon = pygame.transform.scale(self.sound_icon, (30, 30))
        self.__screen.blit(self.sound_icon, (self.slider_rect.x - 45, self.slider_rect.y - 13))

        # Draw sound slider (primitive one)
        slider_handle_x = self.slider_rect.x + self.volume * self.slider_rect.width
        slider_handle_y = self.slider_rect.y + self.slider_rect.height // 2
        pygame.draw.rect(self.__screen, (200, 200, 200), self.slider_rect)
        pygame.draw.circle(self.__screen, (202, 62, 110), (slider_handle_x, slider_handle_y), self.slider_handle_radius)

    def handle_event(self, event):
        """
        Handles menu key pressing
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.__buttons:
                if button["rect"].collidepoint(event.pos):
                    if button["action"] == "guest":
                        self.__running = False  # Guest mode
                    elif button["action"] == "nickname":
                        self.enter_nickname()
                    elif button["action"] == "quit":
                        pygame.quit()
                        sys.exit()
                    elif button["action"] == "scoreboard":
                        self.show_scoreboard()
                    elif button["action"] == "tutorial":
                        tutorial = Tutorial(self.__screen)
                        tutorial.show()
            # Перевіряємо, чи натиснуто на повзунок для зміни гучності
            if self.slider_rect.collidepoint(event.pos):
                self.volume = (event.pos[0] - self.slider_rect.x) / self.slider_rect.width  # Обчислюємо нову гучність
                self.volume = max(0.0, min(self.volume, 1.0))  # Переконуємося, що гучність в межах 0-1
                pygame.mixer.music.set_volume(self.volume)  # Змінюємо гучність

        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:  # Якщо натиснута ліва кнопка миші
                if self.slider_rect.collidepoint(event.pos):  # Якщо мишка над повзунком
                    self.volume = (event.pos[0] - self.slider_rect.x) / self.slider_rect.width
                    self.volume = max(0.0, min(self.volume, 1.0))  # Обмежуємо гучність від 0 до 1
                    pygame.mixer.music.set_volume(self.volume)  # Змінюємо гучність

    def enter_nickname(self):
        """
        Gets users nickname
        """
        nickname = ""
        font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 24)

        while True:
            self.__screen.fill((0, 0, 0))
            prompt = font.render("Enter your nickname:", True, (255, 255, 255))
            self.__screen.blit(prompt, (constants.SCREEN_WIDTH // 2 - prompt.get_width() // 2, 200))

            nickname_surface = font.render(nickname, True, (255, 255, 0))
            self.__screen.blit(nickname_surface, (constants.SCREEN_WIDTH // 2 - nickname_surface.get_width() // 2, 250))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and nickname.strip():
                        self.__running = False
                        self.nickname = nickname.strip()  # Saving nickname
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    elif event.unicode.isalnum():
                        nickname += event.unicode

    def show_scoreboard(self):
        """
        Shows TOP 10 of the players
        """
        scoreboard = ScoreBoard()
        top_scores = scoreboard.get_top_scores()

        font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 24)
        back_button = pygame.Rect(250, 500, 300, 50)

        while True:
            self.__screen.fill((0, 0, 0))
            title = font.render("Scoreboard", True, (255, 255, 255))
            self.__screen.blit(title, (constants.SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

            y_offset = 120
            for i, (name, score) in enumerate(top_scores):
                text = font.render(f"{i + 1}. {name}: {score}", True, (255, 255, 0))
                self.__screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
                y_offset += 40

            pygame.draw.rect(self.__screen, (255, 0, 0), back_button)
            back_text = font.render("Back", True, (255, 255, 255))
            self.__screen.blit(back_text, (back_button.x + 100, back_button.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        return

    def run(self):
        """
        Game cycle
        """
        if self.nickname is None:
            self.nickname = "Guest"

        while self.__running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.render()
            pygame.display.flip()
