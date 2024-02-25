import pygame as pg

FOG_BLUE = (190, 190, 250)
FOG_ORANGE = (112, 58, 16)
FOG_BLACK = (0, 0, 0)


def create_fog(pa, fog_color, blend_factor, size):
    fog = []
    print(f"create_fog(): blend_factor={blend_factor} fog_color={fog_color}")
    for x in range(size[0]):
        col = pa[x:x + 1, :]
        for y in range((len(col[0]))):
            # print(f"y={pa[x:x+1,y]}")
            b = (pa[x:x + 1, y][0] & 0xff0000) >> 16
            g = (pa[x:x + 1, y][0] & 0xff00) >> 8
            r = pa[x:x + 1, y][0] & 0xff
            b1 = 1 - blend_factor
            nr = int(r * b1 + fog_color[0] * blend_factor) & 0xff
            ng = int(g * b1 + fog_color[1] * blend_factor) & 0xff
            nb = int(b * b1 + fog_color[2] * blend_factor) & 0xff
            nr <<= 16
            ng <<= 8
            pa[x:x + 1, y] = nr | ng | nb
        f_col = pa[x:x + 1].make_surface()
        fog.append(f_col)
    return fog


class Fog(object):
    def __init__(self, color=FOG_BLACK):
        self.color = color

        self.fog_min = 0.01
        self.fog_max = 0.5
        self.fog_steps = 20
        self.f_dt = (self.fog_max - self.fog_min) / self.fog_steps
        self.fog_dist = 50.0
        self.no_fog = 10.0
        self.fog_dt = (self.fog_dist - self.no_fog) / self.fog_steps

    def create_fog_layers(self, pa, size):
        fog_layers = []
        factor = self.fog_min
        for _ in range(self.fog_steps):
            fog_layers.append(create_fog(pa, self.color, factor, size))
            factor += self.f_dt
        return fog_layers

    def tex_lookup(self, sf, fog_layers, q):
        l = len(fog_layers)
        if q > self.no_fog:
            li = int((q - self.no_fog) / self.fog_dt)
            if li >= l:
                li = l - 1
            return fog_layers[li]
        else:
            return sf
