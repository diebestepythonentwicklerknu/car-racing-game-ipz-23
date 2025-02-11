import pygame

from constants import *


class Camera:
    def __init__(self):
        self.camera_offset_x = 0
        self.mode = "road"  # Початковий режим камери

    def update(self, car, road):
        if self.mode == "road":
            # Камера залишається в центрі дороги
            self.camera_offset_x = 0
        elif self.mode == "car":
            # Камера слідкує за автомобілем
            self.camera_offset_x = -car.x + SCREEN_WIDTH // 2

    def switch_mode(self):
        if self.mode == "road":
            self.mode = "car"
        else:
            self.mode = "road"
