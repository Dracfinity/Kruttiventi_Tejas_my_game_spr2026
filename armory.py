import pygame as pg
from settings import *
from utils import Camera,Cooldown
from random import randint

Sprite = pg.sprite.Sprite
vec = pg.math.Vector2

class BaseProjectile(Sprite):
    def __init__(self,game,x,y,w,h):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((w, h),pg.SRCALPHA)
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.hits = []
    def clear(self):
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
    def draw(self):
        self.rect.center = (self.pos.x - Camera.x + (WIDTH+TILESIZE)/2 ,self.pos.y - Camera.y + (HEIGHT+TILESIZE)/2)
        self.game.screen.blit(self.image)

class DurationProjectile(BaseProjectile):
    #Stats Needed
    #BaseStats = {
    #    "dmg":,
    #    "cooldown":,
    #    "duration":,
    #    "dmgtick":,
    #}
    #
    def __init__(self,game,x,y,w,h,duration):
        BaseProjectile.__init__(self,game,x,y,w,h)
        self.duration = duration
        self.begintime = pg.time.get_ticks()
        
    def killcheck(self):
        if self.duration < pg.time.get_ticks()-self.begintime:
            self.kill()
    
class Earthquake(DurationProjectile):
    BaseStats = {
        "dmg": 100,
        "cooldown": Cooldown(2000),
        "duration": 200,
        "dmgtick": 10,
    }
    BaseStats["cooldown"].start()
    def __init__(self,game,x,y):
        self.dmg = Earthquake.BaseStats["dmg"]
        self.dmgtick = Cooldown(float(Earthquake.BaseStats["dmgtick"]))
        self.size = TILESIZE*5
        super().__init__(game,x,y,self.size,self.size,Earthquake.BaseStats["duration"])
        self.lines = []
        for i in range(25):
            self.lines.append([vec(randint(int(0.1*self.size),int(self.size*0.9)),randint(int(0.1*self.size),int(self.size*0.9))),vec(randint(int(-0.1*self.size),int(self.size*0.1)),randint(int(-0.1*self.size),int(self.size*0.1)))])
    
    def update(self):
        self.killcheck()
        self.clear()
        for i in self.lines:
            pg.draw.lines(self.image,(150,50,0),False,((self.size/2,self.size/2),(i[0].x,i[0].y),(i[1].x+i[0].x,i[1].y+i[0].y)),5)
        pg.draw.circle(self.image,(100,20,0),(self.size/2,self.size/2),self.size*0.1,0)
        self.draw()
        self.collide()
    def collide(self):
        hits = pg.sprite.spritecollide(self,self.game.all_mobs,False)
        for i in hits:
            if self.dmgtick.ready():
                i.health -= self.dmg
                self.dmgtick.start()

class RelativeDuration(DurationProjectile):
    def __init__(self,game,w,h,duration):
        DurationProjectile.__init__(self,game,game.player.pos.x,game.player.pos.x,w,h,duration)
    def update(self):
        self.pos = self.game.player.pos

class Tornado(RelativeDuration):
    BaseStats = {
        "dmg": 5,
        "cooldown": Cooldown(1000),
        "duration": 1000,
        "dmgtick": 20,
    }
    def __init__(self,game):
        self.dmg = Tornado.BaseStats["dmg"]
        self.size = TILESIZE*4
        self.dmgtick = Cooldown(float(Tornado.BaseStats["dmgtick"]))
        RelativeDuration.__init__(self,game,self.size,self.size,Tornado.BaseStats['duration'])
        self.lines = 10
    def update(self):
        self.killcheck()
        super().update()
        self.clear()
        for i in range(self.lines):
            pg.draw.circle(self.image,(255,255,255,150),(self.size/2+randint(-2,2),self.size/2+randint(-2,2)),(self.size*i)/(self.lines*2)-2,1);
        self.draw()
        self.collide()
    def collide(self):
        if self.dmgtick.ready():
            hits = pg.sprite.spritecollide(self,self.game.all_mobs,False)
            for i in hits:
                i.health -= self.dmg
                self.dmgtick.start()

class RelativeDirectionDuration(RelativeDuration):
    def __init__(self,game,w,h,duration):
        DurationProjectile.__init__(self,game,game.player.pos.x,game.player.pos.x,w,h,duration)
        try:
            self.dir = self.game.player.vel.normalize()
        except:
            self.dir = vec(1,0)
    def update(self):
        super().update()
        try:
            self.dir = self.game.player.vel.normalize()
        except:
            self.dir = vec(1,0)

class Tsunami(RelativeDirectionDuration):
    #BaseStats
    BaseStats = {
        "dmg": 100,
        "cooldown": Cooldown(3000),
        "duration": 500,
        "dmgtick": 20,
    }
    def __init__(self,game):
        self.dmg = Tsunami.BaseStats["dmg"]
        self.size = TILESIZE*25
        self.dmgtick = Cooldown(float(Tsunami.BaseStats["dmgtick"]))
        RelativeDuration.__init__(self,game,self.size,self.size,Tsunami.BaseStats['duration'])
        self.width = 0.05
    def update(self):
        self.killcheck()
        super().update()
        self.clear()
        pg.draw.polygon(self.image,(100,100,255),[(self.size/2,self.size/2),(self.size/2+(self.dir.x*self.size/2)-(self.dir.y/self.width),self.size/2+(self.dir.y*self.size/2)+(self.dir.x/self.width)),(self.size/2+(self.dir.x*self.size/2)+(self.dir.y/self.width),self.size/2+(self.dir.y*self.size/2)-(self.dir.x/self.width))])
        self.draw()
        self.collide()
    #Collide, Rect then Mask
    def collide(self):
        if self.dmgtick.ready():
            hits = pg.sprite.spritecollide(self,self.game.all_mobs,False)
            self.mask = pg.mask.from_surface(self.image)
            for i in hits:
                if pg.sprite.collide_mask(self,i) != None:
                    i.health -= self.dmg
                    self.dmgtick.start()