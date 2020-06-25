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
        self.chance_of_wall = 0.35
        self.max_fps = 120
        self.display_fps = True

        self.start_x_restriction = 0.2
        self.start_y_restriction = 0.05

        self.end_x_restriction = 0.2
        self.end_y_restriction = 0.05

        # Pygame & loop control
        pygame.init()
        pygame.display.set_caption('Dijkstrastar')
        self.screen = pygame.display.set_mode((self.cols * self.width, self.rows * self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.grid_surface = None
        self.running = False
        self.fps_avg = 0
        self.fps_frames = 0

        # Searches
        self.searches = [
            Search(False, False, (0, 255, 255), self.nodes_as_circles, self.allow_diagonal_paths),  # Dijkstra (cyan)
            Search(False, True, (255, 0, 255), self.nodes_as_circles, self.allow_diagonal_paths)  # A* (magenta)
        ]
        self.reset()

    def reset(self):
        # Generate the grid of nodes
        self.grid = [[Node(_x, _y, self.chance_of_wall) for _y in range(self.rows)] for _x in range(self.cols)]
        self.grid_surface = None
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

        # Create base grid if not already done
        if not self.grid_surface:
            self.grid_surface = pygame.Surface((self.cols * self.width, self.rows * self.height))
            self.grid_surface.fill((100, 100, 100))

            # Draw all the points
            for col in self.grid:
                for row in col:
                    grid_color = None
                    if row.wall:
                        grid_color = (20, 20, 20)
                    if row == self.start:
                        grid_color = (255, 255, 0)
                    if row == self.end:
                        grid_color = (0, 255, 0)
                    self.grid_surface.blit(*row.show(self.width, self.height, grid_color, self.nodes_as_circles))

        # Base grid
        self.screen.blit(self.grid_surface, (0, 0))

        # Allow searches to draw their paths
        for search in self.searches:
            search.draw(self.screen, self.width, self.height)

        # FPS
        if self.display_fps:
            fps = self.clock.get_fps()
            self.fps_avg = (self.fps_avg * self.fps_frames + fps) / (self.fps_frames + 1)
            self.fps_frames += 1
            fps_text = self.font.render("FPS: {:,.1f} / Avg: {:,.1f}".format(fps, self.fps_avg), 1, (255, 255, 255))
            self.screen.blit(fps_text, (10, 5))

        # Render
        self.clock.tick(self.max_fps)
        pygame.display.flip()

    def run(self):
        self.running = True
        self.fps_avg = 0
        self.fps_frames = 0
        while self.running:
            for search in self.searches:
                search.search()
            self.draw()


if __name__ == "__main__":
    Grid().run()
