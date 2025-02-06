import math
import pygame
import os
import constants
from utils.sprite_manager import SpriteManager

class Car:
    '''
    Player car class
    '''
    def __init__(self, sprites, max_speed, mass, max_power, drag_coefficient, frontal_area, wheelbase):
        self.isTurningLeft: bool = False;
        self.isTurningRight: bool = False;
        self.isStopping: bool = False;
        
        self.x: int = constants.CAR_POSITION[0]
        self.y: int = constants.CAR_POSITION[1]
        self.width: int = constants.CAR_SIZE[0];
        self.height: int = constants.CAR_SIZE[1];
        self.current_sprite_frame: int = 0;
        self.sprites: List[pygame.Surface] = sprites;
        self.speed: int = 0 
        self.throttle: int = 0
        self.min_speed: int = 0
        self.max_speed: int = max_speed
        self.target_x: int = self.x  # Car's start position
        self.max_offset: int = 245
        self.road_center: int = constants.CAR_POSITION[0]
        self.font: pygame.Font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 16)

        # Car characteristics
        self.mass: int = mass  # Маса автомобіля в кг
        self.max_power: int = max_power  # Максимальна потужність в Вт
        self.drag_coefficient: float = drag_coefficient
        self.frontal_area: int = frontal_area  # Лобова площа в м²
        self.air_density: float = 1.225  # Густина повітря в кг/м³
        self.wheelbase: int = wheelbase  # Колісна база автомобіля в метрах
        self.steering_angle: int = 0  # Кут повороту керма

    def get_steering_factor(self) -> float:
        '''
        Defines the speed of steering based on car's speed
        '''
        return max(1.5, 2 - abs(self.speed - 200) / 150)  # Максимальна чутливість при 80 км/год

    def get_max_steering_angle(self) -> int:
        '''
        Limits the steering max angle based on the current speed
        '''
        return max(10, 20 - (self.speed / 60))  # При 300 км/год макс кут = 10°

    def with_steering_params(func):
        def wrapper(self, *args, **kwargs):
            steering_factor = self.get_steering_factor()
            max_angle = self.get_max_steering_angle()
            return func(self, steering_factor, max_angle)
        
        return wrapper

    @with_steering_params
    def move_left(self, steering_factor, max_angle):
        self.steering_angle = max(self.steering_angle - steering_factor, -max_angle)

    @with_steering_params
    def move_right(self, steering_factor, max_angle):
        self.steering_angle = min(self.steering_angle + steering_factor, max_angle)

    def reset_steering(self):
        '''
        Turns the steering to its original place if no key is pressed
        '''
        if self.steering_angle > 0:
            self.steering_angle = max(self.steering_angle - 0.81, 0)
        elif self.steering_angle < 0:
            self.steering_angle = min(self.steering_angle + 0.81, 0)

    def update_steering(self):
        '''
        Adds a momentum to cars movement
        '''
        if self.steering_angle > 0:
            self.steering_angle = max(self.steering_angle - 0.1, 0)
        elif self.steering_angle < 0:
            self.steering_angle = min(self.steering_angle + 0.1, 0)


    def update(self, road, delta_time: float):
        '''
        Updates car's state based on road conditions and user input.
        '''
        self._update_speed()
        self._update_position()
        self.apply_road_force(road, delta_time)
        self.reset_steering()

    def render(self, screen):
        '''
        Renders car
        '''
        speed_text = self.font.render(f"Speed: {self.speed:.0f} km/h", True, (255, 255, 255))
        
        self.update_car_sprite()
        screen.blit(self.sprites[int(self.current_sprite_frame // constants.FRAME_FACTOR)], (self.x - self.width, self.y, self.width, self.height));
        screen.blit(speed_text, (10, 580))
        #Uncomment to draw car hitbox
        #pygame.draw.rect(screen, (0, 0, 0), (self.x - self.width // 2, self.y + self.height // 2, self.width, self.height), 1)

    def update_car_sprite(self):
        '''
        Updates car sprites based on the current state
        '''
        
        if (self.isTurningLeft):
            self._animate_turn_left()
        elif (self.isTurningRight):
            self._animate_turn_right()
        elif (self.isStopping):
            self._animate_stop()
        elif (self.speed > 0):
            self._animate_move()
        else:
            self.current_sprite_frame = 0

        if self.speed > 100:
            self.current_sprite_frame += constants.FRAME_STEP
        elif self.speed > 0:
            self.current_sprite_frame += constants.FRAME_STEP_SLOW

    def _animate_turn_left(self):
        if (self.current_sprite_frame + 1 >= 50 or
            self.current_sprite_frame < 35):
            self.current_sprite_frame = 35
    def _animate_turn_right(self):
        if (self.current_sprite_frame + 1 >= 35 or
            self.current_sprite_frame < 20):
            self.current_sprite_frame = 20
    def _animate_move(self):
        if (self.current_sprite_frame + 1 >= 70 or
            self.current_sprite_frame < 55):
            self.current_sprite_frame = 55
    def _animate_stop(self):
        if (self.current_sprite_frame + 1 >= 20):
            self.current_sprite_frame = 0

    def increase_throttle(self):
        '''
        Increases car's throttle (max = 1.0).
        '''
        self.throttle = min(self.throttle + 0.1, 1.0)

    def decrease_throttle(self):
        '''
        Decreases car's throttle (min = 0.0).
        '''
        self.throttle = max(self.throttle - 0.1, 0.0)
        if self.throttle == 0:
            self.decrease_speed(constants.CAR_STOP_FACTOR)

    def decrease_speed(self, speed_factor):
        '''
        Slowly decreases car's speed
        '''
        if self.speed > 0:
            self.speed = max(self.speed - speed_factor, self.min_speed)  # Плавне гальмування

    def throttle_inertia(self):
        '''
        Slowly decreases car's throttle
        '''
        if self.throttle > 0:
            self.throttle = max(self.throttle - 0.05, 0)

    def get_rect(self):
        '''
        Returns car's hitbox
        '''
        return pygame.Rect(self.x - self.width // 2, self.y + self.height // 2, self.width, self.height)

    def apply_road_force(self, road, delta_time):
        '''
        Road impact on a car movement
        '''
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
        '''
        Updates car's speed based on throttle level & physics
        '''
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
            self.decrease_speed(constants.CAR_INERTIA_FACTOR)

    def _update_position(self):
        '''
        Updates car's position based on turn's type
        '''
        if abs(self.steering_angle) > 0:
            radius = self.wheelbase / math.tan(math.radians(self.steering_angle))
            angular_velocity = (self.speed / 3.6) / radius  # Радіани в секунду
            self.x += angular_velocity * radius * math.sin(math.radians(self.steering_angle))

        self.x = max(self.road_center - self.max_offset, min(self.x, self.road_center + self.max_offset))


class Ferrari458Italia(Car):
    def __init__(self):
        carSprites = SpriteManager.get_frame_sequence('car_full.png', 64, 24, 4);
        super().__init__(carSprites, max_speed=324, mass=1100, max_power=352000, drag_coefficient=0.34, frontal_area=1.9,
                        wheelbase=2.45)
