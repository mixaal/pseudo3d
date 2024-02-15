from transform import Point3d
from wall import Wall


class World(object):
    def __init__(self):
        self.walls = [
            Wall(-1.0,  2.0, 1.0, 2.0),
            Wall(-1.0,  1.0, -1.0, 2.0),
            Wall(1.0, 1.0, 1.0, 2.0),

            Wall(-1.0, 1.0, -2.0, 1.0),
            Wall(1.0, 1.0, 2.0, 1.0),
            Wall(-2.0, 1.0, -2.0, -1.0),
            Wall(2.0, 1.0, 2.0, -1.0),

            Wall(1.0, -1.0, 2.0, -1.0),
            Wall(-1.0, -1.0, -2.0, -1.0),

            Wall(-1.0, -2.0, 1.0, -2.0),
            Wall(-1.0, -1.0, -1.0, -2.0),
            Wall(1.0, -1.0, 1.0, -2.0),
        ]

    def draw(self, screen, player):
        size = screen.get_size()
        for wall in self.walls:
            wall.draw(screen, size, player)
