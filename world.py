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

    def closest_wall(self, pov, ray):
        q_min = -1
        wall_min = None
        t_wall = None
        for wall in self.walls:
            t,q = wall.top_line.intersect(pov, ray)
            if 0<=t<=1:
                if q_min < 0 < q:
                    q_min = q
                if q_min >= q:
                    q_min = q
                    wall_min = wall
                    t_wall = t

        return wall_min, t_wall



    def draw(self, screen, player):
        size = screen.get_size()
        dx = 2.0 / size[0]
        x = -1.0
        for xx in range(size[0]):
            ray = player.direction.add(player.right_dir.mul(x))
            wall, t = self.closest_wall(player, ray)
            if wall is not None:
                wall.texture.scale()

            x += dx
            print(f"xx={xx} x={x} dx={dx} ray={ray}")




        # for wall in self.walls:
        #     wall.draw(screen, size, player)
