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
        self.actions = {pygame.K_LEFT: 'left',
                        pygame.K_RIGHT: 'right',
                        pygame.K_UP: 'accelerate',
                        pygame.K_DOWN: 'brake', }
        self.pressed_keys = set()
        self.unpressed_keys = set()
        self.pause_key_pressed: bool = False
        self.pause_key_handled: bool = False  # Space key

    def handle_event(self, event):
        """
        Handles key events
        """
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(event.key)
            if event.key == pygame.K_SPACE:
                self.pause_key_pressed = True
        elif event.type == pygame.KEYUP:
            self.pressed_keys.discard(event.key)
            self.unpressed_keys.add(event.key)
            if event.key == pygame.K_SPACE:
                self.pause_key_pressed = False
                self.pause_key_handled = False

    def is_pause_pressed(self):
        """
        Checks if the Pause button is pressed. Returns TRUE only once
        """
        if self.pause_key_pressed and not self.pause_key_handled:
            self.pause_key_handled = True  # Space is pressed
            return True
        return False


    # @staticmethod
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
        car.isTurningLeft = pygame.K_LEFT in self.pressed_keys
        car.isTurningRight = pygame.K_RIGHT in self.pressed_keys
        car.isStopping = pygame.K_DOWN in self.pressed_keys

        if car.isTurningLeft:
            car.move_left()
        if car.isTurningRight:
            car.move_right()
        if pygame.K_UP in self.pressed_keys:
            car.increase_throttle()
        elif car.isStopping:
            car.decrease_throttle()
        else:
            car.decrease_speed(constants.CAR_INERTIA_FACTOR)
            car.throttle_inertia()
