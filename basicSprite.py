import pygame

class Sprite(pygame.sprite.Sprite):
    '''base class for all sprites in the game'''
    def __init__(self, centerPoint, image):
        pygame.sprite.Sprite.__init__(self)
        # Set the image and the rect
        self.image = image
        self.rect = image.get_rect()
        # move the rect into the right position
        self.rect.center = centerPoint
