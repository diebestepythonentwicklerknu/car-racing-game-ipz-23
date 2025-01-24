import pygame

class SpriteManager:
    def loadImage(filename):
        return pygame.image.load('project/sprites/' + filename).convert_alpha()
    
    def getFrame(image, frame, width, height):
        surface = pygame.Surface((width, height)).convert_alpha()
        surface.blit(image, (0, 0), ((frame * width), 0, width, height) )
        surface = pygame.transform.scale(surface, (width * 4, height * 4))
        surface.set_colorkey((0,0,0));
        return surface


