import pygame as pg
import random as r
import settings as s

cooldown_tracker = 0
score = 0
dead = False

class Program():
    
    def __init__(self):
        global score
        pg.init()
        self.screen = pg.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.background_surf = pg.image.load("Galaga\Assets\Background.jpg").convert_alpha()
        self.background_surf = pg.transform.smoothscale(self.background_surf, (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        self.cooldown_count = 0
        self.font = pg.font.Font(None, 125)
        
        self.running = True
        self.gameloop(self.running)
        
    def update(self):
        global player
        global bullet
        global enemy
        global dead
        
        self.cooldown()
        
        if not dead:
            pg.Surface.blit(self.screen, self.background_surf, (0,0))
            
            self.score_surface = self.font.render(("Score: " + str(score)), False, "White")
            pg.Surface.blit(self.screen, self.score_surface, (s.SCREEN_WIDTH / 2 - 200, 150))
            
            
            player.update()
            player.draw(self.screen)
            
            bullet.update()
            bullet.draw(self.screen)
            
            if self.cooldown_count == 0:
                enemy.add(Enemy())
                self.cooldown_count += 1
            
            enemy.draw(self.screen)
            enemy.update()
        else:
            self.text_surface = self.font.render('You Died', False, "White")
            pg.Surface.blit(self.screen, self.text_surface, (s.SCREEN_WIDTH / 2 - 200, 150))
            self.score_surface = self.font.render(("Score: " + str(score)), False, "White")
            pg.Surface.blit(self.screen, self.score_surface, (s.SCREEN_WIDTH / 2 - 200, 300))
            self.text_surface2 = self.font.render('Press R To Retry', False, "White")
            pg.Surface.blit(self.screen, self.text_surface, (s.SCREEN_WIDTH / 2 - 200, 150))
        
        pg.display.flip()
        self.clock.tick(s.FPS)
        
    def cooldown(self):
        if self.cooldown_count >= 120:
            self.cooldown_count = 0
        elif self.cooldown_count > 0:
            self.cooldown_count += 1
        
            
    def gameloop(self, running):
        global dead
        global score
        while running:
            if not dead:
                keys = pg.key.get_pressed()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                        print('surface')
                    if keys[pg.K_ESCAPE]:
                        running = False
            else:
                keys = pg.key.get_pressed()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    if keys[pg.K_ESCAPE]:
                        running = False
                    if keys[pg.K_r]:
                        score = 0
                        dead = False
                        
                        
                self.screen.fill('Black')
                    
            self.update()
        pg.quit()
        
class Player(pg.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('Galaga/Assets/Ships/Level1.png')
        self.image = pg.transform.smoothscale(self.image, (100, 100))
        self.clock = pg.time.Clock()
        self.cooldown_count = 0
        self.rect = self.image.get_rect(midbottom = (s.SCREEN_WIDTH / 2, s.SCREEN_HEIGHT / 1.2))
        
    def input(self):
        global bullet
        global enemy
        self.cooldown()
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_a]:
            self.rect.x -= 10
        if self.keys[pg.K_d]:
            self.rect.x += 10
        if self.keys[pg.K_SPACE] and self.cooldown_count == 0:
            bullet.add(Bullet(self.rect))
            self.cooldown_count += 1
                
            
    def cooldown(self):
        if self.cooldown_count >= 30:
            self.cooldown_count = 0
        elif self.cooldown_count > 0:
            self.cooldown_count += 1
    
    def update(self):
        global dead
        self.input()
        
        hit_list2 = pg.sprite.spritecollide(self, enemy, True)
        if len(hit_list2) >= 1:
            dead = True
        
class Bullet(pg.sprite.Sprite):
    
    def __init__(self, rect2):
        super().__init__()
        self.image = pg.image.load('Galaga/Assets/Bullet.png')
        self.image = pg.transform.smoothscale(self.image, (50, 50))
        self.rect2 = rect2
        self.score = score
        self.rect = self.image.get_rect(topleft = (self.rect2.x + 20, 750))
        
    def update(self):
        global score
        global enemy
        self.rect.y -= 5
        
        hit_list = pg.sprite.spritecollide(self, enemy, True)
        self.score += len(hit_list)    
        score = self.score    
        
        #print(self.score)
class Enemy(pg.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('Galaga/Assets/Bullet.png')
        self.image = pg.transform.smoothscale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft = (r.randint(100, 1820), 200))
        
    
    def update(self):
        self.rect.y += 3
        
player = pg.sprite.GroupSingle()
player.add(Player())

bullet = pg.sprite.Group()

enemy = pg.sprite.Group()
    
#Game Code Here:
Program()
