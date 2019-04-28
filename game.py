import pygame
import random
import numpy as np

from plate import Plate
from player import Player

def spawn_simple_maze():
    plates = np.empty((8, 8), dtype=Plate)
    yellow = [
        (0, 1), (1,1), (2,1), (3,1), (4, 1), (6,1),
        (3, 2), (6, 2),
        (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
        (2, 4), (4, 4),
        (1, 5), (2, 5), (4, 5), (5, 5), (6, 5),
        (1, 6), (4, 6),
        (1, 7)
    ]
    for y in range(plates.shape[1]):
        for x in range(plates.shape[0]):
            t = Plate.ROCK
            if (x, y) in yellow:
                t = Plate.YELLOW
            plates[x, y] = Plate((x * Plate.SIZE[0], y * Plate.SIZE[1]), type=t)

    return plates

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.done = False

        self.plates = spawn_simple_maze()
        self.player_index = (7, 1)
        self.player = Player(self.plates[self.player_index].rect.center)
        
        self.screen = pygame.display.set_mode((1920, 1080))#, pygame.FULLSCREEN)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.plates)
        self.all_sprites.add(self.player)

    def draw(self):
        self.screen.fill((0,0,0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def update(self):
        self._handle_keys()
        
        self._show_neighb_plates()

    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            self.update()
            self.draw()

            self.clock.tick(10)

    def _handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.done = True

        if keys[pygame.K_RIGHT]:
            self.player_index = self.player_index[0] + 1, self.player_index[1]
            self.player.direction = Player.RIGHT
        if keys[pygame.K_DOWN]:
            self.player_index = self.player_index[0], self.player_index[1] + 1
            self.player.direction = Player.DOWN
        if keys[pygame.K_LEFT]:
            self.player_index = self.player_index[0] - 1, self.player_index[1]
            self.player.direction = Player.LEFT
        if keys[pygame.K_UP]:
            self.player_index = self.player_index[0], self.player_index[1] - 1
            self.player.direction = Player.UP


        self.player.rect.center = self.plates[self.player_index].rect.center



    def _show_neighb_plates(self):
        x, y = self.player_index
        
        slice = self.plates[x-1 if x > 0 else x:x+2, y-1 if y > 0 else y:y+2]
        for y in range(slice.shape[1]):
            for x in range(slice.shape[0]):
                slice[x, y].visible = True


if __name__ == "__main__":
    pygame.init()
    
    g = Game()
    g.run()