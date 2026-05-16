import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
from os import path
from armory import *
from math import sqrt
from modals import *

vec = pg.math.Vector2



class Player(Sprite):
    def __init__(self, game, x, y):
        #Basics
        self.groups = game.all_sprites
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.surface.Surface((TILESIZE,TILESIZE))
        self.rect = pg.rect.Rect(0,0,TILESIZE,TILESIZE)
        self.image.fill((0,255,255));
        #Movement
        self.vel = vec(1,0)
        self.pos = vec(x,y) * TILESIZE
        #Hitbox
        self.hit_rect = PLAYER_HIT_RECT
        #Immunity Frames for damage
        self.i_frames = Cooldown(500)
        self.i_frames.start()
        #frames for animated updates
        self.last_update = 0
        self.current_frame = 0
        #different actions and states the player can be in
        self.state = {
            "moving":False,
            "idling":False,
            "onground":False,
        }
        #Settings imported to be dynamically customizable
        self.FRICTION = FRICTION;
        self.SPEED = PLAYERSPEED;
        self.maxhealth = PLAYERHEALTH;
        self.health = self.maxhealth;
        #Armory
        self.armory = Armory(self.game)
        #Experience and Levels
        self.level = 1;
        self.exp = 0;
        self.exptolvlup = self.level**3
        #Health
        self.health = 100;
        self.canHeal = True;
        #FireRate
        self.firerate = Cooldown(500)
        self.firerate.start()

    def get_keys(self):
        #movement
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vel.y -= PLAYERSPEED*self.SPEED
        if keys[pg.K_a]:
            self.vel.x -= PLAYERSPEED*self.SPEED
        if keys[pg.K_s]:
            self.vel.y += PLAYERSPEED*self.SPEED
        if keys[pg.K_d]:
            self.vel.x += PLAYERSPEED*self.SPEED


        #Adds Friction
        self.vel.x *= self.FRICTION
        self.vel.y *= self.FRICTION

        #Moves PLAYERSPEED per second
        if(self.vel.x != 0 or self.vel.y != 0):
            self.pos.x += self.vel.x
            self.pos.y += self.vel.y

    def update(self):
        #Dynamic Camera System to allow to have the camera follow you
        Camera.x = self.pos.x
        Camera.y = self.pos.y
        self.hit_rect.centerx = self.rect.centerx
        self.hit_rect.centery = self.rect.centery
        self.rect.x = WIDTH/2
        self.rect.y = HEIGHT/2
        self.game.screen.blit(self.image,self.rect)
        self.levelhandle()
        self.armory.handle()

    
    def levelhandle(self):
        if(self.exp >= self.exptolvlup):
            self.exp -= self.exptolvlup;
            LevelUp(self.game)
            self.level += 1;
            self.exptolvlup = self.level**3

        
                
                


