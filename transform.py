from math import cos, sin, sqrt

Z_CLIP = 1.0
Z_F = 1.0


class Point3d(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def normalize(self):
        d = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        if d == 0.0:
            return Point3d(0.0, 0.0, 0.0)
        return Point3d(self.x / d, self.y / d, self.z / d)

    def transform(self, pov):
        x = self.x - pov.position.x
        y = self.y - pov.position.y
        z = self.z - pov.position.z

        d1 = pov.right_dir.x * pov.right_dir.x + pov.right_dir.y * pov.right_dir.y + pov.right_dir.z * pov.right_dir.z
        d2 = pov.direction.x * pov.direction.x + pov.direction.y * pov.direction.y + pov.direction.z * pov.direction.z
        c1 = (x * pov.right_dir.x + y * pov.right_dir.y + z * pov.right_dir.z) / d1
        c2 = (x * pov.direction.x + y * pov.direction.y + z * pov.direction.z) / d2

        return Point3d(c1, y, c2)

    def mul(self, k):
        return Point3d(self.x * k, self.y * k, self.z * k)

    def add(self, v):
        return Point3d(self.x + v.x, self.y + v.y, self.z + v.z)

    def sub(self, v):
        return Point3d(self.x - v.x, self.y - v.y, self.z - v.z)

    def rotate(self, a):
        x = self.x
        z = self.z
        return Point3d(x * cos(a) + z * sin(a), 0, -x * sin(a) + z * cos(a))

    def screen(self, screen_size):
        sx = screen_size[0] / 2
        sy = screen_size[1] / 2
        f = Z_F
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
        self.right_dir = Point3d(1.0, 0.0, 0.0)

    def forward(self, step=0.1):
        self.position.x += self.direction.x * step
        self.position.y += self.direction.y * step
        self.position.z += self.direction.z * step

    def backward(self, step=0.1):
        self.position.x -= self.direction.x * step
        self.position.y -= self.direction.y * step
        self.position.z -= self.direction.z * step

    def left(self, step=0.1):
        self.position.x -= self.right_dir.x * step
        self.position.y -= self.right_dir.y * step
        self.position.z -= self.right_dir.z * step

    def right(self, step=0.1):
        self.position.x += self.right_dir.x * step
        self.position.y += self.right_dir.y * step
        self.position.z += self.right_dir.z * step

    def rotate(self, a):
        self.right_dir = self.right_dir.rotate(a)
        self.direction = self.direction.rotate(a)


def _lerp(a, b, t):
    return a + (b - a) * t


def lerp(p1, p2, t):
    return Point3d(_lerp(p1.x, p2.x, t), _lerp(p1.y, p2.y, t), _lerp(p1.z, p2.z, t))


class Line(object):
    def __init__(self, x1, z1, x2, z2):
        self.x1 = x1
        self.z1 = z1
        self.x2 = x2
        self.z2 = z2

    def intersect(self, pov, ray):
        x1Px = self.x1 - pov.position.x
        z1Pz = self.z1 - pov.position.z
        dz = self.z2 - self.z1
        dx = self.x2 - self.x1
        d = ray.x * dz - ray.z * dx
        t = -1.0
        q = -1.0
        if d != 0.0:
            t = (ray.z * x1Px - ray.x * z1Pz) / d
        q = (x1Px + t * dx) / ray.x
        return t, q

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
