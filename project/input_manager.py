import pygame
import constants


class InputManager:
    """
    An interface to manage user inputs
    """

    def __init__(self):
        """
        Initializes the input manager components
        """
        self.__actions = {pygame.K_LEFT: 'left',
                        pygame.K_RIGHT: 'right',
                        pygame.K_UP: 'accelerate',
                        pygame.K_DOWN: 'brake', }
        self.__pressed_keys = set()
        self.__unpressed_keys = set()
        self.__pause_key_pressed: bool = False
        self.__pause_key_handled: bool = False  # Space key

    def handle_event(self, event):
        """
        Handles key events
        """
        if event.type == pygame.KEYDOWN:
            self.__pressed_keys.add(event.key)
            if event.key == pygame.K_SPACE:
                self.__pause_key_pressed = True
        elif event.type == pygame.KEYUP:
            self.__pressed_keys.discard(event.key)
            self.__unpressed_keys.add(event.key)
            if event.key == pygame.K_SPACE:
                self.__pause_key_pressed = False
                self.__pause_key_handled = False

    def is_pause_pressed(self):
        """
        Checks if the Pause button is pressed. Returns TRUE only once
        """
        if self.__pause_key_pressed and not self.__pause_key_handled:
            self.__pause_key_handled = True  # Space is pressed
            return True
        return False


    @staticmethod
    def handle_pause(func):
        """
        Decorator to pause the game
        """

        def wrapper(self, *args, **kwargs):
            if self.is_pause_pressed():
                return
            return func(self, *args, **kwargs)

        return wrapper

    @handle_pause
    def update_car(self, car):
        """ Оновлює стан автомобіля на основі введених даних """
        car.is_turning_left = pygame.K_LEFT in self.__pressed_keys
        car.is_turning_right = pygame.K_RIGHT in self.__pressed_keys
        car.is_stopping = pygame.K_DOWN in self.__pressed_keys

        if car.is_turning_left:
            car.move_left()
        if car.is_turning_right:
            car.move_right()
        if pygame.K_UP in self.__pressed_keys:
            car.increase_throttle()
        elif car.is_stopping:
            car.decrease_throttle()
        else:
            car.decrease_speed(constants.CAR_INERTIA_FACTOR)
            car.throttle_inertia()
