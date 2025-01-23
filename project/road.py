import random

import pygame

from project.constants import SCREEN_HEIGHT, ROAD_HORIZON_Y


class Road:

    def __init__(self):
        self.segments = [{"curve": 0} for _ in range(5)]
        self.offset = 0
        self.turn_timer = 0  # Turn timer
        self.road_color = (50, 50, 50)
        self.lane_mark_color = (255, 255, 255)
        self.horizon_y = 400  # Позиція горизонту (нижче середини екрану)
        self.transition_progress = 0.0
        self.transition_duration = 5.0
        self.turn_delay = 5.0
        self.delay_timer = 0
        self.current_turn = "straight"
        self.next_turn = "straight"

    @staticmethod
    def generate_turn():
        """
        Randomly generates a turn type
        :return: (turn_name, curve_value)
        """
        turn_types = ["straight", "long_left", "long_right", "hard_left", "hard_right"]
        return random.choice(turn_types)

    def get_lane_positions(self, depth):
        """
        Calculates lane boundaries for a given depth.
        """
        # Отримання координат лівої та правої меж дороги
        current_left, current_right = self.get_control_points(self.current_turn)
        next_left, next_right = self.get_control_points(self.next_turn)

        # Інтерполяція контрольних точок
        interpolated_left = [
            self.interpolate_points(current_left[i], next_left[i], self.transition_progress)
            for i in range(3)
        ]
        interpolated_right = [
            self.interpolate_points(current_right[i], next_right[i], self.transition_progress)
            for i in range(3)
        ]

        # Розрахунок позицій для заданої глибини за допомогою кривих Безьє
        def bezier_point(t, p0, p1, p2):
            """Розрахунок точки на квадратичній кривій Безьє."""
            return (
                (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
                (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1],
            )

        t = min(depth, 1)  # Переконатися, що t в межах [0, 1]
        left_edge = bezier_point(t, *interpolated_left)
        right_edge = bezier_point(t, *interpolated_right)

        # Ширина дороги
        road_width = right_edge[0] - left_edge[0]

        # Пропорції ширини для кожної смуги
        total_ratio = 3.2  # Ліва (1) + Центральна (1.2) + Права (1)
        lane_ratios = [1, 1.2, 1]  # Відносна ширина кожної смуги

        # Розрахунок меж смуг
        lane_edges = [left_edge[0]]
        for ratio in lane_ratios:
            lane_edges.append(lane_edges[-1] + road_width * (ratio / total_ratio))

        return lane_edges, left_edge[1]

    def get_y_position(self, depth):
        """
        Повертає координату `y` для об'єкта на основі глибини.
        """
        horizon_y = self.horizon_y
        bottom_y = 600
        return bottom_y - (bottom_y - horizon_y) * min(depth, 1)

    def update(self, speed, delta_time):
        self.offset += speed / 60

        if self.transition_progress < 1.0:
            self.transition_progress += delta_time / self.transition_duration
        else:
            self.delay_timer += delta_time
            if self.delay_timer >= self.turn_delay:
                self.current_turn = self.next_turn
                print(f"Current Turn: {self.current_turn}")
                self.next_turn = self.generate_turn()
                print(f"Next Turn: {self.next_turn}")
                self.transition_progress = 0.0
                self.delay_timer = 0.0

        if self.offset >= len(self.segments):
            self.offset -= len(self.segments)
            self.segments.append(self.segments.pop(0))  # Rotate segments

    @staticmethod
    def get_control_points(turn_name):
        """
        Повертає опорні точки для даного типу повороту.
        """
        if turn_name == "hard_left":
            left_start = (0, 600)
            left_control = (300, 500)
            left_end = (0, 400)
            right_start = (800, 600)
            right_control = (600, 400)
            right_end = (150, 400)

        elif turn_name == "long_left":
            left_start = (0, 600)
            left_control = (300, 500)
            left_end = (220, 400)
            right_start = (800, 600)
            right_control = (500, 400)
            right_end = (350, 400)

        elif turn_name == "long_right":
            left_start = (0, 600)
            left_control = (300, 400)
            left_end = (450, 400)
            right_start = (800, 600)
            right_control = (500, 500)
            right_end = (580, 400)

        elif turn_name == "hard_right":
            left_start = (0, 600)
            left_control = (200, 400)
            left_end = (650, 400)
            right_start = (800, 600)
            right_control = (500, 500)
            right_end = (800, 400)

        else:
            left_start = (0, 600)
            left_control = (187, 500)
            left_end = (375, 400)
            right_start = (800, 600)
            right_control = (613, 500)
            right_end = (425, 400)

        return (left_start, left_control, left_end), (right_start, right_control, right_end)

    @staticmethod
    def interpolate_points(p1, p2, t):
        """
        Інтерполює дві точки `p1` і `p2` за параметром `t`.
        """
        return (1 - t) * p1[0] + t * p2[0], (1 - t) * p1[1] + t * p2[1],

    def render(self, screen):
        """
        Малює дорогу з вигнутими межами, використовуючи криві Безьє, та додає суцільні лінії.
        """
        current_left, current_right = self.get_control_points(self.current_turn)
        next_left, next_right = self.get_control_points(self.next_turn)

        # Інтерполяція між контрольними точками
        interpolated_left = [
            self.interpolate_points(current_left[i], next_left[i], self.transition_progress) for i in range(3)]
        interpolated_right = [
            self.interpolate_points(current_right[i], next_right[i], self.transition_progress) for i in range(3)]

        # Інтерполяція точок кривих Безьє
        def bezier_point(t, p0, p1, p2):
            """Розраховує точку на квадратичній кривій Безьє."""
            return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1],)

        # Розрахунок точок для лівої та правої меж
        num_segments = 50  # Кількість точок на кривій для плавності
        left_curve = [bezier_point(t / num_segments, *interpolated_left) for t in range(num_segments + 1)]
        right_curve = [bezier_point(t / num_segments, *interpolated_right) for t in range(num_segments + 1)]

        # Розрахунок точок для центральних ліній (розділових смуг)
        central_curve_left = [
            (
                left_curve[i][0] + (right_curve[i][0] - left_curve[i][0]) * 1 / 3,
                left_curve[i][1] + (right_curve[i][1] - left_curve[i][1]) * 1 / 3,
            )
            for i in range(len(left_curve))
        ]

        central_curve_right = [
            (
                left_curve[i][0] + (right_curve[i][0] - left_curve[i][0]) * 2 / 3,
                left_curve[i][1] + (right_curve[i][1] - left_curve[i][1]) * 2 / 3,
            )
            for i in range(len(left_curve))
        ]

        # Draw road
        for i in range(num_segments):
            pygame.draw.polygon(screen, self.road_color, [
                left_curve[i],  # Ліва нижня точка
                left_curve[i + 1],  # Ліва верхня точка
                right_curve[i + 1],  # Права верхня точка
                right_curve[i],  # Права нижня точка
            ], )


        # Draw dividing lines for lanes
        for i in range(num_segments):
            pygame.draw.line(screen, self.lane_mark_color, central_curve_left[i], central_curve_left[i + 1], 2)
            pygame.draw.line(screen, self.lane_mark_color, central_curve_right[i], central_curve_right[i + 1], 2)