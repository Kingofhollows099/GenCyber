import pygame as pg
import settings as Settings

pg.init()
screen = pg.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    screen.fill("purple")



    pg.display.flip()

    clock.tick(Settings.FPS)

pg.quit()