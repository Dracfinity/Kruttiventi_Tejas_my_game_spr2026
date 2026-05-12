import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
from os import path
from armory import *
from math import sqrt
from modals import *

vec = pg.math.Vector2



def collide_hit_rect(one,two):
    #detect collisions
    return one.hit_rect.colliderect(two.rect)

    


class Player(Sprite):
    def __init__(self, game, x, y):
        #Basics
        self.groups = game.all_sprites
        Sprite.__init__(self,self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "Spritesheet.png"))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
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
        #Health
        self.health = 100;
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
        self.levelhandle()
        self.armory.handle()

    def load_images(self):
        #pull a TILESIZExTILESIZE square out of self.spritesheet
        self.standing_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE), 
                                self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)]
        for frame in self.standing_frames:
            frame.set_colorkey(WHITE)

    
    def levelhandle(self):
        if(self.exp >= self.level**2):
            self.exp -= self.level**2;
            LevelUp(self.game)
            self.level += 1;

        
                
                


