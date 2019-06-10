from random import random

import pygame
from pygame.locals import SRCALPHA


class Node:
    DIAGONALS_ENABLED = True
    DIAGONAL_WALL_CHECK = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.total_cost = 0  # "fScore"
        self.cost_to_node = 0  # "gScore"
        self.previous = None

        self.wall = random() < 0.25

        self.__neighbours = None

    def __str__(self):
        return "Node({},{}) Wall={}".format(self.x, self.y, self.wall)

    def __eq__(self, other):
        if other.x != self.x:
            return False
        if other.y != self.y:
            return False
        return True

    def show(self, width, height, color):
        surface = pygame.Surface((width, height), SRCALPHA)
        if color is not None:
            rect = pygame.Rect(0, 0, width / 2, height / 2)
            rect.center = (width / 2, height / 2)
            pygame.draw.ellipse(surface, color, rect)
        return surface, (width * self.x, height * self.y)

    def neighbours(self, grid):
        # Cache so we don't need to calc every time
        if self.__neighbours is not None:
            return self.__neighbours

        self.__neighbours = []

        # Top
        if self.y > 0:
            self.__neighbours.append(grid[self.x][self.y - 1])
        # Right
        if self.x + 1 < len(grid):
            self.__neighbours.append(grid[self.x + 1][self.y])
        # Bottom
        if self.y + 1 < len(grid[0]):
            self.__neighbours.append(grid[self.x][self.y + 1])
        # Left
        if self.x > 0:
            self.__neighbours.append(grid[self.x - 1][self.y])

        if Node.DIAGONALS_ENABLED:
            # Top left (if no top/left walls)
            if self.y > 0 and self.x > 0:
                if not Node.DIAGONAL_WALL_CHECK or \
                        (not grid[self.x][self.y - 1].wall and not grid[self.x - 1][self.y].wall):
                    self.__neighbours.append(grid[self.x - 1][self.y - 1])
            # Top right (if no top/right walls)
            if self.y > 0 and self.x + 1 < len(grid):
                if not Node.DIAGONAL_WALL_CHECK or \
                        (not grid[self.x][self.y - 1].wall and not grid[self.x + 1][self.y].wall):
                    self.__neighbours.append(grid[self.x + 1][self.y - 1])
            # Bottom right (if no bottom/right walls)
            if self.y + 1 < len(grid[0]) and self.x + 1 < len(grid):
                if not Node.DIAGONAL_WALL_CHECK or \
                        (not grid[self.x][self.y + 1].wall and not grid[self.x + 1][self.y].wall):
                    self.__neighbours.append(grid[self.x + 1][self.y + 1])
            # Bottom left (if no bottom/left walls)
            if self.y + 1 < len(grid[0]) and self.x > 0:
                if not Node.DIAGONAL_WALL_CHECK or \
                        (not grid[self.x][self.y + 1].wall and not grid[self.x - 1][self.y].wall):
                    self.__neighbours.append(grid[self.x - 1][self.y + 1])

        # Remove any neighbours that are walls
        for node in self.__neighbours.copy():
            if node.wall:
                self.__neighbours.remove(node)

        return self.__neighbours
