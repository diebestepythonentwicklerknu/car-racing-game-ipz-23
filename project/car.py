import math

import pygame

from constants import SCREEN_WIDTH


class Car:
    """
    Клас автомобіля
    """

    def __init__(self, max_speed, mass, max_power, drag_coefficient, frontal_area, wheelbase):
        self.x = SCREEN_WIDTH // 2  # Початкове положення по горизонталі
        self.y = 500  # Початкове положення по вертикалі
        self.width = 120
        self.height = 60
        self.color = (255, 0, 0)  # Колір автомобіля
        self.speed = 0  # Початкова швидкість
        self.throttle = 0  # Рівень натискання газу (0.0 - 1.0)
        self.min_speed = 0
        self.max_speed = max_speed
        self.target_x = self.x  # Позиція, до якої автомобіль рухається
        self.max_offset = 245  # Максимальна відстань, на яку можна повернути
        self.road_center = SCREEN_WIDTH // 2
        self.font = pygame.font.Font(None, 26)

        # Фізичні параметри
        self.mass = mass  # Маса автомобіля в кг
        self.max_power = max_power  # Максимальна потужність в Вт
        self.drag_coefficient = drag_coefficient
        self.frontal_area = frontal_area  # Лобова площа в м²
        self.air_density = 1.225  # Густина повітря в кг/м³
        self.wheelbase = wheelbase  # Колісна база автомобіля в метрах
        self.steering_angle = 0  # Кут повороту керма

    def get_steering_factor(self):
        """
        Визначає, наскільки швидко повертається кермо залежно від швидкості.
        На середніх швидкостях (50-100 км/год) повороти найшвидші.
        """
        return max(1.5, 2 - abs(self.speed - 200) / 150)  # Максимальна чутливість при 80 км/год

    def get_max_steering_angle(self):
        """
        Обмежує кут повороту залежно від швидкості (understeering).
        """
        return max(10, 20 - (self.speed / 60))  # При 300 км/год макс кут = 10°

    def move_left(self):
        """
        Плавний поворот вліво із обмеженням кута повороту.
        """
        steering_factor = self.get_steering_factor()
        max_angle = self.get_max_steering_angle()
        self.steering_angle = max(self.steering_angle - steering_factor, -max_angle)

    def move_right(self):
        """
        Плавний поворот вправо із обмеженням кута повороту.
        """
        steering_factor = self.get_steering_factor()
        max_angle = self.get_max_steering_angle()
        self.steering_angle = min(self.steering_angle + steering_factor, max_angle)

    def reset_steering(self):
        """
        Повертає кермо в початкове положення, коли клавіші не натиснуті.
        """
        if self.steering_angle > 0:
            self.steering_angle = max(self.steering_angle - 0.81, 0)
        elif self.steering_angle < 0:
            self.steering_angle = min(self.steering_angle + 0.81, 0)

    def update_steering(self):
        """
        Додає інерцію: кермо не змінює напрямок миттєво.
        """
        if self.steering_angle > 0:
            self.steering_angle = max(self.steering_angle - 0.1, 0)
        elif self.steering_angle < 0:
            self.steering_angle = min(self.steering_angle + 0.1, 0)

    def update(self, road, delta_time):
        """
        Оновлення стану автомобіля.
        """
        self._update_speed()
        self._update_position()
        self.apply_road_force(road, delta_time)
        self.reset_steering()

    def render(self, screen):
        """
        Малює автомобіль на екрані.
        """
        italic_font = self.font
        italic_font.set_italic(True)
        speed_text = italic_font.render(f"Speed: {self.speed:.0f} km/h", True, (102, 10, 5))

        outline_color = (255, 255, 255)
        outline_positions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for offset in outline_positions:
            outline_text = italic_font.render(f"Speed: {self.speed:.0f} km/h", True, outline_color)
            screen.blit(outline_text, (10 + offset[0], 580 + offset[1]))

        screen.blit(speed_text, (10, 580))
        pygame.draw.rect(screen, self.color, (self.x - self.width // 2, self.y, self.width, self.height))

    def increase_throttle(self):
        """
        Збільшує газ до максимуму (1.0).
        """
        self.throttle = min(self.throttle + 0.1, 1.0)

    def decrease_throttle(self):
        """
        Зменшує газ до мінімуму (0.0).
        """
        self.throttle = max(self.throttle - 0.1, 0.0)
        if self.throttle == 0:
            self.decrease_speed()

    def decrease_speed(self):
        """
        Зменшує швидкість.
        """
        if self.speed > 0:
            self.speed = max(self.speed - 0.5, self.min_speed)  # Плавне гальмування

    def apply_inertia(self):
        """
        Сповільнення через інерцію при відсутності натискання клавіш.
        """
        if self.speed > 0:
            self.speed = max(self.speed - 0.05, 0)  # Плавне сповільнення

    def throttle_inertia(self):
        """Інерція педалі газу (скидання обертів)"""
        if self.throttle > 0:
            self.throttle = max(self.throttle - 0.05, 0)

    def get_rect(self):
        """
        Повертає прямокутник автомобіля для перевірки зіткнень.
        """
        return pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)

    def apply_road_force(self, road, delta_time):
        """
        Вплив дороги на автомобіль залежно від типу повороту.
        """
        # Визначення сили впливу для кожного типу повороту
        turn_effect = {"straight": 0,  # Без зміщення
                       "long_left": 0.4,  # Легкий вплив вправо
                       "long_right": -0.4,  # Легкий вплив вліво
                       "hard_left": 0.8,  # Сильний вплив вправо
                       "hard_right": -0.8  # Сильний вплив вліво
                       }

        # Отримання сили впливу повороту
        force_multiplier = turn_effect.get(road.next_turn, 0)

        # Розрахунок зміщення залежно від швидкості та часу
        force = force_multiplier * self.speed * delta_time

        # Зміщення автомобіля
        self.x += force

        # Обмеження в межах дороги
        self.x = max(self.road_center - self.max_offset, min(self.x, self.road_center + self.max_offset))

    def _update_speed(self):
        """
        Оновлює швидкість автомобіля на основі фізичних законів та рівня газу.
        """
        if self.speed > 0 or self.throttle > 0:
            # Обчислення сили аеродинамічного опору
            drag_force = 0.5 * self.drag_coefficient * self.air_density * self.frontal_area * (self.speed / 3.6) ** 2

            # Обмеження максимальної тяги двигуна
            max_force = ((self.max_power * self.throttle) /
                         max(self.speed / 3.6, 1e-6)) if self.speed > 0 else self.max_power * self.throttle

            # Чиста сила для прискорення
            net_force = max(0, max_force - drag_force)

            # Обчислення прискорення
            acceleration = net_force / self.mass

            # Оновлення швидкості автомобіля
            self.speed += acceleration * (1 / 60) * 3.6

            # Обмеження швидкості максимальним значенням
            self.speed = max(self.min_speed, min(self.speed, self.max_speed))

        # Повільне зменшення швидкості, якщо газ не натиснутий
        if self.throttle == 0 and self.speed > 0:
            self.apply_inertia()

    def _update_position(self):
        """
        Оновлює положення автомобіля з урахуванням повороту.
        """
        if abs(self.steering_angle) > 0:
            radius = self.wheelbase / math.tan(math.radians(self.steering_angle))
            angular_velocity = (self.speed / 3.6) / radius  # Радіани в секунду
            self.x += angular_velocity * radius * math.sin(math.radians(self.steering_angle))

        self.x = max(self.road_center - self.max_offset, min(self.x, self.road_center + self.max_offset))


class LamborghiniDiablo(Car):
    def __init__(self):
        super().__init__(max_speed=322, mass=1576, max_power=367000, drag_coefficient=0.31, frontal_area=2.0,
                         wheelbase=2.65)
        self.color = (255, 215, 0)  # Жовтий Lamborghini


class FerrariF40(Car):
    def __init__(self):
        super().__init__(max_speed=324, mass=1100, max_power=352000, drag_coefficient=0.34, frontal_area=1.9,
                         wheelbase=2.45)
        self.color = (255, 0, 0)  # Червоний Ferrari
