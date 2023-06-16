import pygame as pg
import random
import settings as s
class Program():
    
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.background_surf = pg.image.load("Galaga\Assets\Background.jpg").convert_alpha()
        self.background_surf = pg.transform.smoothscale(self.background_surf, (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        
        
        
        self.running = True
        self.gameloop(self.running)
        
    def update(self):
        global player
        self.screen.fill("purple")
        
        self.screen.blit(self.background_surf, (0,0))
        
        player.update()
        player.draw(self.background_surf)
        
        
        pg.display.flip()
        self.clock.tick(s.FPS)
        
            
    def gameloop(self, running):
        while running:
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                    print('surface')
                if keys[pg.K_ESCAPE]:
                    running = False
                    
            self.update()
        pg.quit()
        
class Player(pg.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('Galaga/Assets/Ships/Level1.png')
        self.image = pg.transform.smoothscale(self.image, (200, 200))
        self.rect = self.image.get_rect(midbottom = (200, 200))
        
    def input(self):
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_w]:
            self.rect.x += 10
    
    def update(self):
        self.input()
        
player = pg.sprite.GroupSingle()
player.add(Player())
    
#Game Code Here:
Program()
