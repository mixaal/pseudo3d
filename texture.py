import pygame as pg


class Texture(object):
    def __init__(self, name, repeat_x=1.0, repeat_y=1.0):
        self.img = pg.image.load(name)
        self.repeat_x = repeat_x
        self.repeat_y = repeat_y
        self.size = self.img.get_size()
        self.sf = []
        pa = pg.PixelArray(self.img)
        for x in range(self.size[0]):
            col = pa[x:x + 1, :].make_surface()
            self.sf.append(col)
        pa.close()

    def scale(self, xx, batch, t, q, x1, y1, x2, y2):
        if t < 0:
            return None

        idx = int(self.size[0] * self.repeat_x * t)
        idx %= self.size[0]

        # print(f"xx={xx} t={t} q={q} z={z} idx={idx}")

        #h = int(800 / (0.1 + q))
        h = y2 - y1
        s = pg.transform.scale(self.sf[idx], (batch, h))
        return s, h, y1
