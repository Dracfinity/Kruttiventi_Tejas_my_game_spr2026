import pygame as pg
from settings import *
from utils import Camera,Cooldown
from random import randint,sample,random
from math import sin,cos,sqrt

Sprite = pg.sprite.Sprite
vec = pg.math.Vector2

def Distance(x1,y1,x2,y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)

class Armory():
    def __init__(self,game):
        self.owned = [[None,0],[None,0],[None,0],[None,0],[None,0],[None,0]]
        self.game = game
        self.allWeapons = ["Earthquake","Tsunami","Tornado","Landslide","Plague","Wildfire"]
    def upgrade(self,weapon):
        for i in range(len(self.owned)):
            if self.owned[i][0] == weapon:
                self.owned[i][1] += 1
                return 0;
        for i in range(len(self.owned)):
            if self.owned[i][0] == None:
                self.owned[i][0] = weapon
                self.owned[i][1] += 1
                return 0;
    def getOptions(self):
        full = True;
        for i in self.owned:
            if i[0] == None:
                full = False;
        
        if full == False:
            self.possible = self.allWeapons
            for i in self.owned:
                if i[1] == 7 and i[0] in self.possible:
                    self.possible.remove(i[0])
            return sample(self.possible,k=3)
        else:
            self.possible = [x[0] for x in self.owned if x[1] < 7]
            if len(self.possible) > 3:
                    return sample(self.possible,k=3)
            else:
                while len(self.possible) <= 3:
                    self.possible.append("Full")
                return self.possible
    def getLevel(self,weapon):
        for i in self.owned:
            if i[0] == weapon:
                return i[1]
        return 0;
            

    def handle(self):
        for i in self.owned:
            match(i[0]):
                case None:
                    continue;
                case "Earthquake":
                    if Earthquake.BaseStats["cooldown"].ready():
                        Earthquake.BaseStats["cooldown"].start()
                        Earthquake(self.game,self.game.player.pos.x+randint(int(-WIDTH/2),int(WIDTH/2)),self.game.player.pos.y+randint(int(-WIDTH/2),int(WIDTH/2)))
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
                case "Wildfire":
                    if Wildfire.BaseStats["cooldown"].ready():
                        if Wildfire.BaseStats["ultimate"]:
                            Wildfire.BaseStats["cooldown"].start()
                            Wildfire(self.game)
                            Wildfire(self.game)
                            Wildfire(self.game)
                        else:
                            Wildfire.BaseStats["cooldown"].start()
                            Wildfire(self.game)

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
        DurationProjectile.__init__(self,game,game.player.pos.x,game.player.pos.y,w,h,duration)
    def update(self):
        self.pos = self.game.player.pos
        
class RelativeDirectionDuration(RelativeDuration):
    def __init__(self,game,w,h,duration):
        RelativeDuration.__init__(self,game,w,h,duration)
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
        RelativeDuration.__init__(self,game,w,h,duration)
        #direction facing
        self.dir = 0
        #speed
        self.speed = speed
    def update(self):
        super().update()
        #loops dir from 0 -> 2pi with self.speed per tick
        self.dir = (self.dir + self.speed) % 6.14318

class BulletProjectile(BaseProjectile):
    def __init__(self,game,x,y,w,h,vx,vy):
        BaseProjectile.__init__(self,game,x,y,w,h)
        self.vx = vx
        self.vy = vy
    def update(self):
        BaseProjectile.update(self)
        self.pos.x += self.vx
        self.pos.y += self.vy
    def killcheck(self):
        if self.pos.x < -WIDTH/2 or self.pos.x > WIDTH*1.5 or self.pos.y < -HEIGHT/2 or self.pos.y > HEIGHT*1.5:
            self.kill()

##Weapons

