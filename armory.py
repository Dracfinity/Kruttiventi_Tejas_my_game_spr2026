import pygame as pg
from settings import *
from utils import Camera,Cooldown
from random import randint,choices
from math import sin,cos

Sprite = pg.sprite.Sprite
vec = pg.math.Vector2

#allWeapons = ["Earthquake","Tsunami","Tornado","Landslide","Plague"]

class Armory():
    def __init__(self,game):
        self.owned = [[None,0],[None,0],[None,0],[None,0],[None,0],[None,0]]
        self.game = game
    def upgrade(self,weapon):
        for i in range(len(self.owned)):
            if self.owned[i][0] == None or self.owned[i][0] == weapon:
                self.owned[i][0] = weapon
                self.owned[i][1] += 1
    def getOptions(self):
        full = True
        for i in self.owned:
            if i[0] == None:
                full = False;
        if full == False:
            allWeapons = ["Earthquake","Tsunami","Tornado","Landslide","Plague"]
            return choices(allWeapons,None,None,3)

    def handle(self):
        for i in self.owned:
            match(i[0]):
                case None:
                    continue;
                case "Earthquake":
                    if Earthquake.BaseStats["cooldown"].ready():
                        Earthquake.BaseStats["cooldown"].start()
                        Earthquake(self.game,self.pos.x+randint(int(-WIDTH/2),int(WIDTH/2)),self.pos.y+randint(int(-WIDTH/2),int(WIDTH/2)))
                case "Tornado":
                    if Tornado.BaseStats["cooldown"].ready():
                        Tornado.BaseStats["cooldown"].start()
                        Tornado(self.game)
                case "Tsunami":
                    if Tsunami.BaseStats["cooldown"].ready():
                        Tsunami.BaseStats["cooldown"].start()
                        Tsunami(self.game)
                case "Plague":
                    if Plague.BaseStats["cooldown"].ready():
                        Plague.BaseStats["cooldown"].start()
                        Plague(self.game)
                case "Landslide":
                    if Landslide.BaseStats["cooldown"].ready():
                        Landslide.BaseStats["cooldown"].start()
                        Landslide(self.game)

##WeaponStructure
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
    def __init__(self,game,x,y,w,h,duration):
        BaseProjectile.__init__(self,game,x,y,w,h)
        self.duration = duration
        self.begintime = pg.time.get_ticks()
        
    def killcheck(self):
        if self.duration < pg.time.get_ticks()-self.begintime:
            self.kill()

class MassDuration(DurationProjectile):
    def __init__(self,game,w,h,duration,amount):
        DurationProjectile.__init__(self,game,game.player.pos.x,game.player.pos.y,WIDTH,HEIGHT,duration)
        self.projectiles = []
        for i in range(amount):
            self.projectiles.append([vec(WIDTH/2,HEIGHT/2),(w,h),vec(0,0)])#Pos,Size,Vel
    def update(self):
        for i in self.projectiles:
            i[0].x += i[2].x
            i[0].y += i[2].y
        



class RelativeDuration(DurationProjectile):
    def __init__(self,game,w,h,duration):
        DurationProjectile.__init__(self,game,game.player.pos.x,game.player.pos.x,w,h,duration)
    def update(self):
        self.pos = self.game.player.pos
        
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

class SpinningRelativeDuration(RelativeDuration):
    def __init__(self,game,w,h,duration,speed):
        DurationProjectile.__init__(self,game,game.player.pos.x,game.player.pos.x,w,h,duration)
        self.dir = 0
        self.dirvec = vec(1,0)
        self.speed = speed
    def update(self):
        super().update()
        self.dir = (self.dir + self.speed) % 6.14318

##Weapons

class Earthquake(DurationProjectile):
    BaseStats = {
        "dmg": 100,
        "cooldown": Cooldown(1000),
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

class Landslide(SpinningRelativeDuration):
    BaseStats = {
        "dmg": 30,
        "cooldown": Cooldown(6000),
        "duration": 1500,
        "dmgtick": 40,
        "amount": 8,
        "speed": 0.01,
    }
    def __init__(self,game):
        self.dmg = Landslide.BaseStats["dmg"]
        self.size = TILESIZE*12
        self.dmgtick = Cooldown(float(Landslide.BaseStats["dmgtick"]))
        SpinningRelativeDuration.__init__(self,game,self.size,self.size,Landslide.BaseStats['duration'],Landslide.BaseStats['speed'])
        self.spinradius = TILESIZE*5
        self.rockradius = TILESIZE/4
    def update(self):
        self.clear()
        self.killcheck()
        super().update()
        for i in range(Landslide.BaseStats['amount']):
            pg.draw.circle(self.image,(150,100,70),(self.size/2+((sin(self.dir+(6.14*i/Landslide.BaseStats['amount'])))*self.spinradius),self.size/2+((cos(self.dir+(6.14*i/Landslide.BaseStats['amount']))))*self.spinradius),self.rockradius)
        self.draw()
        self.collide()
    def collide(self):
        if self.dmgtick.ready():
            hits = pg.sprite.spritecollide(self,self.game.all_mobs,False)
            self.mask = pg.mask.from_surface(self.image)
            for i in hits:
                if pg.sprite.collide_mask(self,i) != None:
                    i.health -= self.dmg
                    self.dmgtick.start()

class Tornado(RelativeDuration):
    BaseStats = {
        "dmg": 2,
        "cooldown": Cooldown(1000),
        "duration": 1000,
        "dmgtick": 40,
        "size": TILESIZE*4,
        "ultimate": False,
    }
    def __init__(self,game):
        self.dmg = Tornado.BaseStats["dmg"]
        self.size = Tornado.BaseStats['size']
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
        if Tornado.BaseStats['ultimate'] == True:
            self.ultcollide()
        else:
            self.collide()
    def collide(self):
        if self.dmgtick.ready():
            hits = pg.sprite.spritecollide(self,self.game.all_mobs,False)
            for i in hits:
                i.health -= self.dmg
                self.dmgtick.start()
    def ultcollide(self):
        if self.dmgtick.ready():
            hits = pg.sprite.spritecollide(self,self.game.all_mobs,False)
            for i in hits:
                i.health -= self.dmg
                i.effects.append(["Slow", 0.5 ])
                self.dmgtick.start()

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

class Plague(MassDuration):
    BaseStats = {
        "dmg": 5,
        "cooldown": Cooldown(3000),
        "duration": 2000,
        "dmgtick": 20,
    }
    def __init__(self,game):
        MassDuration.__init__(self,game,10,10,Plague.BaseStats['duration'],20)
        self.dmg = Plague.BaseStats['dmg']
        self.dmgtick = Cooldown(Plague.BaseStats['dmgtick'])
        for i in self.projectiles:
            i[2] = vec(randint(-1,1),randint(-1,1))
    def update(self):
        self.killcheck()
        MassDuration.update(self)
        self.clear()
        for i in self.projectiles:
            i[2].x += randint(-10,10)/100
            i[2].y += randint(-10,10)/100
            pg.draw.rect(self.image,(0,150,0),(i[0],i[1]))
        self.draw()
        self.collide()
    def collide(self):
        if self.dmgtick.ready():
            hits = pg.sprite.spritecollide(self,self.game.all_mobs,False)
            self.mask = pg.mask.from_surface(self.image)
            for i in hits:
                if pg.sprite.collide_mask(self,i) != None:
                    i.health -= self.dmg
                    self.dmgtick.start()