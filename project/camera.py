from project.constants import SCREEN_WIDTH


class Camera:
    def __init__(self):
        self.camera_offset_x = 0
        self.mode = "road"

    def update(self, car):
        if self.mode == "road":
            self.camera_offset_x = 0

        elif self.mode == "car":
            self.camera_offset_x = car.road_offset_x + SCREEN_WIDTH // 2
            car.x = SCREEN_WIDTH // 2

    def switch_mode(self, car):
        if self.mode == "road":
            car.road_offset_x = -car.x
            self.mode = "car"
        else:
            car.x = -car.road_offset_x
            self.mode = "road"

        def get_position(self):
            """Returns the current camera position."""
            return self.camera_offset_x, 0