class Wildfire(BulletProjectile):
    BaseStats = {
        "burntier": 0.5,
        "cooldown": Cooldown(500),
        "dmgtick": 40,
        "speed": 10,
        "size":TILESIZE/4,
        "ultimate": False
    }
    def __init__(self,game):
        BulletProjectile.__init__(self,game,game.player.pos.x,game.player.pos.y,Wildfire.BaseStats["size"],Wildfire.BaseStats["size"],(random()-0.5)*2*Wildfire.BaseStats["speed"],(random()-0.5)*2*Wildfire.BaseStats["speed"])
        self.dmgtick = Cooldown(Wildfire.BaseStats["dmgtick"])
        self.dmg = Wildfire.BaseStats["burntier"]
    def update(self):
        BulletProjectile.update(self)
        self.clear()
        self.image.fill((255,100,0))
        self.draw()
        self.collide()
    def collide(self):
        if self.dmgtick.ready():
            hits = pg.sprite.spritecollide(self,self.game.all_mobs,False)
            for i in hits:
                if ["Poison", self.dmg] not in i.effects:
                    i.effects.append(["Poison", self.dmg])
                self.dmgtick.start()
        

class Earthquake(DurationProjectile):
    BaseStats = {
        "dmg": 25,
        "cooldown": Cooldown(1000),
        "duration": 200,
        "dmgtick": 40,
        "size":TILESIZE*5,
        "ultimate": False
    }
    BaseStats["cooldown"].start()
    def __init__(self,game,x,y):
        self.dmg = Earthquake.BaseStats["dmg"]
        self.dmgtick = Cooldown(float(Earthquake.BaseStats["dmgtick"]))
        self.size = Earthquake.BaseStats["size"]
        super().__init__(game,x,y,self.size,self.size,Earthquake.BaseStats["duration"])
        self.lines = []
        #Bunch of lines branching out from center
        for i in range(50):
            self.lines.append([vec(randint(10,90)/100,randint(10,90)/100),vec(randint(-10,10)/100,randint(-10,10)/100)])
    
    def update(self):
        self.killcheck()
        self.clear()
        for i in self.lines:
            pg.draw.lines(self.image,(150,50,0),False,((self.size/2,self.size/2),(i[0].x*self.size,i[0].y*self.size),((i[1].x+i[0].x)*self.size,(i[1].y+i[0].y)*self.size)),3)
        self.draw()
        self.collide()
        if Earthquake.BaseStats["ultimate"] == True:
            self.dmg *= 1.05
    def collide(self):
        if self.dmgtick.ready():
            hits = pg.sprite.spritecollide(self,self.game.all_mobs,False)
            for i in hits:
                i.health -= self.dmg
                self.dmgtick.start()

#Uses a for loop with range amount to create equal circles on a radius around the player, uses mask collide to allow for each circle to collide seperately
class Landslide(SpinningRelativeDuration):
    BaseStats = {
        "dmg": 15,
        "cooldown": Cooldown(6000),
        "duration": 1500,
        "dmgtick": 40,
        "amount": 4,
        "speed": 0.01,
        "spinradius": TILESIZE*5,
        "rockradius": TILESIZE/4,
        "ultimate":False,
    }
    def __init__(self,game):
        self.dmg = Landslide.BaseStats["dmg"]
        self.spinradius = Landslide.BaseStats["spinradius"]
        self.rockradius = Landslide.BaseStats["rockradius"]
        self.size = self.spinradius*2 + self.rockradius*2

        self.dmgtick = Cooldown(float(Landslide.BaseStats["dmgtick"]))
        SpinningRelativeDuration.__init__(self,game,self.size,self.size,Landslide.BaseStats['duration'],Landslide.BaseStats['speed'])
    def update(self):
        self.clear()
        self.killcheck()
        super().update()
        for i in range(Landslide.BaseStats['amount']):
            pg.draw.circle(self.image,(150,100,70),(self.size/2+((sin(self.dir+(6.14*i/Landslide.BaseStats['amount'])))*self.spinradius),self.size/2+((cos(self.dir+(6.14*i/Landslide.BaseStats['amount']))))*self.spinradius),self.rockradius)
        #Ultimate with extra layer
        if Landslide.BaseStats["ultimate"] == True:  
            for i in range(Landslide.BaseStats['amount']):
                pg.draw.circle(self.image,(150,100,70),(self.size/2+((sin(self.dir+(6.14*i/Landslide.BaseStats['amount'])))*(self.spinradius/2)),self.size/2-((cos(self.dir+(6.14*i/Landslide.BaseStats['amount']))))*(self.spinradius/2)),self.rockradius)
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

