import pygame


class Road:
    def __init__(self):
        self.segments = [{"curve": 0} for _ in range(25)]
        self.offset = 0
        self.road_color = (50, 50, 50)
        self.lane_mark_color = (255, 255, 255)
        self.horizon_y = 400  # Позиція горизонту (нижче середини екрану)

    def get_lane_positions(self, depth):
        """
        Обчислює межі смуг для заданої глибини.
        """
        road_bottom_width = 750
        road_top_width = 10
        total_ratio = 3.2  # Ліва (1) + Центральна (1.2) + Права (1)
        lane_ratios = [1, 1.2, 1]  # Відносна ширина смуг

        # Ширина дороги на заданій глибині
        width = road_bottom_width * (1 - min(depth, 1)) + road_top_width * max(depth - 1, 0)

        # Ширина кожної смуги
        lane_widths = [width * (r / total_ratio) for r in lane_ratios]

        # Межі смуг
        center_y = self.get_y_position(depth)  # Вертикальна координата
        start_x = 400 - width // 2
        lane_edges = [start_x]
        for lane_width in lane_widths:
            lane_edges.append(lane_edges[-1] + lane_width)

        return lane_edges, center_y

    def get_y_position(self, depth):
        """
        Повертає координату `y` для об'єкта на основі глибини.
        """
        horizon_y = self.horizon_y
        bottom_y = 600
        return bottom_y - (bottom_y - horizon_y) * min(depth, 1)

    def update(self, speed):
        self.offset += speed / 60
        if self.offset >= len(self.segments):
            self.offset -= len(self.segments)

    def render(self, screen):
        """
        Малює дорогу з перспективою.
        """
        center = 400  # Центр екрана
        road_bottom_width = 750
        road_top_width = 50  # Початкова ширина дороги
        segment_height = 8  # Висота кожного сегмента дороги

        for i in range(len(self.segments)):
            # Обчислюємо координати верхнього і нижнього країв трапеції
            depth = i / len(self.segments)  # Відносна глибина сегмента
            bottom_width = road_bottom_width * (1 - depth) + road_top_width * depth
            top_width = road_bottom_width * (1 - (depth + 1 / len(self.segments))) + road_top_width * (
                        depth + 1 / len(self.segments))

            y_bottom = 600 - i * segment_height
            y_top = y_bottom - segment_height

            # Якщо сегмент вийшов за межі горизонту, не малюємо його
            if y_top < self.horizon_y:
                break

            # Малюємо трапецію для сегмента
            pygame.draw.polygon(screen, self.road_color,
                                [(center - bottom_width // 2, y_bottom), (center + bottom_width // 2, y_bottom),
                                    (center + top_width // 2, y_top), (center - top_width // 2, y_top), ])

            # Кількість смуг і відносна ширина центральної
            lanes = 3
            central_lane_ratio = 1.2  # Центральна смуга на 20% ширша

            # Вираховуємо ширину кожної смуги
            total_ratio = central_lane_ratio + (lanes - 1)  # 1.2 (центральна) + 1 (ліва) + 1 (права)
            lane_ratios = [1, central_lane_ratio, 1]  # Ліва, центральна, права
            lane_widths_bottom = [bottom_width * (r / total_ratio) for r in lane_ratios]
            lane_widths_top = [top_width * (r / total_ratio) for r in lane_ratios]

            # Вираховуємо межі смуг (знизу і зверху)
            lane_edges_bottom = [center - bottom_width // 2]
            lane_edges_top = [center - top_width // 2]
            for i in range(lanes):
                lane_edges_bottom.append(lane_edges_bottom[-1] + lane_widths_bottom[i])
                lane_edges_top.append(lane_edges_top[-1] + lane_widths_top[i])

            # Малюємо кожну смугу дороги
            for i in range(lanes):
                pygame.draw.polygon(screen, self.road_color,
                                    [(lane_edges_bottom[i], y_bottom), (lane_edges_bottom[i + 1], y_bottom),
                                        (lane_edges_top[i + 1], y_top), (lane_edges_top[i], y_top)])

            # Малюємо суцільні лінії між смугами
            for i in range(1, lanes):
                pygame.draw.line(screen, self.lane_mark_color, (lane_edges_bottom[i], y_bottom),
                                 (lane_edges_top[i], y_top), 2)
