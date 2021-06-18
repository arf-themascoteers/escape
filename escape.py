import pygame
import random
from direction import Direction
from element import Element
import numpy as np

pygame.init()

font = pygame.font.SysFont('arial.ttf', 25)

BLOCK_SIZE = 16
SPEED = 5

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

class EscapeGame:
    def __init__(self, w=640, h=480):
        self.WIDTH = w
        self.HEIGHT = h
        self.step = 0

        self.COLS = self.WIDTH // BLOCK_SIZE
        self.ROWS = self.HEIGHT // BLOCK_SIZE

        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Escape")
        self.clock = pygame.time.Clock()
        self.direction = Direction.RIGHT

        self.score = 1000
        self.grid = np.zeros([self.ROWS, self.COLS], dtype=np.uint8)
        self.HOLE_X = None
        self.HOLE_Y = None
        self.AGENT_X = 10
        self.AGENT_Y = 10
        self.grid[self.AGENT_X,self.AGENT_Y] = Element.AGENT.value
        self.prepare()

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        self.step = self.step +1
        print("Step ",self.step)
        self._move(self.direction)

        game_over = False

        if self.AGENT_X == self.HOLE_X and self.AGENT_Y == self.HOLE_Y:
            print("Winner!")
            game_over = True
            return game_over, self.score

        if self._is_collision():
            print("Loser - Wall hit")
            game_over = True
            return game_over, 0

        if self.score == 0:
            print("Loser - Time up")
            game_over = True
            return game_over, 0

        self.score = self.score - 1
        self._update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for i in range(self.grid.shape[1]):
            for j in range(self.grid.shape[0]):
                if self.grid[j,i] != 0:
                    self.draw_element(i,j)

        text = font.render("Score: "+str(self.score), True, WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()

    def draw_element(self, i, j):
        element = Element(self.grid[j,i])
        color = BLACK
        if element == Element.WALL:
            color = RED
        elif element == Element.AGENT:
            color = BLUE1

        rect = pygame.Rect(i*BLOCK_SIZE, j*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(self.display, color, rect)

    def _move(self, direction):
        self.grid[self.AGENT_Y, self.AGENT_X] = Element.BLANK.value
        if direction == Direction.RIGHT:
            self.AGENT_X += 1
        elif direction == Direction.LEFT:
            self.AGENT_X -= 1
        elif direction == Direction.DOWN:
            self.AGENT_Y += 1
        elif direction == Direction.UP:
            self.AGENT_Y -= 1
        if self.AGENT_X >=0 and self.AGENT_X < self.grid.shape[1]-1 and \
                self.AGENT_Y >=0 and self.AGENT_Y < self.grid.shape[0]-1:
            self.grid[self.AGENT_Y, self.AGENT_X] = Element.AGENT.value


    def _is_collision(self):
        if self.AGENT_X > self.grid.shape[1] - 1 or \
                self.AGENT_X < 0 or \
                self.AGENT_Y > self.grid.shape[0] - 1 or \
                self.AGENT_Y < 0:
            return True

        return False

    def prepare(self):
        self.place_wall()
        self.put_hole()

    def place_wall(self):
        corner_y = self.ROWS - 1
        corner_x = self.COLS - 1

        for x in range(self.COLS):
            self.grid[0, x] = Element.WALL.value
            self.grid[corner_y, x] = Element.WALL.value

        for y in range(self.ROWS):
            self.grid[y, 0] = Element.WALL.value
            self.grid[y, corner_x]  = Element.WALL.value

    def put_hole(self):
        side = random.randint(1,4)
        self.put_hole_side(Direction(side))

    def put_hole_side(self, side):
        x = 0
        y = 1
        if side == Direction.LEFT:
            x = 0
            y = random.randint(1, self.ROWS - 2)
        elif side == Direction.RIGHT:
            x = self.COLS - 1
            y = random.randint(1, self.ROWS - 2)
        elif side == Direction.UP:
            x = random.randint(1, self.COLS - 2)
            y = 0
        elif side == Direction.DOWN:
            x = random.randint(1, self.COLS - 2)
            y = self.ROWS - 1
        self.grid[y,x] = Element.BLANK.value
        self.HOLE_X = x
        self.HOLE_Y = y


if __name__ == '__main__':
    game = EscapeGame()
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print("Final Score", score)

    pygame.quit()