#The tornado spins around the player and does damage to mobs near it. 
# It uses a rect collide which is mildy innacurate but leagues faster than the amount of maskcollides that the dmgtick could justify
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
                if ["Slow", 0.5] not in i.effects:
                    i.effects.append(["Slow", 0.5])
                self.dmgtick.start()

class Tsunami(RelativeDirectionDuration):
    #BaseStats
    BaseStats = {
        "dmg": 50,
        "cooldown": Cooldown(3000),
        "duration": 500,
        "dmgtick": 40,
        "width": 0.05,
        "ultimate": False,
    }
    def __init__(self,game):
        self.dmg = Tsunami.BaseStats["dmg"]
        self.size = TILESIZE*25
        self.dmgtick = Cooldown(float(Tsunami.BaseStats["dmgtick"]))
        RelativeDuration.__init__(self,game,self.size,self.size,Tsunami.BaseStats['duration'])
        self.width = Tsunami.BaseStats["width"]
    def update(self):
        self.killcheck()
        super().update()
        self.clear()
        pg.draw.polygon(self.image,(100,100,255),[(self.size/2,self.size/2),(self.size/2+(self.dir.x*self.size/2)-(self.dir.y/self.width),self.size/2+(self.dir.y*self.size/2)+(self.dir.x/self.width)),(self.size/2+(self.dir.x*self.size/2)+(self.dir.y/self.width),self.size/2+(self.dir.y*self.size/2)-(self.dir.x/self.width))])
        if Tsunami.BaseStats["ultimate"] == True:   
            pg.draw.polygon(self.image,(100,100,255),[(self.size/2,self.size/2),(self.size/2-(self.dir.x*self.size/2)-(self.dir.y/self.width),self.size/2-(self.dir.y*self.size/2)+(self.dir.x/self.width)),(self.size/2-(self.dir.x*self.size/2)+(self.dir.y/self.width),self.size/2-(self.dir.y*self.size/2)-(self.dir.x/self.width))])
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
        "cooldown": Cooldown(5000),
        "duration": 2000,
        "dmgtick": 40,
        "amount": 10,
        "speed": 1,
        "ultimate":False,
    }
    def __init__(self,game):
        MassDuration.__init__(self,game,10,10,Plague.BaseStats['duration'],Plague.BaseStats['amount'])
        self.dmg = Plague.BaseStats['dmg']
        self.dmgtick = Cooldown(Plague.BaseStats['dmgtick'])
        self.speed = Plague.BaseStats["speed"]
        for i in self.projectiles:
            i[2].x += randint(-10,10)/100 * self.speed
            i[2].y += randint(-10,10)/100 * self.speed
    def update(self):
        self.killcheck()
        MassDuration.update(self)
        self.clear()
        for i in self.projectiles:
            pg.draw.rect(self.image,(0,150,0),(i[0],i[1]))
        self.draw()
        if Plague.BaseStats['ultimate'] == True:
            self.ultcollide()
        else:
            self.collide()
    def collide(self):
        if self.dmgtick.ready():
            hits = pg.sprite.spritecollide(self,self.game.all_mobs,False)
            self.mask = pg.mask.from_surface(self.image)
            for i in hits:
                if pg.sprite.collide_mask(self,i) != None:
                    i.health -= self.dmg
                    self.dmgtick.start()
    def ultcollide(self):
        if self.dmgtick.ready():
            hits = pg.sprite.spritecollide(self,self.game.all_mobs,False)
            for i in hits:
                i.health -= self.dmg
                if ["Poison", 0.25] not in i.effects:
                    i.effects.append(["Poison", 0.25])
                self.dmgtick.start()

