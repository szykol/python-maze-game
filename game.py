import pygame
import random
import numpy as np

from plate import Plate
from player import Player
from threading import Timer

def spawn_simple_maze(pos):
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
            plates[x, y] = Plate((x * Plate.SIZE[0] + pos[0], y * Plate.SIZE[1] + pos[1]), type=t)

    return plates

def load_plates(path, pos):
    # for now they are hardcoded
    SIZE_X = 18
    SIZE_Y = 10

    plates = np.empty((SIZE_X, SIZE_Y), dtype=Plate)
    with open(path, 'r') as f:
        y = 0
        for line in f:
            raw_plates = line.split(' ')
            print(raw_plates)
            for x in range(len(raw_plates)):
                plate_type = int(raw_plates[x].strip())
                print(plate_type)
                t = Plate.ROCK if plate_type == 0 else Plate.YELLOW
                plates[x, y] = Plate((x * Plate.SIZE[0] + pos[0], y * Plate.SIZE[1] + pos[1]), type=t)
            y += 1

    return plates

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.done = False
        self.screen = pygame.display.set_mode((1920, 1080))#, pygame.FULLSCREEN)
        self.plates = load_plates('level1', (400, 200))

        background = pygame.sprite.Sprite()
        background.image = pygame.image.load('img/maze.png')
        background.rect = background.image.get_rect()
        
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(background)
        self.all_sprites.add(self.plates)
        self._setup()
        
        
    def draw(self):
        self.screen.fill((0,0,0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def update(self):
        self._handle_keys()

        if self.player_index == self.end_index:
            print('Win!')
            self._setup()
        
    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            self.update()
            self.draw()

            self.clock.tick(60)

    def _setup(self):
        self.player_index = (0, 1)
        self.end_index = (16,9)
        self.forks = []
        self.visited_forks = []

        if hasattr(self, 'player'):
            self.all_sprites.remove(self.player)
            
        self.player = Player(self.plates[self.player_index].rect.center)
        self.all_sprites.add(self.player)

        self._show_neighb_plates()
        self._check_neighb_plates()
        self._enable_move()

    def _handle_keys(self):
        keys = pygame.key.get_pressed()
        
        next_move = None
        direction = None
        if keys[pygame.K_q]:
            self.done = True
        elif keys[pygame.K_RIGHT]:
            next_move = (self.player_index[0] + 1, self.player_index[1])
            direction = Player.RIGHT
        elif keys[pygame.K_DOWN]:
            next_move = (self.player_index[0], self.player_index[1] + 1)
            direction = Player.DOWN
        elif keys[pygame.K_LEFT]:
            next_move = (self.player_index[0] - 1, self.player_index[1])
            direction = Player.LEFT
        elif keys[pygame.K_UP]:
            next_move = (self.player_index[0], self.player_index[1] - 1)
            direction = Player.UP

        if next_move is not None:
            self._move_player(next_move, direction)


    def _move_player(self, next_pos, direction):
        if not self.can_move or (next_pos[0] < 0 or next_pos[0] >= self.plates.shape[0]
            or next_pos[1] < 0 or next_pos[1] >= self.plates.shape[1]):
            return

        if self.plates[next_pos].type == Plate.YELLOW:
            # if player_index is the newest fork index
            if self.forks and self.player_index == self.forks[-1]['index']:
                print(self.forks)
                # if direction is the same as fork's current direction
                if direction == self.forks[-1]['directions'][0]:
                    # pop direction when the movement is correct
                    print(self.forks[-1]['directions'])
                    self.forks[-1]['directions'].pop(0)
                    print(self.forks[-1]['directions'])

                    # if there's no more directions - pop the current fork
                    if not self.forks[-1]['directions']:
                        self.forks.pop()
                        print(self.forks)
                else:
                    self._setup()
                    return

            prev_pos = self.player_index
            self.player_index = next_pos
            self.player.rect.center = self.plates[self.player_index].rect.center
            self._show_neighb_plates()
            self._check_neighb_plates(prev_pos)
            self.player.direction = direction

            self.can_move = False
            Timer(0.25, self._enable_move).start()

        
    def _enable_move(self):
        self.can_move = True

    def _show_neighb_plates(self):
        x, y = self.player_index
        
        slice = self.plates[x-1 if x > 0 else x:x+2, y-1 if y > 0 else y:y+2]
        for y in range(slice.shape[1]):
            for x in range(slice.shape[0]):
                slice[x, y].visible = True

    def _check_neighb_plates(self, prev_pos=None):
        x, y = self.player_index

        indices = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        directions = []
        for i in range(4):
            # print(indices[i])
            pos_x, pos_y = indices[i]
            if pos_x > 0 and pos_x < self.plates.shape[0] and pos_y > 0 and pos_y < self.plates.shape[1]:
                if self.plates[pos_x, pos_y].type == Plate.YELLOW:
                    if prev_pos is not None and (pos_x, pos_y) != prev_pos:
                        directions.append(i)
                    # print('App')
                    # print(indices[i])
                    # print(directions)

        if len(directions) > 1 and not (x,y) in self.visited_forks:
            self.forks.append({
                'index': (x,y),
                'directions': directions
            })
            self.visited_forks.append((x,y))
            print('Appending')
        else:
            self.no_move = True




if __name__ == "__main__":
    # print(load_plates('level1', (10, 10)))
    pygame.init()
    
    g = Game()
    g.run()

