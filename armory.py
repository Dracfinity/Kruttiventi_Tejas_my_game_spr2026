#CREATE WEAPONS HERE TO FIRE

import pygame as pg
from settings import *
from utils import Camera,Cooldown
from random import randint

Sprite = pg.sprite.Sprite
vec = pg.math.Vector2



class BaseProjectile(Sprite):
    BaseStats = {
        "firerate":20,
        "dmg":15,
        "pierce":2,
        "amount":1,
        "speed":15,
    }
    #Global Cooldown
    Cooldown = Cooldown(500);
    Cooldown.start();
    def __init__(self,game,x,y,vel):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/2, TILESIZE/2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vel
        self.pos = vec(x,y)
        self.hits = []
        self.piercing = self.BaseStats['pierce']
    def update(self):
        #Projectile AI
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        #Dynamic Camera Based Position
        self.rect.center = (self.pos.x - Camera.x + (WIDTH+TILESIZE)/2 ,self.pos.y - Camera.y + (HEIGHT+TILESIZE)/2)
        self.killcheck()
    def killcheck(self):
        dx = self.pos.x - self.game.player.pos.x
        dy = self.pos.y - self.game.player.pos.y

        if abs(dx) > WIDTH/2 or abs(dy) > HEIGHT/2:
            self.kill()



class Boomerang(BaseProjectile):
    BaseStats = {
        "firerate":20,
        "dmg":5,
        "pierce":2,
        "amount":1,
        "speed":2,
    }
    #Global Cooldown
    Cooldown = Cooldown(2000);
    Cooldown.start();
    #Initialization
    def __init__(self,game,x,y,vel, arclength):
        BaseProjectile.__init__(self,game,x,y,vel)
        self.image.fill(BLUE)
        #The length of the boomerang curve
        self.arc = 0
        self.arclength = arclength
        self.piercing = self.BaseStats['pierce']
    def update(self):
        #Projectile AI
        self.pos.x += self.vel.x * -0.5*(self.arc - self.arclength/2)
        self.pos.y += self.vel.y * -0.5*(self.arc - self.arclength/2)
        self.arc+=1
        #Dynamic Camera Based Position
        self.rect.center = (self.pos.x - Camera.x + (WIDTH+TILESIZE)/2 ,self.pos.y - Camera.y + (HEIGHT+TILESIZE)/2)
        super().killcheck()

class BurstFire():
    #Basic Stats to change for new stats
    BaseStats = {
        "firerate":50,
        "dmg":3,
        "pierce":1,
        "amount":20,
        "speed":2,
    }
    #Global Cooldown
    Cooldown = Cooldown(2000);
    Cooldown.start();
    def __init__(self,game,x,y,vel,amount):
        self.projectiles = []
        for i in range(amount):
            self.projectiles.append(BaseProjectile(game,x,y,vec(vel.x+randint(-amount,amount)/5,vel.y+randint(-amount,amount)/5)))
    def update(self):
        for i in range(len(self.projectiles)):
            self.projectiles[i].update()

