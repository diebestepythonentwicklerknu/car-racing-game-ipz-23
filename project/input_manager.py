import pygame
import constants

class InputManager:
    '''
    An interface to manage user inputs 
    '''

    def __init__(self):
        self.actions = {pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right', pygame.K_UP: 'accelerate',
                        pygame.K_DOWN: 'brake', }
        self.pressed_keys = set()
        self.unpressed_keys = set()
        self.pause_key_pressed: bool = False
        self.pause_key_handled: bool = False  # Для обробки натискання Space один раз

    def handle_event(self, event):
        '''
        Handles key events
        '''
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(event.key)
            if event.key == pygame.K_SPACE:
                self.pause_key_pressed = True
        elif event.type == pygame.KEYUP:
            self.pressed_keys.discard(event.key)
            self.unpressed_keys.add(event.key)
            if event.key == pygame.K_SPACE:
                self.pause_key_pressed = False
                self.pause_key_handled = False  # Дозволяємо повторну обробку Space

    def is_pause_pressed(self):
        '''
        Checks if the Pause button is pressed. Returns TRUE only once 
        '''
        if self.pause_key_pressed and not self.pause_key_handled:
            self.pause_key_handled = True  # Space вже оброблено
            return True
        return False

    def update_car(self, car):
        '''
        Updates car state based on pressed keys
        '''
        if pygame.K_LEFT in self.pressed_keys:
            car.move_left()
            car.isTurningLeft = True
        else:
            car.isTurningLeft = False

        if pygame.K_RIGHT in self.pressed_keys:
            car.move_right()
            car.isTurningRight = True
        else:
            car.isTurningRight = False

        if pygame.K_UP in self.pressed_keys:
            car.increase_throttle()
        elif pygame.K_DOWN in self.pressed_keys:
            car.decrease_throttle()
            car.isStopping = True
        else:
            car.decrease_speed(constants.CAR_INERTIA_FACTOR)
            car.throttle_inertia()
            car.isStopping = False
