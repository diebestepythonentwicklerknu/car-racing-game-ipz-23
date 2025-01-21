import pygame


class InputManager:
    """
    Обробка натискань клавіш.
    """
    def __init__(self):
        self.left_pressed = False
        self.right_pressed = False
        self.accelerate_pressed = False
        self.decelerate_pressed = False

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left_pressed = True
            elif event.key == pygame.K_RIGHT:
                self.right_pressed = True
            elif event.key == pygame.K_UP:
                self.accelerate_pressed = True
            elif event.key == pygame.K_DOWN:
                self.decelerate_pressed = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left_pressed = False
            elif event.key == pygame.K_RIGHT:
                self.right_pressed = False
            elif event.key == pygame.K_UP:
                self.accelerate_pressed = False
            elif event.key == pygame.K_DOWN:
                self.decelerate_pressed = False

    def update_player(self, player):
        """
        Оновлює стан гравця залежно від натиснутих клавіш.
        """
        if self.left_pressed:
            player.move_left()
        if self.right_pressed:
            player.move_right()
        if self.accelerate_pressed:
            player.increase_speed()
        if self.decelerate_pressed:
            player.decrease_speed()
