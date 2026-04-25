import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
from os import path
from armory import *

vec = pg.math.Vector2



def collide_hit_rect(one,two):
    #detect collisions
    return one.hit_rect.colliderect(two.rect)

    


class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self,self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "Spritesheet.png"))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vel = vec(1,0)
        self.pos = vec(x,y) * TILESIZE
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
        self.stats = {
            "dmg": 1,
            "firerate": 100,
            "speed": 1,
            "amount": 1,
        }
        self.armory = Armory(self.game)
        self.armory.upgrade("Landslide")
        #FireRate
        self.firerate = Cooldown(500)
        self.firerate.start()

    def get_keys(self):
        #movement
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

    def state_handle(self):
        #Handle States and move around different states
        if self.vel != vec(0,0):
            self.state['moving'] = False
            self.state['idling'] = True
        else:
            self.state['moving'] = True
            self.state['idling'] = False

    def update(self):
        #Dynamic Camera System to allow to have the camera follow you
        Camera.x = self.pos.x
        Camera.y = self.pos.y
        self.hit_rect.centerx = self.rect.centerx
        self.hit_rect.centery = self.rect.centery
        self.rect.x = WIDTH/2
        self.rect.y = HEIGHT/2
        self.animate()
        self.armory.handle()

    def load_images(self):
        #pull a TILESIZExTILESIZE square out of self.spritesheet
        self.standing_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE), 
                                self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)]
        for frame in self.standing_frames:
            frame.set_colorkey(WHITE)
        self.dash_frames = [
            
        ]

    def animate(self):
        now = pg.time.get_ticks()
        #Animation of idling for now
        if self.state['idling']:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = pg.transform.rotate(self.standing_frames[self.current_frame], self.vel.angle_to(vec(1,0)))
        
                
                




'''
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        #Dynamic Camera Based Position
        self.rect.center = (self.pos.x - Camera.x + (WIDTH+TILESIZE)/2 ,self.pos.y - Camera.y + (HEIGHT+TILESIZE)/2)
'''
