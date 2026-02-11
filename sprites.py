import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *

vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.i_frames = Cooldown(500)
        self.i_frames.start()

    def get_keys(self):
        keys = pg.key.get_pressed()

        wasdnum = 0
        if keys[pg.K_w]:
            wasdnum +=1
        if keys[pg.K_a]:
            wasdnum +=1
        if keys[pg.K_s]:
            wasdnum +=1
        if keys[pg.K_d]:
            wasdnum +=1
        match(wasdnum):
            case 1:
                accelcoefficient = 1
            case 2:
                accelcoefficient = 0.7071
            case 3:
                accelcoefficient = 1
            case 4:
                accelcoefficient = 0
        if keys[pg.K_w]:
            self.vel.y -= PLAYERSPEED * accelcoefficient
        if keys[pg.K_a]:
            self.vel.x -= PLAYERSPEED * accelcoefficient
        if keys[pg.K_s]:
            self.vel.y += PLAYERSPEED * accelcoefficient
        if keys[pg.K_d]:
            self.vel.x += PLAYERSPEED * accelcoefficient


        #Adds Friction
        self.vel.x *= FRICTION
        self.vel.y *= FRICTION

        #Moves PLAYERSPEED per second
        if(self.vel.x != 0 or self.vel.y != 0):
            self.pos.x += self.vel.x
            self.pos.y += self.vel.y


    def update(self):
        self.rect.x = WIDTH/2 - (self.vel.x * 5)
        self.rect.y = HEIGHT/2 - (self.vel.y * 5)
        Camera.x = self.pos.x + (self.vel.x * 5)
        Camera.y = self.pos.y + (self.vel.y * 5)

class Mob(Sprite):
    def __init__(self,game,x,y):
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
        self.vel.x += (self.vel.x +(self.game.player.pos.x-self.pos.x)/self.pos.magnitude()*MOBSPEED)*FRICTION
        self.vel.y = (self.vel.y + (self.game.player.pos.y-self.pos.y)/self.pos.magnitude()*MOBSPEED)*FRICTION
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        #Dynamic Camera Based Position
        self.rect.center = (self.pos.x - Camera.x + (WIDTH+TILESIZE)/2 ,self.pos.y - Camera.y + (HEIGHT+TILESIZE)/2)

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        self.rect.center = (self.pos.x - Camera.x + (WIDTH+TILESIZE)/2 ,self.pos.y - Camera.y + (HEIGHT+TILESIZE)/2)


