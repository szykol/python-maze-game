import pygame

class Plate(pygame.sprite.Sprite):
    BLACK = 'black.png'
    YELLOW = 'yellow.png'
    ROCK = 'rock.png'

    IMAGES = {
        BLACK: pygame.image.load('img/' + BLACK),
        YELLOW: pygame.image.load('img/' + YELLOW),
        ROCK: pygame.image.load('img/' + ROCK)
    }

    SIZE = (60,60)
    def __init__(self, position, type=ROCK, visible=False):
        self.type = type
        self.visible = visible
        self.rect.left, self.rect.top = position
        pygame.sprite.Sprite.__init__(self)

    @property
    def visible(self):
        return self.__visible
    
    @visible.setter
    def visible(self, v):
        display = None
        if v:
            display = self.type
        else:
            display = Plate.BLACK

        self.image = Plate.IMAGES[display]
        if not hasattr(self, 'rect'):
            self.rect = self.image.get_rect()
