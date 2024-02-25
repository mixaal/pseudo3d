import pygame as pg


class Texture(object):
    def __init__(self, name, fog=None, repeat_x=1.0, repeat_y=1.0):
        self.img = pg.image.load(name)
        self.repeat_x = repeat_x
        self.repeat_y = repeat_y
        self.fog = fog
        self.size = self.img.get_size()
        self.sf = []
        self.fog_layers = []
        pa = pg.PixelArray(self.img)

        for x in range(self.size[0]):
            col = pa[x:x + 1, :].make_surface()
            self.sf.append(col)

        if fog is not None:
            self.fog_layers = fog.create_fog_layers(pa, self.size)
        # self.fog_layers = []
        # self.fog_min = 0.01
        # self.fog_max = 0.5
        # self.fog_steps = 20
        # self.f_dt = (self.fog_max - self.fog_min) / self.fog_steps
        # factor = self.fog_min
        # for _ in range(self.fog_steps):
        #     self.fog_layers.append(self.create_fog(pa, FOG_BLACK, factor))
        #     factor += self.f_dt
        #
        # self.fog_layers_len = len(self.fog_layers)
        # self.fog_dist = 50.0
        # self.no_fog = 10.0
        # self.fog_dt = (self.fog_dist - self.no_fog) / self.fog_layers_len
        pa.close()

    # def create_fog(self, pa, fog_color, blend_factor):
    #     fog = []
    #     print(f"create_fog(): blend_factor={blend_factor} fog_color={fog_color}")
    #     for x in range(self.size[0]):
    #         col = pa[x:x + 1, :]
    #         for y in range((len(col[0]))):
    #             # print(f"y={pa[x:x+1,y]}")
    #             b = (pa[x:x + 1, y][0] & 0xff0000) >> 16
    #             g = (pa[x:x + 1, y][0] & 0xff00) >> 8
    #             r = pa[x:x + 1, y][0] & 0xff
    #             b1 = 1 - blend_factor
    #             nr = int(r * b1 + fog_color[0] * blend_factor) & 0xff
    #             ng = int(g * b1 + fog_color[1] * blend_factor) & 0xff
    #             nb = int(b * b1 + fog_color[2] * blend_factor) & 0xff
    #             nr <<= 16
    #             ng <<= 8
    #             pa[x:x + 1, y] = nr | ng | nb
    #         fcol = pa[x:x + 1].make_surface()
    #         fog.append(fcol)
    #     return fog

    def scale(self, xx, batch, t, q, x1, y1, x2, y2):
        if t < 0:
            return None

        idx = int(self.size[0] * self.repeat_x * t)
        idx %= self.size[0]

        # print(f"xx={xx} t={t} q={q} z={z} idx={idx}")

        # h = int(800 / (0.1 + q))
        h = y2 - y1
        tex_lookup = self.sf
        if self.fog is not None:
            tex_lookup = self.fog.tex_lookup(self.sf, self.fog_layers, q)

        s = pg.transform.scale(tex_lookup[idx], (batch, h))
        return s, h, y1
