from settings import *
import pygame as pg
from utils import *
from random import randint

vec = pg.math.Vector2

class Spawner():
    def __init__(self,game):
        self.time = 0
        self.game = game
        self.BaseMobCooldown = Cooldown(1000)
        self.TankMobCooldown = Cooldown(5000)
    def update(self):
        self.time = pg.time.get_ticks();
        #print(self.handledmobs)
        #BaseMob
        if self.BaseMobCooldown.ready():
            for i in range(min(int(self.time/1000),20)):
                match(randint(0,3)):
                    case 0:
                        BaseMob(self.game,0,randint(0,HEIGHT))
                    case 1:
                        BaseMob(self.game,randint(0,WIDTH),0)
                    case 2:
                        BaseMob(self.game,WIDTH,randint(0,HEIGHT))
                    case 4:
                        BaseMob(self.game,randint(0,WIDTH),HEIGHT)
            self.BaseMobCooldown.start();
        if self.TankMobCooldown.ready():
            for i in range(max(0,min(int(self.time/10000)-2,20))):
                match(randint(0,3)):
                    case 0:
                        TankMob(self.game,0,randint(0,HEIGHT))
                    case 1:
                        TankMob(self.game,randint(0,WIDTH),0)
                    case 2:
                        TankMob(self.game,WIDTH,randint(0,HEIGHT))
                    case 4:
                        TankMob(self.game,randint(0,WIDTH),HEIGHT)
            self.TankMobCooldown.start();
                
        

class BaseMob(Sprite):
    def __init__(self,game,x,y):
        #Initialization of the Mob Class
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(self.game.player.pos.x-WIDTH/2+x,self.game.player.pos.y-HEIGHT/2+y)
        self.maxhealth = 50
        self.health = self.maxhealth
    def update(self):
        #Mob AI
        self.pos.x += ((self.game.player.pos.x-self.pos.x)/vec(self.game.player.pos.x-self.pos.x,self.game.player.pos.y-self.pos.y).magnitude())*MOBSPEED
        self.pos.y += ((self.game.player.pos.y-self.pos.y)/vec(self.game.player.pos.x-self.pos.x,self.game.player.pos.y-self.pos.y).magnitude())*MOBSPEED
        #Dynamic Camera Based Position
        self.rect.center = (self.pos.x - Camera.x + (WIDTH+TILESIZE)/2 ,self.pos.y - Camera.y + (HEIGHT+TILESIZE)/2)
        if self.health <= 0:
            self.kill()
        else:
            self.image.fill((int((self.health*255)/self.maxhealth),0,0))

class TankMob(Sprite):
    def __init__(self,game,x,y):
        #Initialization of the Mob Class
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE*2, TILESIZE*2))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(self.game.player.pos.x-WIDTH/2+x,self.game.player.pos.y-HEIGHT/2+y)
        self.maxhealth = 1000
        self.health = self.maxhealth
    def update(self):
        #Mob AI
        self.pos.x += ((self.game.player.pos.x-self.pos.x)/vec(self.game.player.pos.x-self.pos.x,self.game.player.pos.y-self.pos.y).magnitude())*MOBSPEED/3
        self.pos.y += ((self.game.player.pos.y-self.pos.y)/vec(self.game.player.pos.x-self.pos.x,self.game.player.pos.y-self.pos.y).magnitude())*MOBSPEED/3
        #Dynamic Camera Based Position
        self.rect.center = (self.pos.x - Camera.x + (WIDTH+TILESIZE)/2 ,self.pos.y - Camera.y + (HEIGHT+TILESIZE)/2)
        if self.health <= 0:
            self.kill()
            
        else:
            self.image.fill((int((self.health*200)/self.maxhealth),int((self.health*200)/self.maxhealth),int((self.health*200)/self.maxhealth)))