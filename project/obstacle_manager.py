import os
import random
import time
import pygame
from obstacle import Obstacle

'''
ObstacleManager class is responsible for managing obstacles
'''


class ObstacleManager:

    def __init__(self):
        """
        Initializes the obstacle manager components
        """
        self.__obstacles = []
        self.__near_obstacles = set()
        self.__messages = []

    def update(self, player, road, score_manager, car_speed, camera_offset_x):
        """
        Updates obstacle positions
        """
        collision_detected = False
        player_rect = player.get_rect()
        for obstacle in self.__obstacles:
            obstacle.update(car_speed)

            if obstacle.get_reduced_rect(road, camera_offset_x).colliderect(player.get_rect()):
                collision_detected = True

            # If player goes over 100 kph and near obstacle + 100 to current score
            # Uses wider hitbox
            if obstacle not in self.__near_obstacles:
                if obstacle.get_increased_rect(road, camera_offset_x).colliderect(player.get_rect()) and car_speed > 100:
                    self.__near_obstacles.add(obstacle)
                    score_manager.add_score(100)

                    self.__messages.append({
                        "text": "+100 points!",
                        "time": time.time(),  # Store the current time
                        "position": (player_rect.centerx, player_rect.top - 20)  # Above the player
                    })

        # Remove obstacles that are out of the screen
        self.__obstacles = [o for o in self.__obstacles if o.depth > 0.1]

        self.__near_obstacles = {o for o in self.__near_obstacles if o in self.__obstacles}

        # Generate new obstacles
        if random.random() < 0.01:
            if len(self.__obstacles) < 2:
                lane = random.randint(0, 2)
                depth = random.uniform(1, 1.05)

                # Added an option to add custom depth. May be useful for different obstacle types which can appear
                # anywhere on the road (falling trees, lightning, car crushes?)
                self.__obstacles.append(Obstacle(lane, depth))

        return collision_detected

    def _check_collision(self, player, road, camera_offset_x):
        """
        Checks if objects collides with the player
        """
        return any(obstacle.get_rect(road, camera_offset_x).colliderect(player.get_rect()) for obstacle in
                   self.__obstacles)  # FIX: a bit siplified visualy, but it works

    def render(self, screen, road, camera_offset_x):
        """
        Renders obstacles
        """
        for obstacle in sorted(self.__obstacles, key=lambda x: x.depth, reverse=True):
            obstacle.render(screen, road, camera_offset_x)

        # Display messages about the bonus points
        current_time = time.time()
        for message in self.__messages[:]:
            if current_time - message["time"] <= 1:  # 1 second message lifetime
                message_font = pygame.font.Font(
                    os.path.join(os.path.dirname(__file__), "assets", "PressStart2P-Regular.ttf"), 20)
                text_surface = message_font.render(message["text"], True, (255, 255, 0))
                screen.blit(text_surface, message["position"])
            else:
                self.__messages.remove(message)
