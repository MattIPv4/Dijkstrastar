from math import sqrt, pow
from random import randint

import pygame
from pygame.locals import *

from node import Node


class Search:

    def __init__(self):
        # Basic grid information
        self.cols = 50
        self.rows = 50
        self.width = 20
        self.height = 20

        # Generate the grid of nodes
        self.grid = [[Node(_x, _y) for _y in range(self.rows)] for _x in range(self.cols)]

        # Top quarter corner will be start
        start_max_x = 0
        start_max_y = 0
        # start_max_x = int((self.cols - 1) / 4)
        # start_max_y = int((self.rows - 1) / 4)
        self.start = self.grid[randint(0, start_max_x)][randint(0, start_max_y)]
        self.start.wall = False
        self.start.color = (0, 255, 0)

        # Bottom quarter corner will be end
        end_min_x = self.cols - 1
        end_min_y = self.rows - 1
        # end_min_x = int((self.cols - 1) / 4 * 3)
        # end_min_y = int((self.rows - 1) / 4 * 3)
        self.end = self.grid[randint(end_min_x, self.cols - 1)][randint(end_min_y, self.rows - 1)]
        self.end.wall = False
        self.end.color = (0, 0, 255)

        # Store what has been visited and what is currently open
        self.visited = []
        self.open = [self.start]
        self.cheapest_node = None

        # Pygame & loop control
        pygame.init()
        self.screen = pygame.display.set_mode((self.cols * self.width, self.rows * self.height))
        self.running = False
        self.searching = False

    @staticmethod
    def heuristic(a, b):
        # If can go diagonally, use true distance
        if Node.DIAGONALS_ENABLED:
            return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2))
        # Else, use the "manhattan" distance
        return abs(a.x - b.x) + abs(a.y - b.y)

    def path(self):
        temp = []
        node = self.cheapest_node
        temp.append(node)
        while node.previous:
            temp.append(node.previous)
            node = node.previous
        return temp

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
        path = self.path()
        for col in self.grid:
            for row in col:
                color = None
                if row in self.visited:
                    color = (200, 50, 50)
                if row in self.open:
                    color = (50, 200, 50)
                if row in path:
                    color = (200, 50, 200)
                self.screen.blit(*row.show(self.width, self.height, color))
        pygame.display.flip()

    def search(self):
        # If no nodes to explore, no solution, abort
        if not self.open:
            print("No solution!")
            self.searching = False
            return

        # Find the cheapest node
        self.cheapest_node = None
        for node in self.open:
            if self.cheapest_node is None or node.total_cost < self.cheapest_node.total_cost:
                self.cheapest_node = node

        # We're visiting the end, so we can abort
        node = self.cheapest_node
        if node is self.end:
            print("End found!")
            self.searching = False
            return

        # We're visiting this, so remove from open
        self.open.remove(node)

        # Explore all neighbours of the node
        for neighbour in node.neighbours(self.grid):
            # If node has already been visited, skip
            if neighbour in self.visited:
                continue

            # Calculate new cost to node (assume distance from current to this neighbour is 1)
            temp_cost_to_node = neighbour.cost_to_node + 1

            # If this is a node not seen before, add it to open
            if neighbour not in self.open:
                self.open.append(neighbour)
            # Else, if the new cost to the node is more expensive, skip this node
            elif temp_cost_to_node > neighbour.cost_to_node:
                continue

            # This is the cheapest way to get to this neighbour, so save it
            neighbour.previous = node
            neighbour.cost_to_node = temp_cost_to_node
            neighbour.total_cost = temp_cost_to_node + self.heuristic(neighbour, self.end)

        # We're done, so mark the node as visited
        self.visited.append(node)

    def run(self):
        self.running = True
        self.searching = True
        while self.running:
            if self.searching:
                self.search()
            self.draw()


if __name__ == "__main__":
    Search().run()
