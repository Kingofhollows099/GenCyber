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
        global bullet
        
        pg.Surface.blit(self.screen, self.background_surf, (0,0))
        
        player.update()
        player.draw(self.screen)
        
        bullet.update()
        bullet.draw(self.screen)
        
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
        self.image = pg.transform.smoothscale(self.image, (100, 100))
        self.rect = self.image.get_rect(midbottom = (s.SCREEN_WIDTH / 2, s.SCREEN_HEIGHT / 1.2))
        
    def input(self):
        global bullet
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_a]:
            self.rect.x -= 10
        if self.keys[pg.K_d]:
            self.rect.x += 10
        if self.keys[pg.K_SPACE]:
            bullet.add(Bullet(self.rect))
            
    
    def update(self):
        self.input()
        
class Bullet(pg.sprite.Sprite):
    
    def __init__(self, rect2):
        global player
        super().__init__()
        self.image = pg.image.load('Galaga/Assets/Ships/Level2.png')
        self.image = pg.transform.smoothscale(self.image, (100, 100))
        self.rect2 = rect2
        self.rect = self.image.get_rect(midleft = (self.rect2.x, 800))
        
    def update(self):
        self.rect.y -= 5
    
player = pg.sprite.GroupSingle()
player.add(Player())


bullet = pg.sprite.Group()
    
#Game Code Here:
Program()
