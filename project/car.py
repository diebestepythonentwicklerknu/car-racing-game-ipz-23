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

    def __init__(self, sprites, max_speed, mass, max_power, drag_coefficient, frontal_area, wheelbase):
        self.isTurningLeft: bool = False
        self.isTurningRight: bool = False
        self.isStopping: bool = False

        self.x: int = constants.CAR_POSITION[0]
        self.y: int = constants.CAR_POSITION[1]
        self.width: int = constants.CAR_SIZE[0]
        self.height: int = constants.CAR_SIZE[1]
        self.current_sprite_frame: int = 0
        self.sprites = sprites
        self.speed: int = 0
        self.throttle: int = 0
        self.min_speed: int = 0
        self.max_speed: int = max_speed
        self.target_x: int = self.x  # Car's start position
        self.max_offset: int = 245
        self.road_center: int = constants.CAR_POSITION[0]
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 16)
        self.camera = Camera()

        # Car characteristics
        self.mass: int = mass  # In kg
        self.max_power: int = max_power  # In watts
        self.drag_coefficient: float = drag_coefficient
        self.frontal_area: int = frontal_area  # In m²
        self.air_density: float = 1.225  # In kg/m³
        self.wheelbase: int = wheelbase  # In meters
        self.steering_angle: int = 0  # In degrees

    def get_steering_factor(self) -> float:
        """
        Defines the speed of steering based on car's speed
        """
        return max(1.5, 2 - abs(self.speed - 200) / 150)  # Max sensitivity at 200 km/h

    def get_max_steering_angle(self) -> int:
        """
        Limits the steering max angle based on the current speed
        """
        return max(10, int(20 - (self.speed / 60)))  # Max angle at 300 km/h = 10°

    @staticmethod
    def with_steering_params(func):
        def wrapper(self):
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
        """
        Turns the steering to its original place if no key is pressed
        """
        if self.steering_angle > 0:
            self.steering_angle = max(self.steering_angle - 0.81, 0)
        elif self.steering_angle < 0:
            self.steering_angle = min(self.steering_angle + 0.81, 0)

    def update_steering(self):
        """
        Adds a momentum to cars movement
        """
        if self.steering_angle > 0:
            self.steering_angle = max(self.steering_angle - 0.1, 0)
        elif self.steering_angle < 0:
            self.steering_angle = min(self.steering_angle + 0.1, 0)

    def update(self, road, delta_time, camera):
        """
        Updates car's state based on road conditions and user input.
        """
        self._update_speed()
        self._update_position(camera)
        self.apply_road_force(road, delta_time)
        self.reset_steering()

    def render(self, screen):
        """
        Renders car
        """
        speed_text = self.font.render(f"Speed: {self.speed:.0f} km/h", True, (255, 255, 255))

        self.update_car_sprite()
        screen.blit(self.sprites[int(self.current_sprite_frame // constants.FRAME_FACTOR)],
                    (self.x - self.width, self.y, self.width, self.height))
        screen.blit(speed_text, (10, 580))

        # Uncomment to draw car hitbox
        # pygame.draw.rect(screen, (0, 0, 0),
        # (self.x - self.width // 2, self.y + self.height // 2, self.width, self.height), 1)

    def update_car_sprite(self):
        """
        Updates car sprites based on the current state
        """

        if self.isTurningLeft:
            self._animate_turn_left()
        elif self.isTurningRight:
            self._animate_turn_right()
        elif self.isStopping:
            self._animate_stop()
        elif self.speed > 0:
            self._animate_move()
        else:
            self.current_sprite_frame = 0

        if self.speed > 100:
            self.current_sprite_frame += constants.FRAME_STEP
        elif self.speed > 0:
            self.current_sprite_frame += constants.FRAME_STEP_SLOW

    def _animate_turn_left(self):
        if self.current_sprite_frame + 1 >= 50 or self.current_sprite_frame < 35:
            self.current_sprite_frame = 35

    def _animate_turn_right(self):
        if self.current_sprite_frame + 1 >= 35 or self.current_sprite_frame < 20:
            self.current_sprite_frame = 20

    def _animate_move(self):
        if self.current_sprite_frame + 1 >= 70 or self.current_sprite_frame < 55:
            self.current_sprite_frame = 55

    def _animate_stop(self):
        if self.current_sprite_frame + 1 >= 20:
            self.current_sprite_frame = 0

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
        return pygame.Rect(self.x - self.width // 2, self.y + self.height // 2, self.width, self.height)

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
        self.road_offset_x = min(-(self.road_center - self.max_offset), max(self.road_offset_x, -(self.road_center + self.max_offset)))

    def _update_speed(self):
        """
        Updates car's speed based on throttle level & physics
        """
        if self.speed > 0 or self.throttle > 0:
            # Drag force calculation based on diffrerent factors
            drag_force = 0.5 * self.drag_coefficient * self.air_density * self.frontal_area * (self.speed / 3.6) ** 2

            # Limit the drag force to the car's power
            max_force = ((self.max_power * self.throttle)
                         / max(self.speed / 3.6, 1e-6)) if self.speed > 0 else self.max_power * self.throttle

            # Net force calculation
            net_force = max(0, int(max_force - drag_force))

            # Acceleration calculation
            acceleration = net_force / self.mass

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
        if abs(self.steering_angle) > 0:
            radius = self.wheelbase / math.tan(math.radians(self.steering_angle))
            angular_velocity = (self.speed / 3.6) / radius  # Radians per second
            self.x += angular_velocity * radius * math.sin(math.radians(self.steering_angle))
            self.road_offset_x -= (angular_velocity * radius * math.sin(math.radians(self.steering_angle)))

        self.x = max(self.road_center - self.max_offset, min(self.x, self.road_center + self.max_offset))
        self.road_offset_x = min(-(self.road_center - self.max_offset), max(self.road_offset_x, -(self.road_center + self.max_offset)))

class Ferrari458Italia(Car):
    def __init__(self):
        car_sprites = SpriteManager.get_frame_sequence('car_full.png', 64, 24, 4)
        super().__init__(car_sprites, max_speed=324, mass=1100, max_power=352000, drag_coefficient=0.34,
                         frontal_area=1.9, wheelbase=2.45)
