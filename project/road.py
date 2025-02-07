import random

import pygame


class Road:

    def __init__(self):
        self.segments = [{"curve": 0} for _ in range(5)]
        self.offset = 0
        self.turn_timer = 0  # Turn timer
        self.road_color = (35, 20, 55)
        self.lane_mark_color = (242, 102, 150)
        self.horizon_y = 400  # Horizon line a bit below the center
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

    @staticmethod
    def bezier_point(t, p0, p1, p2):
        """Розраховує точку на квадратичній кривій Безьє."""
        return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
                (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1],)

    @staticmethod
    def calculate_control_points(turn_name):
        """
        Returns the control points for the given type of turn.
        """
        control_points = {
            "hard_left": {"left": [(0, 600), (300, 500), (0, 400)], "right": [(800, 600), (600, 400), (150, 400)], },
            "long_left": {"left": [(0, 600), (300, 500), (220, 400)], "right": [(800, 600), (500, 400), (300, 400)], },
            "long_right": {"left": [(0, 600), (300, 400), (500, 400)], "right": [(800, 600), (500, 500), (580, 400)], },
            "hard_right": {"left": [(0, 600), (200, 400), (650, 400)], "right": [(800, 600), (500, 500), (800, 400)], },
            "straight": {"left": [(0, 600), (187, 500), (375, 400)], "right": [(800, 600), (613, 500), (425, 400)], }, }
        return control_points.get(turn_name, control_points["straight"])

    def get_lane_positions(self, depth):
        """
        Calculates lane boundaries for a given depth.
        """
        current_control = self.calculate_control_points(self.current_turn)
        next_control = self.calculate_control_points(self.next_turn)

        # Interpolate control points between current and next turn
        interpolated_left = [
            self.interpolate_points(current_control["left"][i], next_control["left"][i], self.transition_progress) for i
            in range(3)]
        interpolated_right = [
            self.interpolate_points(current_control["right"][i], next_control["right"][i], self.transition_progress) for
            i in range(3)]

        # Calculate Bezier curve points for the given depth
        t = min(depth, 1)
        left_edge = self.bezier_point(t, *interpolated_left)
        right_edge = self.bezier_point(t, *interpolated_right)

        # Calculate lane edges
        road_width = right_edge[0] - left_edge[0]
        total_ratio = 3.2
        lane_ratios = [1, 1.2, 1]

        lane_edges = [left_edge[0]]
        for ratio in lane_ratios:
            lane_edges.append(lane_edges[-1] + road_width * (ratio / total_ratio))

        return lane_edges, left_edge[1]

    @staticmethod
    def interpolate_points(p1, p2, t):
        """
        Interpolates two points `p1` and `p2` by parameter `t`.
        """
        return (1 - t) * p1[0] + t * p2[0], (1 - t) * p1[1] + t * p2[1],

    def update(self, speed, delta_time):
        self.offset += speed / 60

        if self.transition_progress < 1.0:
            self.transition_progress += delta_time / self.transition_duration
        else:
            self.delay_timer += delta_time
            if self.delay_timer >= self.turn_delay:
                self.current_turn = self.next_turn
                self.next_turn = self.generate_turn()
                self.transition_progress = 0.0
                self.delay_timer = 0.0

        if self.offset >= len(self.segments):
            self.offset -= len(self.segments)
            self.segments.append(self.segments.pop(0))  # Rotate segments

    def render(self, screen):
        """
        Draws the road with curved edges using Bezier curves and adds solid lines.
        """
        # Extract control points for the current and next turns
        current_controls = self.calculate_control_points(self.current_turn)
        next_controls = self.calculate_control_points(self.next_turn)

        # Extract left and right control points from the dictionaries
        current_left, current_right = current_controls["left"], current_controls["right"]
        next_left, next_right = next_controls["left"], next_controls["right"]

        # Interpolate control points between current and next turn
        interpolated_left = [
            self.interpolate_points(current_left[i], next_left[i], self.transition_progress) for i in range(3)]
        interpolated_right = [
            self.interpolate_points(current_right[i], next_right[i], self.transition_progress) for i in range(3)]

        # Calculate Bezier curve points for the left and right edges
        num_segments = 50  # Number of segments to draw the road
        left_curve = [self.bezier_point(t / num_segments, *interpolated_left) for t in range(num_segments + 1)]
        right_curve = [self.bezier_point(t / num_segments, *interpolated_right) for t in range(num_segments + 1)]

        # Calculate central curve points for lane dividing lines
        central_curve_left = [(left_curve[i][0] + (right_curve[i][0] - left_curve[i][0]) * 1 / 3,
                               left_curve[i][1] + (right_curve[i][1] - left_curve[i][1]) * 1 / 3,) for i in
                              range(len(left_curve))]

        central_curve_right = [(left_curve[i][0] + (right_curve[i][0] - left_curve[i][0]) * 2 / 3,
                                left_curve[i][1] + (right_curve[i][1] - left_curve[i][1]) * 2 / 3,) for i in
                               range(len(left_curve))]

        for i in range(num_segments):
            pygame.draw.polygon(screen, self.road_color, [left_curve[i],
                                                          left_curve[i + 1],
                                                          right_curve[i + 1],
                                                          right_curve[i],
                                                          ], )

        # Draw dividing lines for lanes
        for i in range(num_segments):
            pygame.draw.line(screen, self.lane_mark_color, central_curve_left[i], central_curve_left[i + 1], 2)
            pygame.draw.line(screen, self.lane_mark_color, central_curve_right[i], central_curve_right[i + 1], 2)
