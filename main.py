from gfx import Screen
from transform import Pov
from world import World

player = Pov(0, 0, 0.1)
world = World()

s = Screen()
s.update(world, player)
