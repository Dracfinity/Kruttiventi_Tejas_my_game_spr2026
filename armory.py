#CREATE WEAPONS HERE TO FIRE

import pygame as pg
from settings import *
from utils import Camera
from random import randint

Sprite = pg.sprite.Sprite
vec = pg.math.Vector2

class BaseProjectile(Sprite):
    def __init__(self,game,x,y,vel):
        print("Firing")
        self.groups = game.all_sprites,
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/2, TILESIZE/2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vel
        self.pos = vec(x,y)
    def update(self):
        #Projectile AI
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        #Dynamic Camera Based Position
        self.rect.center = (self.pos.x - Camera.x + (WIDTH+TILESIZE)/2 ,self.pos.y - Camera.y + (HEIGHT+TILESIZE)/2)
        self.killcheck()
    def killcheck(self):
        if (-1*WIDTH/2 > self.pos.x-self.game.player.pos.x or self.pos.x-self.game.player.pos.x > WIDTH/2) and (-1/2*HEIGHT > self.pos.y-self.game.player.pos.y or self.pos.y-self.game.player.pos.y > -1/2*HEIGHT):
            self.kill()

class Boomerang(BaseProjectile):
    def __init__(self,game,x,y,vel, arclength):
        BaseProjectile.__init__(self,game,x,y,vel)
        self.image.fill(BLUE)
        self.arc = 0
        self.arclength = arclength
    def update(self):
        #Projectile AI
        self.pos.x += self.vel.x * -1*(self.arc - self.arclength/2)
        self.pos.y += self.vel.y * -1*(self.arc - self.arclength/2)
        self.arc+=1
        #Dynamic Camera Based Position
        self.rect.center = (self.pos.x - Camera.x + (WIDTH+TILESIZE)/2 ,self.pos.y - Camera.y + (HEIGHT+TILESIZE)/2)
        super().killcheck()

class Shotgun():
    def __init__(self,game,x,y,vel):
        self.projectiles = []
        for i in range(10):
            self.projectiles.append(BaseProjectile(game,x,y,vec(vel.x,vel.y+randint(-5,5)/5)))
    def update(self):
        for i in range(len(self.projectiles)):
            self.projectiles[i].update()

