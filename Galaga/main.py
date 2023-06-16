import pygame as pg
import random as r
import settings as s
import tkinter as tk


score = 0
dead = False
coins = 0
shipUpgrade = 1
speed = 3

pg.mixer.init()
pg.mixer.music.load("Galaga\Assets\Sequenz.mp3")
pg.mixer.music.play(-1)

def Highscore():
    HS = open("Galaga\Highscore.txt", "r+")
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
        self.cooldown_count2 = 0
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
        global speed
        ShipUpgradeCosts = [3, 5, 8, 13, 21, 34, 51]
        
        self.cooldown()
        
        if not dead:
            pg.Surface.blit(self.screen, self.background_surf, (0,0))
            
            self.score_surface = self.fontMini.render(("Score: " + str(score)), False, "White")
            pg.Surface.blit(self.screen, self.score_surface, (s.SCREEN_WIDTH - 1500, 50))
            
            self.coins_surface = self.fontMini.render('Coins: ' + str(coins), False, "Yellow")
            pg.Surface.blit(self.screen, self.coins_surface, (s.SCREEN_WIDTH - 1500, 100))
            
            self.text_surface = self.fontMini.render('Ship Upgrade Cost. ('+ str(ShipUpgradeCosts[shipUpgrade - 1]) +')', False, "Yellow")
            pg.Surface.blit(self.screen, self.text_surface, (s.SCREEN_WIDTH-780, 100))
            
            self.shop_surface = self.fontMini.render('Press M to purchase ship upgrade. ('+ str(shipUpgrade) +')', False, "White")
            pg.Surface.blit(self.screen, self.shop_surface, (s.SCREEN_WIDTH-780, 50))
            
            HS = open("Galaga\Highscore.txt", "r+")

            self.highScore_surface = self.fontMini.render("Highscore: " + str(HS.read()), False, "White")
            pg.Surface.blit(self.screen, self.highScore_surface, (s.SCREEN_WIDTH - 1300, 50))
            
            
            
            self.keys = pg.key.get_pressed()
            if self.keys[pg.K_m] and coins >= ShipUpgradeCosts[shipUpgrade - 1]:
                coins -= ShipUpgradeCosts[shipUpgrade - 1]
                shipUpgrade += 1
            
            player.update()
            player.draw(self.screen)
            
            bullet.update()
            bullet.draw(self.screen)
            
            if self.cooldown_count == 0:
                enemy.add(Enemy())
                self.cooldown_count += 1
            if self.cooldown_count2 == 0:
                speed += 1
                self.cooldown_count2 += 1
            
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
            
            HS = open("Galaga\Highscore.txt", "r+")

            self.highScore_surface = self.font.render("Highscore: " + str(HS.read()), False, "White")
            pg.Surface.blit(self.screen, self.highScore_surface, (20, 350))

            self.coins_surface = self.font.render('Coins: ' + str(coins), False, "Yellow")
            pg.Surface.blit(self.screen, self.coins_surface, (20, 500))

            self.text_surface2 = self.fontMini.render('Press R To Retry', False, "White")
            pg.Surface.blit(self.screen, self.text_surface2, (20, s.SCREEN_HEIGHT - 60))

            #Right Side
            self.shop_surface = self.fontMini.render('Press M to purchase ship upgrade. ('+ str(shipUpgrade) +')', False, "White")
            pg.Surface.blit(self.screen, self.shop_surface, (s.SCREEN_WIDTH-780, 50))

            
            #Shop                                                                        <--- Add a shooting rate upgrad


        
        pg.display.flip()
        self.clock.tick(s.FPS)
        
    def cooldown(self):
        if self.cooldown_count >= 120:
            self.cooldown_count = 0
        elif self.cooldown_count > 0:
            self.cooldown_count += 1
        if self.cooldown_count2 >= 900:
            self.cooldown_count2 = 0
        elif self.cooldown_count2 > 0:
            self.cooldown_count2 += 1
        
#Gameloop here:
    def gameloop(self, running):
        global dead
        global score
        global coins
        while running:

            Highscore()
            FileMangager("Galaga\Coins.txt", coins)
            FileMangager("Galaga\ShipLevel.txt", shipUpgrade)

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
                        dead = False
                        
                        
                self.screen.fill('Black')
                    
            self.update()
        pg.quit()
        
