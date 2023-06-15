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
    
    screen.fill("black")

#Game Code Here:
    keys = pg.key.get_pressed()
    def pressed(key):
        return keys[pg.K_ + key]

    if keys[pg.K_w] :
        pg.player_pos.y -= 300 * dt
    pg.display.flip()

    clock.tick(s.FPS)
    dt = clock.tick(60) / 1000
pg.quit()