from settings import *
import pygame as pg
from utils import *
from random import randint

vec = pg.math.Vector2

class Spawner():
    def __init__(self,game):
        self.time = 0
        self.game = game
        self.BaseMobCooldown = Cooldown(1000)
        self.NormalMobCooldown = Cooldown(5000)
        self.DashMobCooldown = Cooldown(3000)
        self.TankMobCooldown = Cooldown(10000)
        self.StrongMobCooldown = Cooldown(2000)
    def update(self):
        self.time = pg.time.get_ticks();
        #print(self.handledmobs)
        if len(self.game.all_mobs) < MOB_CAP:
            if self.BaseMobCooldown.ready():
                for i in range(self.getAmount(0,40,3)):
                    self.spawn(WeakMob)
                self.BaseMobCooldown.start();
            if self.NormalMobCooldown.ready():
                for i in range(self.getAmount(20,20,1)):
                    self.spawn(NormalMob)
                self.NormalMobCooldown.start();
            if self.DashMobCooldown.ready():
                for i in range(self.getAmount(40,30,2)):
                    self.spawn(NormalMob)
                self.DashMobCooldown.start();
            if self.TankMobCooldown.ready():
                for i in range(self.getAmount(90,5,1)):
                    self.spawn(NormalMob)
                self.TankMobCooldown.start();
        #Cull mobs too far offscreen
        for i in self.game.all_mobs:
            if WIDTH*2<i.rect.x or -WIDTH>i.rect.x or -HEIGHT > i.rect.y or 2*HEIGHT < i.rect.y:
                i.kill()

    def getAmount(self,begintime,maximum,change):
        return max(0,min(int(self.time/(1000*change))-(begintime*change),maximum))
        
    def spawn(self,mob):
        match(randint(0,3)):
            case 0:
                mob(self.game,0,randint(0,HEIGHT))
            case 1:
                mob(self.game,randint(0,WIDTH),0)
            case 2:
                mob(self.game,WIDTH,randint(0,HEIGHT))
            case 4:
                mob(self.game,randint(0,WIDTH),HEIGHT)


class Mob(Sprite):
    def __init__(self,game,x,y,health,size,color,speed,drop):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(self.game.player.pos.x-WIDTH/2+x,self.game.player.pos.y-HEIGHT/2+y)
        self.maxhealth = health
        self.health = self.maxhealth
        self.size = size
        self.color = color
        self.basespeed = speed
        self.speed = self.basespeed
        self.effects = []
        self.drop = drop
    def update(self):
        #Mob AI
        self.pos.x += ((self.game.player.pos.x-self.pos.x)/vec(self.game.player.pos.x-self.pos.x,self.game.player.pos.y-self.pos.y).magnitude())*MOBSPEED*self.speed
        self.pos.y += ((self.game.player.pos.y-self.pos.y)/vec(self.game.player.pos.x-self.pos.x,self.game.player.pos.y-self.pos.y).magnitude())*MOBSPEED*self.speed
        #Dynamic Camera Based Position
        self.rect.center = (self.pos.x - Camera.x + (WIDTH+TILESIZE)/2 ,self.pos.y - Camera.y + (HEIGHT+TILESIZE)/2)
        if self.health <= 0:
            self.kill()
            self.game.player.exp+=self.drop
        else:
            self.hp = self.health/self.maxhealth
            self.image.fill((self.color.r*self.hp,self.color.g*self.hp,self.color.b*self.hp))
            self.handleeffects()
    def handleeffects(self):
        for i in range(len(self.effects)):
            match(self.effects[i][0]):
                case "Slow":
                    self.speed = self.basespeed * self.effects[i][1]
                case "Poison":
                    self.health -= self.effects[i][1]
                case "Frozen":
                    if self.effects[i][1] >= 0:
                        self.effects[i][1]-=1;
                        self.speed = 0
                    else:
                        self.speed = self.basespeed
                        self.effects.pop(i)

class WeakMob(Mob):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 30, TILESIZE, pg.Color(200,100,100), 1, 0.5)
    def update(self):
        super().update()

class NormalMob(Mob):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 500, TILESIZE*1.5, pg.Color(255,0,0), 1 , 3)
    def update(self):
        super().update()

class DashMob(Mob):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 100, TILESIZE*0.75, pg.Color(50,150,255), 3 , 2)
    def update(self):
        super().update()

class TankMob(Mob):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 10000, TILESIZE*3, pg.Color(150,150,150), 0.3 , 50)
    def update(self):
        super().update()

class StrongMob(Mob):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 100, TILESIZE, pg.Color(255,0,255), 1.5 , 4)
    def update(self):
        super().update()