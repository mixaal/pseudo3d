from math import sqrt

from texture import Texture
from transform import Point3d, Z_CLIP
from wall import Wall


class World(object):
    def __init__(self):
        self.stone = Texture("data/textures/wall_trans.png")
        self.stone2 = Texture("data/textures/wall_trans.png", repeat_x=2.0)
        self.big_walls = [

        ]
        self.z_buffer = []
        self.walls = [
            Wall(-4.0, 20.0, 4.0, 20.0, self.stone2, h=10),
            Wall(-4.0, 8.0, 4.0, 8.0, self.stone2),
            Wall(-4.0, 4.0, -4.0, 8.0, self.stone),
            Wall(4.0, 4.0, 4.0, 8.0, self.stone),

            Wall(-4.0, 4.0, -8.0, 4.0, self.stone2),
            Wall(4.0, 4.0, 8.0, 4.0, self.stone),
            Wall(-8.0, 4.0, -8.0, -4.0, self.stone),
            Wall(8.0, 4.0, 8.0, -4.0, self.stone),

            Wall(4.0, -4.0, 8.0, -4.0, self.stone),
            Wall(-4.0, -4.0, -8.0, -4.0, self.stone),

            Wall(-4.0, -8.0, 4.0, -8.0, self.stone),
            Wall(-4.0, -4.0, -4.0, -8.0, self.stone),
            Wall(4.0, -4.0, 4.0, -8.0, self.stone),
        ]

    def closest_wall(self, pov, ray, walls):
        # print(f"closest_wall(): pov={pov} ray={ray}")
        q_min = -1
        wall_min = None
        t_wall = None
        q_wall = None
        z_wall = None
        for wall in walls:
            t, q, z = wall.top_line.intersect(pov, ray)
            if 0 <= t <= 1 and q > Z_CLIP:
                if q_min < 0 < q:
                    q_min = q
                if q_min >= q:
                    q_min = q
                    wall_min = wall
                    t_wall = t
                    q_wall = q
                    z_wall = z
        # print(f"closest_wall(): t_wall={t_wall} q_wall={q_wall}")
        return wall_min, t_wall, q_wall, z_wall

    def walls_intersecting_ray(self, pov, ray, walls):
        out=[]
        for wall in walls:
            t, q = wall.top_line.intersect(pov, ray)
            if 0 <= t <= 1 and q > Z_CLIP:
                out.append((wall, t, q))

        return out

    def draw(self, screen, player, batch=2):
        size = screen.get_size()
        self.z_buffer = [10000 for i in range(size[0])]

        D = 2.0
        dx = D / size[0]
        x = -D/2 - dx
        for xx in range(0, size[0], batch):
            x += batch*dx
            ray = player.direction.add(player.right_dir.mul(x))

            # self.scan_wall_at(self.big_walls, xx, ray, player, size, screen)
            # self.scan_wall_at(self.walls, xx, ray, player, size, screen)
            self.scan_walls_at(self.walls, xx, batch, ray, player, size, screen)


            # print(f"xx={xx} x={x} dx={dx} ray={ray}")

    def scan_wall_at(self, walls, xx, ray, player, size, screen):
        wall, t, q, z = self.closest_wall(player, ray.normalize(), walls)
        if wall is not None:
            if q<self.z_buffer[xx]:
                self.z_buffer[xx] = q
                top, bottom = wall.lerp(t, player)
                x1, y1 = top.screen(size)
                x2, y2 = bottom.screen(size)

                s, h, y = wall.texture.scale(xx, t, q, x1, y1, x2, y2)
                if s is not None:
                    screen.blit(s, (xx, y))
                    # screen.blit(s, (x1, y))
                    wall.draw(screen, size, player)

    def scan_walls_at(self, walls, xx, batch, ray, player, size, screen):
        walls = self.walls_intersecting_ray(player, ray.normalize(), walls)
        if len(walls)>0:
            sorted_walls = sorted(walls, key=lambda x: x[2], reverse=True)
            # print(f"sorted_walls={sorted_walls}")
            for (wall, t, q) in sorted_walls:
                # if q<self.z_buffer[xx]:
                #     self.z_buffer[xx] = q
                    top, bottom = wall.lerp(t, player)
                    x1, y1 = top.screen(size)
                    x2, y2 = bottom.screen(size)

                    s, h, y = wall.texture.scale(xx, batch, t, q, x1, y1, x2, y2)
                    if s is not None:
                        screen.blit(s, (xx, y))
                        # wall.draw(screen, size, player)