import pygame


class InputManager:
    """
    Клас для управління ввідними подіями
    """

    def __init__(self):
        self.actions = {
            pygame.K_LEFT: 'left',
            pygame.K_RIGHT: 'right',
            pygame.K_UP: 'accelerate',
            pygame.K_DOWN: 'brake'
        }
        self.pressed_keys = set()

    def handle_event(self, event):
        """
        Обробляє події натискання та відпускання клавіш.
        """
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            self.pressed_keys.discard(event.key)

    def update_car(self, car):
        """
        Оновлює стан автомобіля на основі натиснутих клавіш.
        """
        if pygame.K_LEFT in self.pressed_keys:
            car.move_left()
        if pygame.K_RIGHT in self.pressed_keys:
            car.move_right()
        if pygame.K_UP in self.pressed_keys:
            car.increase_throttle()
        elif pygame.K_DOWN in self.pressed_keys:
            car.decrease_throttle()
        else:
            car.apply_inertia()
            car.throttle_inertia()


