from copy import deepcopy
from random import randint

import pygame
from pygame.locals import *

from node import Node
from search import Search


class Grid:

    def __init__(self):
        # Basic grid information
        self.cols = 100
        self.rows = self.cols

        self.width = 10
        self.height = self.width

        self.grid = None
        self.start = None
        self.end = None

        # Simulation information
        self.nodes_as_circles = False
        self.allow_diagonal_paths = True
        self.chance_of_wall = 0.25

        self.start_x_restriction = 0.2
        self.start_y_restriction = 0.05

        self.end_x_restriction = 0.2
        self.end_y_restriction = 0.05

        # Pygame & loop control
        pygame.init()
        self.screen = pygame.display.set_mode((self.cols * self.width, self.rows * self.height))
        self.running = False

        # Searches
        self.searches = [
            Search(False, False, (0, 255, 255), self.nodes_as_circles, self.allow_diagonal_paths),  # Dijkstra (cyan)
            Search(False, True, (255, 0, 255), self.nodes_as_circles, self.allow_diagonal_paths)  # A* (magenta)
        ]
        self.reset()

    def reset(self):
        # Generate the grid of nodes
        self.grid = [[Node(_x, _y, self.chance_of_wall) for _y in range(self.rows)] for _x in range(self.cols)]
        self.get_start()
        self.get_end()

        # Give searches their data (use copies so they don't touch each other)
        for search in self.searches:
            search.reset(deepcopy(self.grid), deepcopy(self.start), deepcopy(self.end))

    def get_start(self):
        start_max_x = int((self.cols - 1) * self.start_x_restriction)
        start_max_y = int((self.rows - 1) * self.start_y_restriction)
        self.start = self.grid[randint(0, start_max_x)][randint(0, start_max_y)]
        self.start.wall = False

    def get_end(self):
        end_min_x = int((self.cols - 1) * (1 - self.end_x_restriction))
        end_min_y = int((self.rows - 1) * (1 - self.end_y_restriction))
        self.end = self.grid[randint(end_min_x, self.cols - 1)][randint(end_min_y, self.rows - 1)]
        self.end.wall = False

    def draw(self):
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_r:
                    self.reset()
                    return
            elif event.type == QUIT:
                self.running = False

        # Do some drawing
        self.screen.fill((200, 200, 200))

        # Draw all the points
        for col in self.grid:
            for row in col:
                color = None
                if row.wall:
                    color = (0, 0, 0)
                if row == self.start:
                    color = (0, 255, 0)
                if row == self.end:
                    color = (0, 0, 255)
                self.screen.blit(*row.show(self.width, self.height, color, self.nodes_as_circles))

        # Allow searches to draw their paths
        for search in self.searches:
            search.draw(self.screen, self.width, self.height)

        # Render
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            for search in self.searches:
                search.search()
            self.draw()


if __name__ == "__main__":
    Grid().run()
