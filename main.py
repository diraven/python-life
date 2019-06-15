"""Main module."""
import random
import typing

import math
import pygame
from pygame import locals

import settings

pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class World:
    """Game world."""

    def __init__(self, display):
        """Initialize world."""
        self._display = display
        self._grid: typing.Dict[typing.Tuple[int, int], Creature] = {}

    def render_frame(self):
        """Render frame onto display."""
        self._display.fill(black)
        for coords, creature in self._grid.items():
            self._display.set_at(coords, creature.color)
        pygame.display.update()

    def spawn_colony(self, color, coords=None, count=32):
        """Spawn a colony."""
        if coords is None:
            coords = (
                random.randint(0, settings.RESOLUTION_WIDTH - 1),
                random.randint(0, settings.RESOLUTION_HEIGHT - 1),
            )
        colony = Colony(self, color)
        for _ in range(count):
            radius = 0
            for _ in range(10):
                angle = 2 * math.pi * random.random()
                x = int(radius * math.cos(angle) + coords[0])
                y = int(radius * math.sin(angle) + coords[1])
                if x >= settings.RESOLUTION_WIDTH \
                        or y >= settings.RESOLUTION_HEIGHT:
                    break
                if (x, y) not in self._grid:
                    self._grid[(x, y)] = Creature(colony)
                    break
                radius += 1


class Colony:
    """Game colony."""

    def __init__(self, world: World, color):
        """Initialize colony."""
        self._world = world
        self._color = color

    @property
    def color(self):
        """Get colony color."""
        return self._color


class Creature:
    """Game creature."""

    def __init__(self, colony: Colony):
        """Initialize creature."""
        self._colony = colony

    @property
    def color(self):
        """Get creature color."""
        return self._colony.color


w = World(pygame.display.set_mode(settings.RESOLUTION))
w.spawn_colony(white)
w.spawn_colony(red)
w.spawn_colony(green)
w.spawn_colony(blue)

while True:
    w.render_frame()
    for event in pygame.event.get():
        if event.type in (locals.QUIT, locals.KEYDOWN):
            exit()
