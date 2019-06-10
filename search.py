from math import sqrt, pow

import pygame


class Search:

    def __init__(self, show_dots, astar, line_color, nodes_as_circles, allow_diagonal_paths):
        # Grid data
        self.grid = None
        self.start = None
        self.end = None
        self.show_dots = show_dots
        self.line_color = line_color  # Use None to use default colors
        self.nodes_as_circles = nodes_as_circles
        self.allow_diagonal_paths = allow_diagonal_paths

        # Searching data
        self.astar = astar
        self.visited = None
        self.open = None
        self.cheapest_node = None
        self.searching = None

    def reset(self, grid, start, end):
        # Save the grid data
        self.grid = grid
        self.start = start
        self.end = end

        # Store what has been visited and what is currently open
        self.visited = []
        self.open = [self.start]
        self.cheapest_node = None
        self.searching = True

    def heuristic(self, a, b):
        # If this is emulating dijkstra, use a heuristic of zero always
        if not self.astar:
            return 0
        # If can go diagonally, use true distance
        if self.allow_diagonal_paths:
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

    def draw(self, surface, node_width, node_height):
        path = self.path()
        path_color = (20, 255, 20) if self.cheapest_node == self.end else (255, 20, 20)

        # Draw all the points
        if self.show_dots:
            for col in self.grid:
                for row in col:
                    color = None
                    if row in self.visited:
                        color = (200, 50, 50) if self.searching else (200, 150, 200)
                    if row in self.open:
                        color = (50, 200, 50) if self.searching else (200, 255, 200)
                    if row in path and not self.searching:
                        color = self.line_color or path_color
                    if color:
                        surface.blit(*row.show(node_width, node_height, color, self.nodes_as_circles))

        # Draw the path
        if len(path) > 1:
            color = self.line_color or ((150, 50, 150) if self.searching else path_color)
            pygame.draw.lines(surface, color, False,
                              [(node.x * node_width + node_width / 2,
                                node.y * node_height + node_height / 2) for node
                               in path], 3)

    def search(self):
        # Don't do anything if not searching
        if not self.searching:
            return

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
        if node == self.end:
            print("End found!")
            self.searching = False
            return

        # We're visiting this, so remove from open
        self.open.remove(node)

        # Explore all neighbours of the node
        for neighbour in node.neighbours(self.grid, self.allow_diagonal_paths, not self.nodes_as_circles):
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
