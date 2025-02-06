import os
import pygame

from car import Ferrari458Italia
import constants
from input_manager import InputManager
from menu import Menu
from obstacle_manager import ObstacleManager
from parallax_manager import ParallaxManager
from road import Road
from score_manager import ScoreManager
from scoreboard import ScoreBoard
from utils.sprite_manager import SpriteManager

'''
Main game-scenario class
'''
class Game:

    '''
    Initialization of the game
    '''
    def __init__(self, nickname=None):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Racing")
        self.clock = pygame.time.Clock()
        self.running: bool = True
        self.paused: bool = False  
        self.game_over: bool = False  
        self.nickname: str = nickname  
        self.camera_offset_x: int = 0  
        self._initialize_game_components()

    '''
    Initialization of the game components
    '''
    def _initialize_game_components(self):
        sky_sprite = pygame.transform.scale(SpriteManager.load_image('sky.png'), (800, 550))
        hills_sprites = [
            pygame.transform.scale(SpriteManager.load_image('hills_l.png'), (800, 400)),
            pygame.transform.scale(SpriteManager.load_image('hills_r.png'), (800, 400)),
        ]
        tree_sprites = SpriteManager.get_frame_sequence('tree-Sheet.png', 64, 96, 2)
        grass_sprites = SpriteManager.get_frame_sequence('grass-Sheet.png', 300, 200, 3)
        
        self.car = Ferrari458Italia()
        self.road: Road = Road()
        self.obstacle_manager: ObstacleManager= ObstacleManager()
        self.input_manager: InputManager = InputManager()
        self.score_manager: ScoreManager = ScoreManager()
        self.parallax_manager: ParallaxManager = ParallaxManager(grass_sprites, tree_sprites, hills_sprites, sky_sprite)
        self.scoreboard: ScoreBoard = ScoreBoard()  


    '''
    Handling of the game events
    Processing pressed keys
    '''    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif self.game_over:  # If game is over, wait for R(restart) or Q(quit) to be pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game() 
                    elif event.key == pygame.K_q:
                        self.go_to_main_menu()
            else:
                self.input_manager.handle_event(event)

        if not self.game_over and self.input_manager.is_pause_pressed():
            self.paused = not self.paused

    '''
    Updating the paralax, obstacles, road and car states
    '''
    def update(self):
        if self.game_over or self.paused:
            return

        delta_time = self.clock.get_time() / 1000
        self.input_manager.update_car(self.car)
        self.car.update(self.road, delta_time)

        if self.car.speed != 0:  # FIX: if the speed is set to 0, than do not update parallax & score
            self.road.update(self.car.speed, delta_time)
            self.parallax_manager.update(self.screen, self.car.speed, self.road)

            if self.obstacle_manager.update(self.car, self.road, self.score_manager, self.car.speed):
                pygame.time.delay(100)
                self.show_game_over_screen()

            self.score_manager.update(self.car.speed, self.car.max_speed)

    '''
    Rendering all the game components
    '''
    def render(self):
        if self.game_over:
            self.show_game_over_message()  # Show game over screen
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
            self.screen.blit(pause_text, (constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 - 50))

    '''
    Running the game
    Main game loop
    '''
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(constants.FPS)

        if self.nickname:
            self.scoreboard.update_score(self.nickname, int(self.score_manager.score))
        pygame.quit()

    '''
    Defines isGameOver flag and awaits R or Q to be pressed 
    '''
    def show_game_over_screen(self):
        self.game_over = True


    '''
    Renders game over screen
    '''
    def show_game_over_message(self):
        self.screen.fill((0, 0, 0))  
        font = pygame.font.Font(os.path.join(os.path.dirname(__file__),
                                             "assets", "PressStart2P-Regular.ttf"), 30)
        text1 = font.render("Game Over!", True, (255, 0, 0))
        text2 = font.render("Press R to Restart", True, (255, 255, 255))
        text3 = font.render("Press Q for Menu", True, (255, 255, 255))
        
        center = (constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2)
        

        self.screen.blit(text1, (center[0] - 150, center[1] - 100))
        self.screen.blit(text2, (center[0] - 250, center[1]))
        self.screen.blit(text3, (center[0] - 230, center[1] + 50))

    '''
    Resets game without going back to the menu
    '''
    def restart_game(self):
        self._initialize_game_components()
        self.game_over = False

    '''
    Goes back to the menu after game is over
    '''
    def go_to_main_menu(self):
        self.scoreboard.update_score(self.nickname, self.score_manager.score)  

        menu = Menu(self.screen)
        menu.run()

        if menu.nickname and menu.nickname != "Guest":
            self.__init__(menu.nickname)
            self.run()
        else:
            self.__init__("Guest")
            self.run()