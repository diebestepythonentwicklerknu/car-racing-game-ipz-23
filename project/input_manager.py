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
            pygame.K_DOWN: 'brake',
        }
        self.pressed_keys = set()
        self.pause_key_pressed = False
        self.pause_key_handled = False  # Для обробки натискання Space один раз

    def handle_event(self, event):
        """
        Обробляє події натискання та відпускання клавіш.
        """
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(event.key)
            if event.key == pygame.K_SPACE:
                self.pause_key_pressed = True
        elif event.type == pygame.KEYUP:
            self.pressed_keys.discard(event.key)
            if event.key == pygame.K_SPACE:
                self.pause_key_pressed = False
                self.pause_key_handled = False  # Дозволяємо повторну обробку Space

    def is_pause_pressed(self):
        """
        Перевіряє, чи натиснуто кнопку паузи, і повертає True лише один раз.
        """
        if self.pause_key_pressed and not self.pause_key_handled:
            self.pause_key_handled = True  # Вказуємо, що Space вже оброблено
            return True
        return False

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
