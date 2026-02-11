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
        self.vel.x *= PLAYERFRICTION
        self.vel.y *= PLAYERFRICTION

        #Moves PLAYERSPEED per second
        if(self.vel.x != 0 or self.vel.y != 0):
            self.pos.x += self.vel.x
            self.pos.y += self.vel.y


    def update(self):
        #Always Centered, and has a dynamic motion based on vel
        self.rect.x = WIDTH/2 - (self.vel.x * 5)
        self.rect.y = HEIGHT/2 - (self.vel.y * 5)

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
        self.pos.x += (self.game.player.pos.x-self.pos.x+400+(TILESIZE/2))
        #Dynamic Camera Based Position
        self.rect.center = (self.pos.x - self.game.player.pos.x,self.pos.y - self.game.player.pos.y)

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
        self.rect.center = (self.pos.x - self.game.player.pos.x,self.pos.y - self.game.player.pos.y)


