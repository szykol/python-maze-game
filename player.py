import pygame

class Player(pygame.sprite.Sprite):
    RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3
    IMAGES = [pygame.image.load('img/player_{}.png'.format(x)) for x in range(4)]

    def __init__(self, center):
        self.direction = Player.UP
        self.rect.center = center
        pygame.sprite.Sprite.__init__(self)

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.__direction = direction
        
        # self.image = pygame.image.load('img/player_{}.png'.format(direction))
        self.image = Player.IMAGES[direction]
        if not hasattr(self, 'rect'):
            self.rect = self.image.get_rect()

        
        