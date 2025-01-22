import random
from obstacle import Obstacle

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, player, road):
        """
        Оновлює позицію перешкод.
        """
        collision_detected = False
        
        for obstacle in self.obstacles:
            obstacle.update()
            if obstacle.get_reduced_rect(road).colliderect(player.get_rect()):
                collision_detected = True

        # Видалення перешкод
        self.obstacles = [o for o in self.obstacles if o.depth > 0.3]

        # Obstacle generation
        # Basically, we create either 1 or 2 obstacles on the horizon
        
        if random.random() < 0.01:
            if (len(self.obstacles) < 2):
                lane = random.randint(0, 2);
                depth = random.uniform(1, 1.05);
                
                # Added an option to add custom depth. 
                # May be useful for different obstacle types which can appear anywhere on the road (falling trees, lightning, car crushes?)
                self.obstacles.append(Obstacle(lane, depth)); 

        return collision_detected

    def check_collision(self, player, road):
        """
        Перевіряє, чи є зіткнення між гравцем і будь-якою перешкодою. Не ворк
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