class Player(pg.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        global shipUpgrade
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
            self.upgrades()
                
            
    def cooldown(self):
        if self.cooldown_count >= 30:
            self.cooldown_count = 0
        elif self.cooldown_count > 0:
            self.cooldown_count += 1
    
    def update(self):
        global dead
        self.input()
        self.image = pg.image.load('Galaga/Assets/Ships/Level' + str(shipUpgrade) + '.png')
        self.image = pg.transform.smoothscale(self.image, (100, 100))
        
        hit_list2 = pg.sprite.spritecollide(self, enemy, True)
        if len(hit_list2) >= 1:
            dead = True
        
    def upgrades(self):
        global shipUpgrade
        match shipUpgrade:
            case 1:
                bullet.add(Bullet(self.rect, "bullet1"))
                self.cooldown_count += 1
            case 2:
                bullet.add(Bullet(self.rect, "bullet1"))
                bullet.add(Bullet(self.rect, "bullet2"))
                self.cooldown_count += 1
            case 3:
                bullet.add(Bullet(self.rect, "bullet1"))
                bullet.add(Bullet(self.rect, "bullet2"))
                bullet.add(Bullet(self.rect, "bullet3"))
                self.cooldown_count += 1
            case 4:
                bullet.add(Bullet(self.rect, "bullet1"))
                bullet.add(Bullet(self.rect, "bullet2"))
                bullet.add(Bullet(self.rect, "bullet3"))
                bullet.add(Bullet(self.rect, "bullet4"))
                self.cooldown_count += 1
            case 5:
                bullet.add(Bullet(self.rect, "bullet1"))
                bullet.add(Bullet(self.rect, "bullet2"))
                bullet.add(Bullet(self.rect, "bullet3"))
                bullet.add(Bullet(self.rect, "bullet4"))
                bullet.add(Bullet(self.rect, "bullet5"))
                self.cooldown_count += 1
            case 6:
                bullet.add(Bullet(self.rect, "bullet1"))
                bullet.add(Bullet(self.rect, "bullet2"))
                bullet.add(Bullet(self.rect, "bullet3"))
                bullet.add(Bullet(self.rect, "bullet4"))
                bullet.add(Bullet(self.rect, "bullet5"))
                bullet.add(Bullet(self.rect, "bullet6"))
                self.cooldown_count += 1
            case 7:
                bullet.add(Bullet(self.rect, "bullet1"))
                bullet.add(Bullet(self.rect, "bullet2"))
                bullet.add(Bullet(self.rect, "bullet3"))
                bullet.add(Bullet(self.rect, "bullet4"))
                bullet.add(Bullet(self.rect, "bullet5"))
                bullet.add(Bullet(self.rect, "bullet6"))
                bullet.add(Bullet(self.rect, "bullet7"))
                self.cooldown_count += 1
                
    
class Bullet(pg.sprite.Sprite):
    
    def __init__(self, rect2, type):
        super().__init__()

        self.rect2 = rect2
        self.score = score
        self.type = type
        
        match self.type:
            case "bullet1":
                self.image = pg.image.load('Galaga/Assets/Bullet.png')
                self.image = pg.transform.smoothscale(self.image, (50, 50))
                self.rect = self.image.get_rect(topleft = (self.rect2.x + 25, self.rect2.y))
            case "bullet2":
                self.image = pg.image.load('Galaga/Assets/Bullet.png')
                self.image = pg.transform.smoothscale(self.image, (50, 50))
                self.rect = self.image.get_rect(topleft = (self.rect2.x, self.rect2.y))
            case "bullet3":
                self.image = pg.image.load('Galaga/Assets/Bullet.png')
                self.image = pg.transform.smoothscale(self.image, (50, 50))
                self.rect = self.image.get_rect(topleft = (self.rect2.x + 50, self.rect2.y))
            case "bullet4":
                self.image = pg.image.load('Galaga/Assets/Bullet.png')
                self.image = pg.transform.smoothscale(self.image, (50, 50))
                self.rect = self.image.get_rect(topleft = (self.rect2.x - 25, self.rect2.y))
            case "bullet5":
                self.image = pg.image.load('Galaga/Assets/Bullet.png')
                self.image = pg.transform.smoothscale(self.image, (50, 50))
                self.rect = self.image.get_rect(topleft = (self.rect2.x + 75, self.rect2.y))
            case "bullet6":
                self.image = pg.image.load('Galaga/Assets/Bullet.png')
                self.image = pg.transform.smoothscale(self.image, (50, 50))
                self.rect = self.image.get_rect(topleft = (self.rect2.x - 50, self.rect2.y))
            case "bullet7":
                self.image = pg.image.load('Galaga/Assets/Bullet.png')
                self.image = pg.transform.smoothscale(self.image, (50, 50))
                self.rect = self.image.get_rect(topleft = (self.rect2.x + 100, self.rect2.y))
            
        #self.rect2 = self.image.get_rect(topleft = (self.rect2.x + 50, self.rect2.y)) <--- Second bullet? Nah I Have Them In Sprite Group We Can Do It In A Better Fashion
        
    def update(self):
        global score
        global enemy
        global coins
        self.rect.y -= 5
        
        
        hit_list = pg.sprite.spritecollide(self, enemy, True)
        self.score += len(hit_list)
        coins += len(hit_list)
        score = self.score

        
        
class Enemy(pg.sprite.Sprite):
    allSkins = ["Galaga/Assets/Enemies/Red.png", "Galaga/Assets/Enemies/Blue.png", "Galaga/Assets/Enemies/Yellow-Blue.png"
                , "Galaga/Assets/Enemies/Green.png", "Galaga/Assets/Enemies/BigBoy.png"]
    def __init__(self):
        global speed
        self.randomFile = r.choice(self.allSkins)
        super().__init__()
        self.image = pg.transform.rotate(pg.image.load(self.randomFile), 90)
        self.image = pg.transform.smoothscale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft = (r.randint(400, 1400), 200))
        self.speed = speed
        
    def update(self):
        self.rect.y += speed
        
        
        
player = pg.sprite.GroupSingle()
player.add(Player())

bullet = pg.sprite.Group()

enemy = pg.sprite.Group()

Program()
#Functions def
def Finish(score, coins):
    global HS
    oldScore = score
    if score > HS.read():
        HS.write(score)