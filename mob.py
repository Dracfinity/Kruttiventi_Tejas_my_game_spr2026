from settings import *
import pygame as pg
from utils import *

vec = pg.math.Vector2

class BaseMob(Sprite):
    def __init__(self,game,x,y):
        #Initialization of the Mob Class
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
    def update(self):
        #Mob AI
        self.vel.x = (self.vel.x +((self.game.player.pos.x-self.pos.x)/self.pos.magnitude())*MOBSPEED)*FRICTION
        self.vel.y = (self.vel.y + ((self.game.player.pos.y-self.pos.y)/self.pos.magnitude())*MOBSPEED)*FRICTION
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        #Dynamic Camera Based Position
        self.rect.center = (self.pos.x - Camera.x + (WIDTH+TILESIZE)/2 ,self.pos.y - Camera.y + (HEIGHT+TILESIZE)/2)