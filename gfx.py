import os

import pygame as pg


def load_image():
    asurf = pg.image.load(os.path.join('data', 'bla.png'))

class Screen(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1280, 1024), pg.SCALED)
        pg.display.set_caption("Wall Fever")
        pg.mouse.set_visible(False)

    def update(self, world, player):
        pg.key.set_repeat(1, 10)
        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))

        clock = pg.time.Clock()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    if event.key == pg.K_UP:
                        player.forward()
                    if event.key == pg.K_DOWN:
                        player.backward()
                    if event.key == pg.K_LEFT:
                        player.rotate(-0.01)
                    if event.key == pg.K_RIGHT:
                        player.rotate(0.01)
                    if event.key == pg.K_a:
                        player.left()
                    if event.key == pg.K_d:
                        player.right()

            clock.tick()
            print(clock.get_fps())

            self.screen.blit(background, (0, 0))
            world.draw(self.screen, player)

            pg.display.flip()

        pg.quit()
