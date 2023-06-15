import pygame as pg
import random
import settings as s
class Program():
    
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.background_surf = pg.Surface((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        
        
        self.running = True
        self.gameloop(self.running)
        
    def update(self):
        self.screen.fill("purple")
        self.background_surf.fill(s.BACKGROUND_COLOR)
        
    
        pg.Surface.blit(self.screen, self.background_surf, (0, 0))
        self.screen.blit(pg.image.load("Galaga\Assets\Background.jpg").convert_alpha(), (0, 0))
        
        pg.display.flip()
        self.clock.tick(s.FPS)
        
            
    def gameloop(self, running):
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    print('surface')
                    
            self.update()
        pg.quit()
    
    
#Game Code Here:
Program()
