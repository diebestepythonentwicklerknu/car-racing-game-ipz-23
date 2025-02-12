import pygame

from constants import *


class Camera:
    def __init__(self):
        self.camera_offset_x = 0
        self.mode = "road"  # Початковий режим камери

    def update(self, car):
        if self.mode == "road":
            # Камера залишається в центрі дороги
            self.camera_offset_x = 0

        elif self.mode == "car":
            # Камера слідкує за автомобілем
            self.camera_offset_x = car.road_offset_x + SCREEN_WIDTH // 2
            car.x = SCREEN_WIDTH // 2


    def switch_mode(self, car):
        if self.mode == "road":
            car.road_offset_x = -car.x
            self.mode = "car"
        else:
            car.x = -car.road_offset_x
            self.mode = "road"
