import pygame
import random
import json

import numpy as np

from plate import Plate
from player import Player
from threading import Timer

def load_random_level(path, pos):
    with open(path, 'r') as f:
        levels = json.load(f)

        r = random.randrange(len(levels))
        lvl_obj = levels[r]

        raw_plates = np.array(lvl_obj['plates'])
        start = tuple(lvl_obj['start'])
        end = tuple(lvl_obj['end'])

        plates = np.empty((raw_plates.shape[1], raw_plates.shape[0]), dtype=Plate)
        y = 0
        for row in raw_plates:
            for x in range(len(row)):
                plate_type = row[x]
                t = Plate.ROCK if plate_type == 0 else Plate.YELLOW
                plates[x, y] = Plate((x * Plate.SIZE[0] + pos[0], y * Plate.SIZE[1] + pos[1]), type=t)
            y += 1

        return {
            "plates": plates,
            "start": start,
            "end": end
        }

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.done = False
        self.screen = pygame.display.set_mode((1920, 1080))#, pygame.FULLSCREEN)
        
        self.level = load_random_level('levels.json', (400, 200))
        self.plates = self.level['plates']

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
        self.player_index = self.level['start']
        self.end_index = self.level['end']

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

        if not self._should_return and next_pos == self.forks[-1]['index']:
            self._setup()
            return

        if self.plates[next_pos].type == Plate.YELLOW:
            # if player_index is the newest fork index
            if self.forks and self.player_index == self.forks[-1]['index']:
                # if direction is the same as fork's current direction
                if direction == self.forks[-1]['directions'][0]:
                    # pop direction when the movement is correct
                    self.forks[-1]['directions'].pop(0)

                    # if there's no more directions - pop the current fork
                    if not self.forks[-1]['directions']:
                        self.forks.pop()
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
            pos_x, pos_y = indices[i]
            if pos_x > 0 and pos_x < self.plates.shape[0] and pos_y > 0 and pos_y < self.plates.shape[1]:
                if self.plates[pos_x, pos_y].type == Plate.YELLOW:
                    if prev_pos is not None and (pos_x, pos_y) != prev_pos:
                        directions.append(i)

        if len(directions) > 1 and not (x,y) in self.visited_forks:
            self.forks.append({
                'index': (x,y),
                'directions': directions
            })
            self.visited_forks.append((x,y))
            self._should_return = False
        elif len(directions) == 0:
            self._should_return = True

if __name__ == "__main__":
    pygame.init()
    
    g = Game()
    g.run()

