from random import random


class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.wall = random() < 0.2
        self.color = (0, 0, 0) if self.wall else (255, 255, 255)
