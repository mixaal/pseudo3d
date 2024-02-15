class Point3d(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def transform(self, pov):
        x = self.x - pov.position.x
        y = self.y - pov.position.y
        z = self.z - pov.position.z

        return Point3d(x, y, z)

    def screen(self, screen_size):
        sx = screen_size[0] / 2
        sy = screen_size[1] / 2
        f = 1.0
        xx = self.x * f / (self.z + f)
        yy = self.y * f / (self.z + f)

        # print(f"[{self.x}, {self.y}, {self.z}] ---> {xx}, {yy}")

        xx *= sx
        yy *= sy
        return sx + xx, sy - yy

    def __str__(self):
        return f"P3D[{self.x}, {self.y}, {self.z}]"


class Pov(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.position = Point3d(x, y, z)
        self.direction = Point3d(0.0, 0.0, 1.0)

    def forward(self, step=0.1):
        self.position.x += self.direction.x * step
        self.position.y += self.direction.y * step
        self.position.z += self.direction.z * step

    def backward(self, step=0.1):
        self.position.x -= self.direction.x * step
        self.position.y -= self.direction.y * step
        self.position.z -= self.direction.z * step

    def left(self, step=0.1):
        self.position.x -= self.direction.z * step
        self.position.y += self.direction.y * step
        self.position.z += self.direction.x * step

    def right(self, step=0.1):
        self.position.x += self.direction.z * step
        self.position.y += self.direction.y * step
        self.position.z += self.direction.x * step


class Line(object):
    def __init__(self, x1, z1, x2, z2):
        self.x1 = x1
        self.z1 = z1
        self.x2 = x2
        self.z2 = z2

    def clip(self):
        # return True, self.x1, self.z1, self.x2, self.z2

        if self.z1 < 0 and self.z2 < 0:
            # Nic neni videt
            return False, None, None, None, None

        if self.z1 >= 0 and self.z2 >= 0:
            # Vsechno je videt
            return True, self.x1, self.z1, self.x2, self.z2

        # Castecne videt, je potreba orezat
        xs = self.x1
        zs = self.z1
        xe = self.x2
        ze = self.z2

        flipped = False
        if zs > ze:
            flipped = True
            xs = self.x2
            zs = self.z2
            xe = self.x1
            ze = self.z1

        dx = xe - xs
        dz = ze - zs

        #
        #     dx / dz = x' / pe.z
        #
        x_clip = ze * dx / dz
        xs = xe - x_clip

        if flipped:
            return True, xe, ze, xs, 0
        else:
            return True, xs, 0, xe, ze
