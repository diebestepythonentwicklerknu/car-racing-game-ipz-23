import os.path

import pygame

'''
SpriteManager class is a utility class that helps to load and manage sprites
'''


class SpriteManager:
    @staticmethod
    def load_image(filename):
        file_path = os.path.join('project','assets', 'sprites', filename)
        sprite = pygame.image.load(file_path).convert_alpha()
        sprite.set_colorkey((0, 0, 0))
        return sprite

    '''
    Gets one frame from a sprite sheet
    '''

    @staticmethod
    def get_frame(image, width, height, scale=1, frame=0):
        surface = pygame.Surface((width, height)).convert_alpha()
        surface.blit(image, (0, 0), ((frame * width), 0, width, height))
        surface = pygame.transform.scale(surface, (width * scale, height * scale))
        surface.set_colorkey((0, 0, 0))

        return surface

    '''
    Gets the sequence of frames from a sprite sheet and return an array of frames
    '''

    @staticmethod
    def get_frame_sequence(img_url, frame_width, frame_height, scale):
        img = SpriteManager.load_image(img_url)
        frames = []
        frame_amount = img.get_width() // frame_width
        for i in range(0, frame_amount):
            frames.append(SpriteManager.get_frame(img, frame_width, frame_height, scale, i))

        return frames
