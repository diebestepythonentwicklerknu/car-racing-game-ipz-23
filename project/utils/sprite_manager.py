import pygame

'''
SpriteManager class is a utility class that helps to load and manage sprites
'''
class SpriteManager:
    def load_image(filename):
        sprite = pygame.image.load('project/assets/sprites/' + filename).convert_alpha()
        sprite.set_colorkey((0,0,0))
        return sprite
    
    '''
    Gets one frame from a sprite sheet
    '''
    def get_frame(image, width, height, scale = 1, frame = 0):
        surface = pygame.Surface((width, height)).convert_alpha()
        surface.blit(image, (0, 0), ((frame * width), 0, width, height) )
        surface = pygame.transform.scale(surface, (width * scale, height * scale))
        surface.set_colorkey((0,0,0))
        
        return surface
    
    '''
    Gets the sequence of frames from a sprite sheet and return an array of frames
    '''
    def get_frame_sequence(imgUrl, frameWidth, frameHeight, scale):
        img = SpriteManager.load_image(imgUrl)
        frames = []
        frameAmount = img.get_width() // frameWidth
        for i in range(0, frameAmount):
            frames.append(SpriteManager.get_frame(img, frameWidth, frameHeight, scale, i))
        
        return frames


