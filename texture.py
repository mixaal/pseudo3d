import numpy as np
from PIL import Image
import pygame as pg


class Texture(object):
    def __init__(self, name):
        self.img = pg.image.load(name)
        self.size = self.img.get_size()
        self.sf = []
        pa = pg.PixelArray(self.img)
        for x in range(self.size[0]):
            col = pa[x:x + 1, :].make_surface()
            self.sf.append(col)
        pa.close()

    def scale(self, x1, y1, x2, y2, x3, y3, x4, y4):

        print(f"x1={x1} y1={y1} x2={x2} y2={y2} x3={x3} y3={y3} x4={x4} y4={y4}")
        if x1 > x2:
            (x1, y1, x2, y2) = (x2, y2, x1, y1)
            (x3, y3, x4, y4) = (x4, y4, x3, y3)

        print(f"x1={x1} y1={y1} x2={x2} y2={y2} x3={x3} y3={y3} x4={x4} y4={y4}")

        w = x2 - x1
        if w < 0.001:
            return None, None, None
        h1 = y1 - y4
        h2 = y2 - y3

        dy = (y3 - y4) / w

        abs_w = w
        if abs_w < 0:
            abs_w = -abs_w
        h = h1
        dh = (h2 - h1) / w

        # print(f"h1={h1} h2={h2} w={w} abs_W={abs_w}")
        mh = max(h1, h2)
        if mh < 0:
            mh = -mh

        cx = (x1 + x2) // 2
        cy = y3 + h2 // 2

        sf = pg.Surface((abs_w, mh))

        xx = 0
        dx = self.size[0] / w

        y = 0
        for x in range(int(abs_w)):
            # print(f"x1={x1} x={x} xx={xx} h={h} y={y} dh={dh}")
            s = pg.transform.scale(self.sf[int(xx)], (1, h))
            sf.blit(s, (x, y))
            # pg.draw.line()
            xx += dx
            h += dh
            y += dy

        return sf, cx, cy

# class Texture(object):
#     def __init__(self, name):
#         self.img = Image.open(name)
#         self.size = self.img.size
#         self.mode = self.img.mode
#         self.width, self.height = self.img.size
#
#     def transform(self, x1, y1, x2, y2, x3, y3, x4, y4):
#
#         print(f"transform: x1={x1} y1={y1} x2={x2} y2={y2} x3={x3} y3={y3} x4={x4} y4={y4}")
#         coeffs = find_coeffs(
#             [(self.width, 0), (0, 0), (0, self.height), (self.width, self.height)],
#             [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
#         print(f"transform: coeffs={coeffs}")
#
#         w = x2 - x1
#         if w < 0:
#             w = -w
#         h = y3 - y2
#         if h < 0:
#             h = -h
#
#         tr = self.img.transform((int(w), int(h)), Image.PERSPECTIVE, coeffs,
#                                 Image.BICUBIC)
#
#         data = tr.tobytes()
#         print(f"mode={self.mode} tr={tr}")
#
#         return pg.image.frombytes(data, (tr.width, tr.height), self.mode)
#         # return pg.image.frombytes(data, self.size, "RGBA")
#
#
# def find_coeffs(pa, pb):
#     matrix = []
#     for p1, p2 in zip(pa, pb):
#         matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
#         matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
#
#     A = numpy.matrix(matrix, dtype=numpy.float32)
#     B = numpy.array(pb).reshape(8)
#
#     res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
#     return numpy.array(res).reshape(8)
