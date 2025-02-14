import os
import pygame
import constants

class Tutorial:
    def __init__(self, screen):
        """
        Initializes the tutorial screen.
        """
        self.__screen = screen
        self.__font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 18)
        self.__back_button = pygame.Rect(constants.SCREEN_WIDTH // 2 - 100, 500, 200, 50)

        self.__tutorial_text = [
            "Controls:",
            "↑ : Accelerate",
            "↓ : Break",
            "← → : Left/Right turn",
            "-------------------------------------------",
            "C : Change camera view",
            "Space : Pause",
            "Mouse click : Interact"
        ]


    def show(self):
        """
        Displays the tutorial screen with game controls information.
        """
        while True:
            self.__screen.fill((0, 0, 0))

            title = self.__font.render("Tutorial", True, (255, 255, 255))
            self.__screen.blit(title, (constants.SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

            y_offset = 150
            for line in self.__tutorial_text:
                text = self.__font.render(line, True, (255, 255, 0))
                self.__screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
                y_offset += 40

            pygame.draw.rect(self.__screen, (255, 0, 0), self.__back_button)
            back_text = self.__font.render("Back", True, (255, 255, 255))
            self.__screen.blit(back_text, (self.__back_button.x + 65, self.__back_button.y + 15))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.__back_button.collidepoint(event.pos):
                        return  # Exit tutorial and go back to menu
    
