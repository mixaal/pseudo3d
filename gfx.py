import pygame as pg


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
                        player.left()
                    if event.key == pg.K_RIGHT:
                        player.right()

            self.screen.blit(background, (0, 0))
            world.draw(self.screen, player)
            # allsprites.draw(screen)
            pg.display.flip()

        pg.quit()