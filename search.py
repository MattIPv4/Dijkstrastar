from random import randint

import pygame
from pygame.locals import *

from node import Node


class Search:

    def __init__(self):
        # Basic grid information
        self.cols = 5
        self.rows = 5
        self.width = 20
        self.height = 20

        # Generate the grid of nodes
        self.grid = [[Node(_x, _y) for _y in range(self.rows)] for _x in range(self.cols)]

        # Top third corner will be start
        start_max_x = int((self.cols - 1) / 3)
        start_max_y = int((self.rows - 1) / 3)
        start_max_x = 0
        start_max_y = 0
        self.start = self.grid[randint(0, start_max_x)][randint(0, start_max_y)]
        self.start.wall = False
        self.start.color = (0, 255, 0)

        # Bottom third corner will be end
        end_min_x = int((self.cols - 1) / 3 * 2)
        end_min_y = int((self.rows - 1) / 3 * 2)
        end_min_x = self.cols - 1
        end_min_y = self.rows - 1
        self.end = self.grid[randint(end_min_x, self.cols - 1)][randint(end_min_y, self.rows - 1)]
        self.end.wall = False
        self.end.color = (0, 0, 255)

        # Store what has been visited and what is currently open
        self.visited = []
        self.open = [self.start]

        # Pygame & loop control
        pygame.init()
        self.screen = pygame.display.set_mode((self.cols * self.width, self.rows * self.height))
        self.running = True

    def draw(self):
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == QUIT:
                self.running = False

        # Do some drawing
        self.screen.fill((255, 255, 255))
        for col in self.grid:
            for row in col:
                color = None
                if row in self.visited:
                    color = (200, 50, 50)
                if row in self.open:
                    color = (50, 200, 50)
                self.screen.blit(*row.show(self.width, self.height, color))
        pygame.display.flip()

    def search(self):
        if not self.open:
            # No solution, abort
            self.running = False
            return

    def run(self):
        self.running = True
        while self.running:
            self.search()
            self.draw()


if __name__ == "__main__":
    Search().run()
