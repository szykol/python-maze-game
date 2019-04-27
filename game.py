import pygame
import random
import numpy as np

from plate import Plate

pygame.init()
screen = pygame.display.set_mode((1920, 1080))#, pygame.FULLSCREEN)

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
p = Plate((100, 200), Plate.YELLOW, visible=True)

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
            plates[x, y] = Plate((x * Plate.SIZE[0], y * Plate.SIZE[1]), type=t, visible=True)

    return plates

plates = spawn_simple_maze()

all_sprites.add(plates)
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        done = True


    screen.fill((0,0,0))

    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)