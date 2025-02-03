import pygame
import os

from car import LamborghiniDiablo
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from input_manager import InputManager
from parallax_manager import ParallaxManager
from obstacle_manager import ObstacleManager  
from road import Road
from score_manager import ScoreManager
from scoreboard import ScoreBoard  
from menu import Menu


class Game:
    def __init__(self, nickname=None):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racing")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False  
        self.game_over = False  # FIX: Додаємо флаг для екрану завершення гри
        self.nickname = nickname  
        self.camera_offset_x = 0  
        self._initialize_game_components()

    def _initialize_game_components(self):
        self.car = LamborghiniDiablo()
        self.car.speed = 0
        self.road = Road()
        self.obstacle_manager = ObstacleManager()
        self.input_manager = InputManager()
        self.score_manager = ScoreManager()
        self.parallax_manager = ParallaxManager()
        self.scoreboard = ScoreBoard()  
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif self.game_over:  # Якщо гра закінчена, перевіряємо натискання R або Q
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()  # R for restart Q for quit
                    elif event.key == pygame.K_q:
                        self.go_to_main_menu()  
            else:
                self.input_manager.handle_event(event)

        if not self.game_over and self.input_manager.is_pause_pressed():
            self.paused = not self.paused

    def update(self):
        if self.game_over or self.paused:  
            return  

        delta_time = self.clock.get_time() / 1000
        self.input_manager.update_car(self.car)
        self.car.update(self.road, delta_time)

        if self.car.speed != 0:  
            self.road.update(self.car.speed, delta_time)
            self.parallax_manager.update(self.car.speed, self.road)

            if self.obstacle_manager.update(self.car, self.road, self.score_manager, self.car.speed):
                pygame.time.delay(100)  
                self.show_game_over_screen()
            
            self.score_manager.update()
                
    def render(self):
        if self.game_over:
            self.show_game_over_message()  # FIX: Відображаємо екран завершення гри
        elif not self.paused:  
            self.screen.fill((100, 200, 255))  
            self.parallax_manager.render(self.screen)
            self.road.render(self.screen)
            self.obstacle_manager.render(self.screen, self.road)
            self.car.render(self.screen)
            self.score_manager.render(self.screen)
        else:  
            pause_font = pygame.font.Font(os.path.join(os.path.dirname(__file__),
                                                       "assets", "PressStart2P-Regular.ttf"), 40)
            pause_text = pause_font.render("Paused", True, (255, 255, 255))
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(FPS)

        if self.nickname:  
            self.scoreboard.update_score(self.nickname, self.score_manager.score) 
        pygame.quit()

    def show_game_over_screen(self):
        """ 
        Встановлює флаг завершення гри і очікує натискання R або Q 
        """
        self.game_over = True

    def show_game_over_message(self):
        """ 
        Малює екран завершення гри 
        """
        self.screen.fill((0, 0, 0))  
        font = pygame.font.Font(os.path.join(os.path.dirname(__file__),
                                             "assets", "PressStart2P-Regular.ttf"), 30)
        text1 = font.render("Game Over!", True, (255, 0, 0))
        text2 = font.render("Press R to Restart", True, (255, 255, 255))
        text3 = font.render("Press Q for Menu", True, (255, 255, 255))

        self.screen.blit(text1, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(text2, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2))
        self.screen.blit(text3, (SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 + 50))

    def restart_game(self):
        """ 
        Скидає гру без виходу в головне меню
        """
        self._initialize_game_components()
        self.game_over = False  

    def go_to_main_menu(self):
        """
        Повертає в меню після завершення гри
        """
        self.scoreboard.update_score(self.nickname, self.score_manager.score)  

        menu = Menu(self.screen)  
        menu.run() 

        if menu.nickname and menu.nickname != "Guest":
            self.__init__(menu.nickname)  
            self.run()
        else:
            self.__init__("Guest")  
            self.run()

        

        