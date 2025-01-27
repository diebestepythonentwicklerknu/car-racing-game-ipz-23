import pygame
import random
import time
import os


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.near_obstacles = set()
        self.messages = []
        

    def update(self, player, road, score_manager):
        """
        Оновлює позицію перешкод.
        """
        collision_detected = False
        player_rect = player.get_rect()
        for obstacle in self.obstacles:
            obstacle.update()

            if obstacle.get_reduced_rect(road).colliderect(player.get_rect()):
                collision_detected = True
            
            # Якщо гравець робить близький обгін, додати 1000 очок
            # Використовує ширший хітбокс для обгону
            if obstacle not in self.near_obstacles:
                if obstacle.get_increased_rect(road).colliderect(player.get_rect()):
                    self.near_obstacles.add(obstacle)
                    score_manager.add_score(1000)

                    self.messages.append({
                        "text": "+1000 points!",
                        "time": time.time(),  # Store the current time
                        "position": (player_rect.centerx, player_rect.top - 20)  # Above the player
                    })
                    

        # Видалення перешкод
        self.obstacles = [o for o in self.obstacles if o.depth > 0.3]
        self.near_obstacles = {o for o in self.near_obstacles if o in self.obstacles}

        # Генерація перешкод
        if random.random() < 0.01:
            lane = random.randint(0, 2)
            self.obstacles.append(Obstacle(lane))

        return collision_detected

    def check_collision(self, player, road):
        """
        Перевіряє, чи є зіткнення між гравцем і будь-якою перешкодою. 
        """
        for obstacle in self.obstacles:
            if obstacle.get_rect(road).colliderect(player.get_rect()):
                return True
        return False

    def render(self, screen, road):
        """
        Малює всі перешкоди.
        """
        for obstacle in self.obstacles:
            obstacle.render(screen, road)

        # Малює повідомлення про бонусні очки
        current_time = time.time()
        for message in self.messages[:]:
            if current_time - message["time"] <= 1:  # Відображає повідомлення протягом 1 секунди
                message_font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "PressStart2P-Regular.ttf"), 20)
                text_surface = message_font.render(message["text"], True, (255, 255, 0))
                screen.blit(text_surface, message["position"])
            else:
                self.messages.remove(message)  # Видаляє повідомлення після закінчення часу (1 секунда)


class Obstacle:
    def __init__(self, lane):
        self.lane = lane
        self.depth = 1  # Початкова глибина (горизонт)
        self.color = (0, 255, 0)  # Зелений колір перешкоди

    def update(self):
        """
        Оновлює глибину перешкоди для наближення.
        """
        self.depth -= 0.006  # Чим ближче до гравця, тим менша глибина
        if self.depth <= 0.1:
            self.depth = 0

    def get_rect(self, road):
        """
        Обчислює позицію і розмір перешкоди на основі перспективи.
        """
        lane_edges, y = road.get_lane_positions(self.depth)
        width = max((lane_edges[self.lane + 1] - lane_edges[self.lane]) * 0.8, 15)
        height = width / 2  # Пропорційна висота
        x = (lane_edges[self.lane] + lane_edges[self.lane + 1]) // 2
        return pygame.Rect(x - width // 2, y - height, width, height)

    def get_reduced_rect(self, road):
        """
        Обчислення хітбоксу, меншого за візуал
        :param road:
        :return:
        """
        rect = self.get_rect(road)
        reduced_width = rect.width // 2
        reduced_height = rect.height // 2
        return pygame.Rect(
            rect.x + rect.width // 4,
            rect.y + rect.height // 4,
            reduced_width, reduced_height
        )
    
    def get_increased_rect(self, road):
        """
        Обчислення хітбоксу, більшого за візуал
        Використовується для близького обгону
        :param road:
        :return:
        """
        rect = self.get_rect(road)
        increased_width = rect.width * 1.5
        increased_height = rect.height
        new_x = rect.x - (increased_width - rect.width) // 2 # Центрування хітбоксу

        return pygame.Rect(
            new_x, rect.y,
            increased_width, increased_height
        )

    def render(self, screen, road):
        """
        Малює перешкоду на екрані.
        """
        rect = self.get_rect(road)
        pygame.draw.rect(screen, self.color, rect)
        # Відмалювання хітбокса + хітбокса для обгону
        # (Для тесту) Якщо перетинає малий хб - аварія, якщо великий - бонус 100 поінтів
        reduced_rect = self.get_reduced_rect(road)
        increased_rect = self.get_increased_rect(road)
        pygame.draw.rect(screen, (255, 0, 0), reduced_rect, 2)
        pygame.draw.rect(screen, (0, 0, 255), increased_rect, 2)