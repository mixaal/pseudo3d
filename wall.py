import pygame as pg

from texture import Texture
from transform import Point3d, Line, lerp


class Wall(object):
    def __init__(self, x1, z1, x2, z2, texture):
        self.top_line = Line(x1, z1, x2, z2)

        self.p1 = Point3d(x1, -0.8, z1)
        self.p2 = Point3d(x2, -0.8, z2)
        self.p3 = Point3d(x2, 1.7, z2)
        self.p4 = Point3d(x1, 1.7, z1)
        self.texture = texture

    def lerp(self, t, player):
        bottom = lerp(self.p1, self.p2, t).transform(player)
        top = lerp(self.p4, self.p3, t).transform(player)
        return top, bottom


    def draw(self, screen, size, player):
        p1 = self.p1.transform(player)
        p2 = self.p2.transform(player)
        p3 = self.p3.transform(player)
        p4 = self.p4.transform(player)

        visible, xs, zs, xe, ze = Line(p1.x, p1.z, p2.x, p2.z).clip()

        if not visible:
            return

        p2.x = xs
        p2.z = zs

        p1.x = xe
        p1.z = ze

        p3.x = xs
        p3.z = zs

        p4.x = xe
        p4.z = ze

        (x1, y1) = p1.screen(size)
        (x2, y2) = p2.screen(size)
        (x3, y3) = p3.screen(size)
        (x4, y4) = p4.screen(size)
        pg.draw.line(screen, (0, 0, 255), (x1, y1), (x2, y2))
        pg.draw.line(screen, (0, 200, 0), (x2, y2), (x3, y3))
        pg.draw.line(screen, (255, 0, 0), (x3, y3), (x4, y4))
        pg.draw.line(screen, (100, 100, 100), (x4, y4), (x1, y1))

