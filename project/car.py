import math
import os

import pygame

import constants
from camera import Camera
from utils.sprite_manager import SpriteManager


class Car:
    """
    Player car class
    """

    def __init__(self, sprites, max_speed,
                 mass, max_power, drag_coefficient,
                 frontal_area, wheelbase):
        self.is_turning_left: bool = False
        self.is_turning_right: bool = False
        self.is_stopping: bool = False

        self.x: int = constants.CAR_POSITION[0]
        self.y: int = constants.CAR_POSITION[1]
        self.__width: int = constants.CAR_SIZE[0]
        self.__height: int = constants.CAR_SIZE[1]
        self.__current_sprite_frame: int = 0
        self.__sprites = sprites
        self.speed: int = 0
        self.throttle: int = 0
        self.min_speed: int = 0
        self.max_speed: int = max_speed
        self.target_x: int = self.x  # Car's start position
        self.max_offset: int = 245
        self.road_center: int = constants.CAR_POSITION[0]
        self.road_offset_x: int = 0
        self.__font = pygame.font.Font(
            os.path.join(constants.ASSETS_DIR, "PressStart2P-Regular.ttf"), 16)
        self.camera = Camera()

        # Car characteristics
        self.__mass: int = mass  # In kg
        self.__max_power: int = max_power  # In watts
        self.__drag_coefficient: float = drag_coefficient
        self.__frontal_area: int = frontal_area  # In m²
        self.__air_density: float = 1.225  # In kg/m³
        self.__wheelbase: int = wheelbase  # In meters
        self.__steering_angle: int = 0  # In degrees

    def __get_steering_factor(self) -> float:
        """
        Defines the speed of steering based on car's speed
        """
        return max(1.5, 2 - abs(self.speed - 200) / 150)  # Max sensitivity at 200 km/h

    def __get_max_steering_angle(self) -> int:
        """
        Limits the steering max angle based on the current speed
        """
        return max(10, int(20 - (self.speed / 60)))  # Max angle at 300 km/h = 10°

    # @staticmethod
    def with_steering_params(func):
        def wrapper(self):
            steering_factor = self.__get_steering_factor()
            max_angle = self.__get_max_steering_angle()
            return func(self, steering_factor, max_angle)

        return wrapper

    @with_steering_params
    def move_left(self, steering_factor, max_angle):
        self.__steering_angle = max(self.__steering_angle - steering_factor, -max_angle)

    @with_steering_params
    def move_right(self, steering_factor, max_angle):
        self.__steering_angle = min(self.__steering_angle + steering_factor, max_angle)

    def _reset_steering(self):
        """
        Turns the steering to its original place if no key is pressed
        """
        if self.__steering_angle > 0:
            self.__steering_angle = max(self.__steering_angle - 0.81, 0)
        elif self.__steering_angle < 0:
            self.__steering_angle = min(self.__steering_angle + 0.81, 0)

    def _update_steering(self):
        """
        Adds a momentum to cars movement
        """
        if self.__steering_angle > 0:
            self.__steering_angle = max(self.__steering_angle - 0.1, 0)
        elif self.__steering_angle < 0:
            self.__steering_angle = min(self.__steering_angle + 0.1, 0)

    def update(self, road, delta_time, camera):
        """
        Updates car's state based on road conditions and user input.
        """
        self._update_speed()
        self._update_position(camera)
        self.apply_road_force(road, delta_time)
        self._reset_steering()

    def render(self, screen):
        """
        Renders car
        """
        speed_text = self.__font.render(f"Speed: {self.speed:.0f} km/h", True, (255, 255, 255))

        self._update_car_sprite()
        screen.blit(self.__sprites[int(self.__current_sprite_frame // constants.FRAME_FACTOR)],
                    (self.x - self.__width, self.y, self.__width, self.__height))
        screen.blit(speed_text, (10, 580))

        # Uncomment to draw car hitbox
        # pygame.draw.rect(screen, (0, 0, 0),
        # (self.x - self.width // 2, self.y + self.height // 2, self.width, self.height), 1)

    def _update_car_sprite(self):
        """
        Updates car sprites based on the current state
        """

        if self.is_turning_left:
            self.__animate_turn_left()
        elif self.is_turning_right:
            self.__animate_turn_right()
        elif self.is_stopping:
            self.__animate_stop()
        elif self.speed > 0:
            self.__animate_move()
        else:
            self.__current_sprite_frame = 0

        if self.speed > 100:
            self.__current_sprite_frame += constants.FRAME_STEP
        elif self.speed > 0:
            self.__current_sprite_frame += constants.FRAME_STEP_SLOW

    def __animate_turn_left(self):
        if self.__current_sprite_frame + 1 >= 50 or self.__current_sprite_frame < 35:
            self.__current_sprite_frame = 35

    def __animate_turn_right(self):
        if self.__current_sprite_frame + 1 >= 35 or self.__current_sprite_frame < 20:
            self.__current_sprite_frame = 20

    def __animate_move(self):
        if self.__current_sprite_frame + 1 >= 70 or self.__current_sprite_frame < 55:
            self.__current_sprite_frame = 55

    def __animate_stop(self):
        if self.__current_sprite_frame + 1 >= 20:
            self.__current_sprite_frame = 0

    def increase_throttle(self):
        """
        Increases car's throttle (max = 1.0).
        """
        self.throttle = min(self.throttle + 0.1, 1.0)

    def decrease_throttle(self):
        """
        Decreases car's throttle (min = 0.0).
        """
        self.throttle = max(self.throttle - 0.1, 0.0)
        if self.throttle == 0:
            self.decrease_speed(constants.CAR_STOP_FACTOR)

    def decrease_speed(self, speed_factor):
        """
        Slowly decreases car's speed
        """
        if self.speed > 0:
            self.speed = max(self.speed - speed_factor, self.min_speed)  # Slow breaking

    def throttle_inertia(self):
        """
        Slowly decreases car's throttle
        """
        if self.throttle > 0:
            self.throttle = max(self.throttle - 0.05, 0)

    def get_rect(self):
        """
        Returns car's hitbox
        """
        return pygame.Rect(
            self.x - self.__width // 2,
            self.y + self.__height // 2,
            self.__width, self.__height)

    def apply_road_force(self, road, delta_time):
        """
        Road impact on a car movement
        """
        # Defines the road-force impact on the car's movement
        turn_effect = {"straight": 0,  # Without any impact
                       "long_left": 0.4,  # Slight impact to the right
                       "long_right": -0.4,  # Slight impact to the left
                       "hard_left": 0.8,  # Strong impact to the right
                       "hard_right": -0.8  # Strong impact to the left
                       }

        # Get the road's impact on the car's turns
        force_multiplier = turn_effect.get(road.next_turn, 0)

        # Calculate the force based on speed and time
        force = force_multiplier * self.speed * delta_time

        # Apply the force to the car's position
        self.x += force
        self.road_offset_x -= force

        # Limit the car's position to the road's width
        self.x = max(self.road_center - self.max_offset, min(self.x, self.road_center + self.max_offset))
        self.road_offset_x = \
            min(-(self.road_center - self.max_offset),
                max(self.road_offset_x, -(self.road_center + self.max_offset)))

    def _update_speed(self):
        """
        Updates car's speed based on throttle level & physics
        """
        if self.speed > 0 or self.throttle > 0:
            # Drag force calculation based on diffrerent factors
            drag_force = (0.5 * self.__drag_coefficient *
                          self.__air_density * self.__frontal_area * (
                                  self.speed / 3.6) ** 2)

            # Limit the drag force to the car's power
            max_force = ((self.__max_power * self.throttle)
                         / max(self.speed / 3.6, 1e-6)) if self.speed > 0 else self.__max_power * self.throttle

            # Net force calculation
            net_force = max(0, int(max_force - drag_force))

            # Acceleration calculation
            acceleration = net_force / self.__mass

            # Speed update
            self.speed += acceleration * (1 / 60) * 3.6

            # Speed limits
            self.speed = max(self.min_speed, min(self.speed, self.max_speed))

        # Slight decrease in speed if no throttle is applied
        if self.throttle == 0 and self.speed > 0:
            self.decrease_speed(constants.CAR_INERTIA_FACTOR)

    def _update_position(self, camera):
        """
        Updates car's position based on turn's type
        """
        if abs(self.__steering_angle) > 0:
            radius = self.__wheelbase / math.tan(math.radians(self.__steering_angle))
            angular_velocity = (self.speed / 3.6) / radius  # Radians per second
            self.x += angular_velocity * radius * math.sin(math.radians(self.__steering_angle))
            self.road_offset_x -= (angular_velocity * radius * math.sin(math.radians(self.__steering_angle)))

        self.x = max(self.road_center - self.max_offset, min(self.x, self.road_center + self.max_offset))
        self.road_offset_x = min(-(self.road_center - self.max_offset),
                                 max(self.road_offset_x, -(self.road_center + self.max_offset)))


class Ferrari458Italia(Car):
    def __init__(self):
        car_sprites = SpriteManager.get_frame_sequence('car_full.png', 64, 24, 4)
        super().__init__(car_sprites, max_speed=324, mass=1100, max_power=352000, drag_coefficient=0.34,
                         frontal_area=1.9, wheelbase=2.45)
