import pygame as pg
import settings as s

pg.init()
screen = pg.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    

    screen.fill("purple")



    pg.display.flip()

    clock.tick(s.FPS)

pg.quit()