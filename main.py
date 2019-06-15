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

Coords = typing.Tuple[int, int]


class World:
    """Game world."""

    def __init__(self, display):
        """Initialize world."""
        self._display = display
        self.grid: typing.Dict[typing.Tuple[int, int], Creature] = {}

    def render_frame(self):
        """Render frame onto display."""
        self._display.fill(black)
        for coords, creature in self.grid.items():
            self._display.set_at(coords, creature.color)
        pygame.display.update()

    def update_cell(self, coords: Coords):
        """Update world cell status."""
        for adjacent_cell in self.get_adjacent_coords(coords) + [coords]:
            creature = self.grid.get(adjacent_cell)
            if creature:
                creature.update_activeness()

    @staticmethod
    def get_adjacent_coords(coords: typing.Tuple[int, int]) -> typing.List[
        typing.Tuple[int, int],
    ]:
        """Get adjacent coords set."""
        coords_set = []
        if coords[0] > 0:
            coords_set.append((coords[0] - 1, coords[1]))
        if coords[0] < settings.RESOLUTION_WIDTH - 1:
            coords_set.append((coords[0] + 1, coords[1]))
        if coords[1] > 0:
            coords_set.append((coords[0], coords[1] - 1))
        if coords[1] < settings.RESOLUTION_HEIGHT - 1:
            coords_set.append((coords[0], coords[1] + 1))
        return coords_set


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

    @property
    def world(self):
        """Get colony world."""
        return self._world

    @staticmethod
    def spawn(world: World, color, coords=None, count=32):
        """Spawn a colony."""
        if coords is None:
            coords = (
                random.randint(0, settings.RESOLUTION_WIDTH - 1),
                random.randint(0, settings.RESOLUTION_HEIGHT - 1),
            )
        colony = Colony(world, color)
        for _ in range(count):
            radius = 0
            for _ in range(10):
                angle = 2 * math.pi * random.random()
                x = int(radius * math.cos(angle) + coords[0])
                y = int(radius * math.sin(angle) + coords[1])
                if x >= settings.RESOLUTION_WIDTH \
                        or y >= settings.RESOLUTION_HEIGHT:
                    break
                if (x, y) not in world.grid:
                    Creature.spawn(colony, (x, y))
                    break
                radius += 1
        return colony


class Creature:
    """Game creature."""

    def __init__(self, colony: Colony, coords: typing.Tuple[int, int]):
        """Initialize creature."""
        self._colony = colony
        self._coords = coords
        self.is_active = True

    @property
    def color(self):
        """Get creature color."""
        return self._colony.color

    @property
    def world(self):
        """Get creature world."""
        return self._colony.world

    @property
    def coords(self):
        """Get creature coords."""
        return self._coords

    @property
    def colony(self):
        """Get creature colony."""
        return self._colony

    @staticmethod
    def spawn(colony: Colony, coords: typing.Tuple[int, int]):
        """Spawn creature."""
        colony.world.grid[coords] = Creature(
            colony,
            coords,
        )
        colony.world.update_cell(coords)

    def update_activeness(self):
        """Update activity status of the creature."""
        for adjacent_cell in self.world.get_adjacent_coords(self.coords):
            adjacent_creature = self.world.grid.get(adjacent_cell)
            if not adjacent_creature \
                    or adjacent_creature.colony != self.colony:
                self.is_active = True
                return
        self.is_active = False

    def act(self):
        """Let the creature perform action."""
        coords_set = self.world.get_adjacent_coords(self._coords)
        target_coords = random.choice(coords_set)
        if self.world.grid.get(target_coords) is None:
            Creature.spawn(self._colony, target_coords)
        else:
            pass


w = World(pygame.display.set_mode(settings.RESOLUTION))
Colony.spawn(w, white)
Colony.spawn(w, red)
Colony.spawn(w, green)
Colony.spawn(w, blue)

while True:
    [
        creature.act() for creature in list(w.grid.values())
        if creature.is_active
    ]
    w.render_frame()
    for event in pygame.event.get():
        if event.type in (locals.QUIT, locals.KEYDOWN):
            exit()
