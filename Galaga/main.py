import pygame as pg
import random as r
import settings as s
import tkinter as tk


cooldown_tracker = 0
score = 0
dead = False
coins = 0
shipUpgrade = 1

def Highscore():
     HS = open("Highscore.txt", "r+")
     if score > int(HS.read()):
        HS.seek(0)
        HS.write(str(score))

def FileMangager(filepath, value):
    MFile = open(filepath, "r+")
    if MFile != value:
        MFile.write(str(value))
class Program():
 
    def __init__(self):
        global score
        pg.init()
        self.screen = pg.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.background_surf = pg.image.load("Galaga\Assets\Background.jpg").convert_alpha()
        self.background_surf = pg.transform.smoothscale(self.background_surf, (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        self.cooldown_count = 0
        self.font = pg.font.Font(None, 110)
        self.fontMini = pg.font.Font(None, 60)
        
        self.running = True
        self.gameloop(self.running)
        
    def update(self):
        global player
        global bullet
        global enemy
        global dead
        global coins
        global shipUpgrade
        
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

            """
            Deathscreen
            """
            #Left Side
            self.text_surface = self.font.render('You Died', False, "Red")
            pg.Surface.blit(self.screen, self.text_surface, (20, 50))

            self.score_surface = self.font.render("Score: " + str(score), False, "White")
            pg.Surface.blit(self.screen, self.score_surface, (20, 200))
            
            HS = open("Highscore.txt", "r+")

            self.highScore_surface = self.font.render("Highscore: " + str(HS.read), False, "White")
            pg.Surface.blit(self.screen, self.highScore_surface, (20, 350))

            self.coins_surface = self.font.render('Coins: ' + str(coins), False, "Yellow")
            pg.Surface.blit(self.screen, self.coins_surface, (20, 500))

            self.text_surface2 = self.fontMini.render('Press R To Retry', False, "White")
            pg.Surface.blit(self.screen, self.text_surface2, (20, s.SCREEN_HEIGHT - 60))

            #Right Side
            self.shop_surface = self.fontMini.render('Press M to purchase ship upgrade. ('+ str(shipUpgrade) +')', False, "White")
            pg.Surface.blit(self.screen, self.shop_surface, (s.SCREEN_WIDTH-780, 50))

            
            #Shop                                                                        <--- Add a shooting rate upgrade
            ShipUpgradeCosts = [3, 5, 8, 13, 21, 34, 51]

            if self.keys[pg.K_m] and coins >= ShipUpgradeCosts[shipUpgrade - 1]:
                coins -= ShipUpgradeCosts[shipUpgrade - 1]
                shipUpgrade += 1


        
        pg.display.flip()
        self.clock.tick(s.FPS)
        
    def cooldown(self):
        if self.cooldown_count >= 120:
            self.cooldown_count = 0
        elif self.cooldown_count > 0:
            self.cooldown_count += 1
        
#Gameloop here:
    def gameloop(self, running):
        global dead
        global score
        global coins
        while running:

            Highscore()
            FileMangager("Coins.txt", coins)
            FileMangager("ShipLevel.txt", shipUpgrade)

            if not dead:# Alive
                keys = pg.key.get_pressed()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        coins += score // 10
                        running = False
                    if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                        pass
                    if keys[pg.K_ESCAPE]:
                        coins += score // 10
                        running = False
            else: # Dead
                keys = pg.key.get_pressed()
                for event in pg.event.get():
                    if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                        coins += score // 10
                        running = False
                    if keys[pg.K_r]:
                        coins += score // 10
                        score = 0
                        dead = False
                        
                        
                self.screen.fill('Black')
                    
            self.update()
        pg.quit()
        
class Player(pg.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('Galaga/Assets/Ships/Level' + str(shipUpgrade) + '.png')
        self.image = pg.transform.smoothscale(self.image, (100, 100))
        self.clock = pg.time.Clock()
        self.cooldown_count = 0
        self.rect = self.image.get_rect(midbottom = (s.SCREEN_WIDTH / 2, s.SCREEN_HEIGHT / 1.2))
        
    def input(self):
        global bullet
        global enemy
        self.cooldown()
        self.keys = pg.key.get_pressed()
        #Horizontal
        if self.keys[pg.K_a] and self.rect.left > 0:
            self.rect.x -= 10
        if self.keys[pg.K_d] and self.rect.right < s.SCREEN_WIDTH:
            self.rect.x += 10
        #Verticle
        if self.keys[pg.K_w] and self.rect.top > 0:
            self.rect.y -= 7.5
        if self.keys[pg.K_s] and self.rect.bottom < s.SCREEN_HEIGHT:
            self.rect.y += 7.5

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
        self.rect = self.image.get_rect(topleft = (self.rect2.x + 25, self.rect2.y))
        #self.rect2 = self.image.get_rect(topleft = (self.rect2.x + 50, self.rect2.y)) <--- Second bullet?
        
    def update(self):
        global score
        global enemy
        self.rect.y -= 5
        
        hit_list = pg.sprite.spritecollide(self, enemy, True)
        self.score += len(hit_list)
        score = self.score
        
        
class Enemy(pg.sprite.Sprite):
    allSkins = ["Galaga/Assets/Enemies/Red.png", "Galaga/Assets/Enemies/Blue.png", "Galaga/Assets/Enemies/Yellow-Blue.png"
                , "Galaga/Assets/Enemies/Green.png", "Galaga/Assets/Enemies/BigBoy.png"]
    def __init__(self):
        self.randomFile = r.choice(self.allSkins)
        super().__init__()
        self.image = pg.transform.rotate(pg.image.load(self.randomFile), 90)
        self.image = pg.transform.smoothscale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft = (r.randint(100, 1820), 200))
        
     
    def update(self):
        self.rect.y += 3
        
player = pg.sprite.GroupSingle()
player.add(Player())

bullet = pg.sprite.Group()

enemy = pg.sprite.Group()

Program()
#Functions def
def Finish(score, coins):
    
    oldScore = score
    if score > HS.read():
        HS.write(score)