#ADD MODALS TO ALLOW FOR LEVEL UP SCREENS, LOADING SCREENS, AND MAIN MENU
import pygame as pg
from settings import *
from armory import *

def PauseModal(game):
    game.playing = False;
    others = [["#444444aa",pg.Rect(0,0,WIDTH,HEIGHT)],
              pg.font.SysFont("arial",50).render("Pause",True,(255,255,255)),
            ]
    weapons = game.player.armory.owned
    buttons = [Button(WIDTH/5,11*HEIGHT/20,WIDTH/5,HEIGHT/10,"#888888","#666666","Continue","self.game.playing = True; self.game.prevtime = pg.time.get_ticks()",game),
               Button(3*WIDTH/5,11*HEIGHT/20,WIDTH/5,HEIGHT/10,"#888888","#666666","Quit Game","pg.quit()",game),]
    while game.playing == False:
        mousepos = pg.mouse.get_pos()
        isdown = pg.mouse.get_pressed()
        overlay = pg.surface.Surface((WIDTH,HEIGHT),pg.SRCALPHA)
        
        pg.draw.rect(overlay,others[0][0],others[0][1])
        game.screen.blit(overlay,(0,0))
        game.screen.blit(others[1],(WIDTH/2.5,HEIGHT/3))
        for i in buttons:
            i.check(mousepos,isdown[0])
            i.draw()
        #Weapon Slots and level images
        for j in range(len(weapons)):
            item = pg.Surface((TILESIZE*2,TILESIZE*2))
            match(weapons[j][0]):
                case "Earthquake":
                    pg.draw.circle(item,(150,50,0),(TILESIZE,TILESIZE*0.75),TILESIZE*0.5)
                    pg.draw.rect(item,(255,255,0),(0,TILESIZE*1.25,(TILESIZE*1.8*weapons[j][1]/6)+TILESIZE*0.1,TILESIZE*0.5))
                case "Tsunami":
                    pg.draw.polygon(item,(100,100,255),((TILESIZE*0.25,TILESIZE*0.25),(TILESIZE*0.25,TILESIZE*1.25),(TILESIZE*1.75,TILESIZE*0.75)))
                    pg.draw.rect(item,(255,255,0),(0,TILESIZE*1.25,(TILESIZE*1.8*weapons[j][1]/6)+TILESIZE*0.1,TILESIZE*0.5))
                case "Tornado":
                    pg.draw.circle(item,(255,255,255),(TILESIZE,TILESIZE*0.75),TILESIZE*0.5)
                    pg.draw.rect(item,(255,255,0),(0,TILESIZE*1.25,(TILESIZE*1.8*weapons[j][1]/6)+TILESIZE*0.1,TILESIZE*0.5))
                case "Landslide":
                    pg.draw.circle(item,(150,100,70),(TILESIZE,TILESIZE*0.75),TILESIZE*0.5)
                    pg.draw.rect(item,(255,255,0),(0,TILESIZE*1.25,(TILESIZE*1.8*weapons[j][1]/6)+TILESIZE*0.1,TILESIZE*0.5))
                case "Plague":
                    pg.draw.rect(item,(0,255,0),(TILESIZE*0.5,TILESIZE*0.25,TILESIZE,TILESIZE))
                    pg.draw.rect(item,(255,255,0),(0,TILESIZE*1.25,(TILESIZE*1.8*weapons[j][1]/6)+TILESIZE*0.1,TILESIZE*0.5))
                case "Wildfire":
                    pg.draw.rect(item,(255,0,0),(TILESIZE*0.5,TILESIZE*0.25,TILESIZE,TILESIZE))
                    pg.draw.rect(item,(255,255,0),(0,TILESIZE*1.25,(TILESIZE*1.8*weapons[j][1]/6)+TILESIZE*0.1,TILESIZE*0.5))
                case "Rain":
                    pg.draw.rect(item,(0,100,255),(TILESIZE*0.5,TILESIZE*0.25,TILESIZE,TILESIZE))
                    pg.draw.rect(item,(255,255,0),(0,TILESIZE*1.25,(TILESIZE*1.8*weapons[j][1]/6)+TILESIZE*0.1,TILESIZE*0.5))
                case "Hex":
                    pg.draw.rect(item,(150,0,255),(TILESIZE*0.5,TILESIZE*0.25,TILESIZE,TILESIZE))
                    pg.draw.rect(item,(255,255,0),(0,TILESIZE*1.25,(TILESIZE*1.8*weapons[j][1]/6)+TILESIZE*0.1,TILESIZE*0.5))
            game.screen.blit(item,(TILESIZE*(3*j+1),TILESIZE))
            game.screen.blit(item,(TILESIZE*(3*j+1),TILESIZE))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

def MainMenuModal(game):
    game.playing = False;
    others = [["#444444aa",pg.Rect(0,0,WIDTH,HEIGHT)],
              pg.font.SysFont("arial",50).render("Calamity Mage",True,(255,255,255)),
            ]
    buttons = [Button(WIDTH/5,11*HEIGHT/20,WIDTH/5,HEIGHT/10,"#888888","#666666","Start","self.game.playing = True; self.game.prevtime = pg.time.get_ticks()",game),
               Button(3*WIDTH/5,11*HEIGHT/20,WIDTH/5,HEIGHT/10,"#888888","#666666","Quit Game","pg.quit()",game),]
    while game.playing == False:
        mousepos = pg.mouse.get_pos()
        isdown = pg.mouse.get_pressed()
        overlay = pg.surface.Surface((WIDTH,HEIGHT),pg.SRCALPHA)
        
        pg.draw.rect(overlay,others[0][0],others[0][1])
        game.screen.blit(overlay,(0,0))
        game.screen.blit(others[1],(WIDTH/2.5,HEIGHT/3))
        for i in buttons:
            i.check(mousepos,isdown[0])
            i.draw()
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

def DeathModal(game):
    game.playing = False;
    others = [["#000000",pg.Rect(0,0,WIDTH,HEIGHT)],
              pg.font.SysFont("arial",50).render("You Died",True,(255,255,255)),
            ]
    buttons = [Button(WIDTH/5,11*HEIGHT/20,WIDTH/5,HEIGHT/10,"#888888","#666666","Restart","self.game.playing = True; self.game.prevtime = pg.time.get_ticks();[i.kill() for i in self.game.all_sprites]; self.game.__init__();self.game.time = 0;self.game.player.__init__(self.game,0,0);",game),
               Button(3*WIDTH/5,11*HEIGHT/20,WIDTH/5,HEIGHT/10,"#888888","#666666","Quit Game","pg.quit()",game),]
    while game.playing == False:
        mousepos = pg.mouse.get_pos()
        isdown = pg.mouse.get_pressed()
        overlay = pg.surface.Surface((WIDTH,HEIGHT),pg.SRCALPHA)
        
        pg.draw.rect(overlay,others[0][0],others[0][1])
        game.screen.blit(overlay,(0,0))
        game.screen.blit(others[1],(WIDTH/2.5,HEIGHT/3))
        for i in buttons:
            i.check(mousepos,isdown[0])
            i.draw()
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

#Modal if the Reaper kills you
#Used AI to bugfix because rendering order wrong and could not understand on own
def WinModalA(game):
    game.playing = False;
    others = [["#000000",pg.Rect(0,0,WIDTH,HEIGHT)],
              pg.font.SysFont("arial",50).render("You Win?",True,(255,255,255)),
            ]
    buttons = [Button(WIDTH/5,11*HEIGHT/20,WIDTH/5,HEIGHT/10,"#888888","#666666","Restart","self.game.playing = True; self.game.prevtime = pg.time.get_ticks();[i.kill() for i in self.game.all_sprites]; self.game.__init__();self.game.time = 0;self.game.player.__init__(self.game,0,0);",game),
               Button(3*WIDTH/5,11*HEIGHT/20,WIDTH/5,HEIGHT/10,"#888888","#666666","Quit Game","pg.quit()",game),]
    while game.playing == False:
        mousepos = pg.mouse.get_pos()
        isdown = pg.mouse.get_pressed()
        overlay = pg.surface.Surface((WIDTH,HEIGHT),pg.SRCALPHA)
        
        pg.draw.rect(overlay,others[0][0],others[0][1])
        game.screen.blit(overlay,(0,0))
        game.screen.blit(others[1],(WIDTH/2.5,HEIGHT/3))
        for i in buttons:
            i.check(mousepos,isdown[0])
            i.draw()
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()


#Modal if the Reaper is killed
def WinModalB(game):
    game.playing = False;
    others = [["#000000",pg.Rect(0,0,WIDTH,HEIGHT)],
              pg.font.SysFont("arial",50).render("You have beaten Death, You Win",True,(255,255,255)),
            ]
    buttons = [Button(WIDTH/5,11*HEIGHT/20,WIDTH/5,HEIGHT/10,"#888888","#666666","Restart","self.game.playing = True; self.game.prevtime = pg.time.get_ticks();[i.kill() for i in self.game.all_sprites]; self.game.__init__();self.game.time = 0;self.game.player.__init__(self.game,0,0);",game),
               Button(3*WIDTH/5,11*HEIGHT/20,WIDTH/5,HEIGHT/10,"#888888","#666666","Quit Game","pg.quit()",game),]
    while game.playing == False:
        mousepos = pg.mouse.get_pos()
        isdown = pg.mouse.get_pressed()
        overlay = pg.surface.Surface((WIDTH,HEIGHT),pg.SRCALPHA)
        
        pg.draw.rect(overlay,others[0][0],others[0][1])
        game.screen.blit(overlay,(0,0))
        game.screen.blit(others[1],(WIDTH/4,HEIGHT/3))
        for i in buttons:
            i.check(mousepos,isdown[0])
            i.draw()
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

Options = {
    #The Hex just makes you worse until you are level 7, where it super buffs you;
    "Hex":[
            ["Hex: Curses YOU, sets health to 25%, only available in the 1st round", "self.game.player.armory.upgrade('Hex');self.game.player.maxhealth=25;self.game.player.health=25;self.game.player.armory.allWeapons.append('Hex')"],
            ["Upgrade Hex, you now have hysteria \n reversed controls, so you move backwards", "self.game.player.armory.upgrade('Hex');self.game.player.SPEED*=-1"],
            ["Upgrade Hex, The ground turns to ice around you \n, you slip around more and stumble and dont slow down when putting down a key","self.game.player.armory.upgrade('Hex');self.game.player.FRICTION=0.98"],
            ["Upgrade Hex, you now have a virus \n cannot heal","self.game.player.armory.upgrade('Hex');self.game.player.canHeal=False"],
            ["Upgrade Hex, You now have a blight \n your speed is cut in half","self.game.player.armory.upgrade('Hex');self.game.player.SPEED*=0.5"],
            ["Upgrade Hex, It seems to be glowing \n It is changing","self.game.player.armory.upgrade('Hex')"],
            ["Ultimate Hex: Blessing from the Gods \n All debuffs removed, health increase, and Death itself is weakened ","self.game.player.armory.upgrade('Hex');self.game.player.killDeath=True;self.game.player.health = 150;self.game.player.maxhealth = 150;self.game.player.SPEED *= -2;self.game.player.FRICTION = 0.95;self.game.player.canHeal = True;"],
    ],
    #The Tornado
    "Tornado":[
            ["Tornado: A low damage area that damages things \n around the character","self.game.player.armory.upgrade('Tornado')"],
            ["Increase Tornado Damage by 3 per hit","self.game.player.armory.upgrade('Tornado');Tornado.BaseStats['dmg']+=3"],
            ["Increase Tornado Size by 50%","self.game.player.armory.upgrade('Tornado');Tornado.BaseStats['size']*=1.5"],
            ["Make Tornado Attack 25% more","self.game.player.armory.upgrade('Tornado');Tornado.BaseStats['dmgtick']*=0.75"],
            ["Increase Tornado Damage by 5 per hit","self.game.player.armory.upgrade('Tornado');Tornado.BaseStats['dmg']+=5"],
            ["Increase Tornado Size by 50%","self.game.player.armory.upgrade('Tornado');Tornado.BaseStats['size']*=1.5"],
            ["Ultimate:Slow all enemies \n in the range of the Tornado","self.game.player.armory.upgrade('Tornado');Tornado.BaseStats['ultimate']=True"],
            ],
    "Earthquake":[
            ["Earthquake: Random, high damage bursts \n that appear for short times \n at spots on your screen","self.game.player.armory.upgrade('Earthquake')"],
            ["Decrease Earthquake Cooldown by 20%","self.game.player.armory.upgrade('Earthquake');Earthquake.BaseStats['cooldown'].time*=0.8"],
            ["Increase Earthquake Dmg by 20","self.game.player.armory.upgrade('Earthquake');Earthquake.BaseStats['dmg'] += 20"],
            ["Increase Earthquake Size by 50%","self.game.player.armory.upgrade('Earthquake');Earthquake.BaseStats['size'] *= 1.5"],
            ["Increase Earthquake Duration by 100%","self.game.player.armory.upgrade('Earthquake');Earthquake.BaseStats['duration'] *= 2"],
            ["Increase Earthquake Dmg by 20","self.game.player.armory.upgrade('Earthquake');Earthquake.BaseStats['dmg'] += 20"],
            ["Ultimate: Slowly increases in dmg \n over its duration","self.game.player.armory.upgrade('Earthquake');Earthquake.BaseStats['ultimate']=True"],
    ],
    "Landslide":[
            ["Landslide: Rocks that spin around you, \n sliding in a radius around you","self.game.player.armory.upgrade('Landslide')"],
            ["Increase Landslide Damage by 5 per hit","self.game.player.armory.upgrade('Landslide');Landslide.BaseStats['dmg']+=5"],
            ["Add 2 to the Amount of Landslides","self.game.player.armory.upgrade('Landslide');Landslide.BaseStats['amount']+=2"],
            ["Increase Landslide Spin speed by 100%","self.game.player.armory.upgrade('Landslide');Landslide.BaseStats['speed']*=2"],
            ["Make the radius the Landslides\n orbit around 75% size","self.game.player.armory.upgrade('Landslide');Landslide.BaseStats['spinradius']*=0.75"],
            ["Increase Landslide Rock Size by 50%","self.game.player.armory.upgrade('Landslide');Landslide.BaseStats['rockradius']*=1.5"],
            ["Ultimate: Adds two radii of \n landslides, spinning twice in opposite directions","self.game.player.armory.upgrade('Landslide');Landslide.BaseStats['ultimate']=True;self.game.player.armory.upgrade('Landslide');Landslide.BaseStats['spinradius']*=2"],
    ],
    "Plague":[
            ["Plague: Flies that appear from you \n and damage things near you","self.game.player.armory.upgrade('Plague')"],
            ["Decrease Plague Cooldown by 20%","self.game.player.armory.upgrade('Plague');Plague.BaseStats['cooldown'].time*=0.8"],
            ["Increase Fly Speed by 100%","self.game.player.armory.upgrade('Plague');Plague.BaseStats['speed'] *= 2"],
            ["Double the amount of Flies","self.game.player.armory.upgrade('Plague');Plague.BaseStats['amount'] *= 2"],
            ["Increase Plague Duration by 100%","self.game.player.armory.upgrade('Plague');Plague.BaseStats['duration'] *= 2"],
            ["Increase Plague Dmg by 5","self.game.player.armory.upgrade('Plague');Plague.BaseStats['dmg'] += 5"],
            ["Ultimate: The Plague is Airborne, \n and poisons all onscreen enemies","self.game.player.armory.upgrade('Plague');Plague.BaseStats['ultimate']=True"],
    ],
    "Tsunami":[
            ["Tsunami: A Wave that shoots infront of you \n at high speeds, melting enemies","self.game.player.armory.upgrade('Tsunami')"],
            ["Decrease Tsunami Cooldown by 20%","self.game.player.armory.upgrade('Tsunami');Tsunami.BaseStats['cooldown'].time*=0.8"],
            ["Increase Tsunami Dmg by 25","self.game.player.armory.upgrade('Tsunami');Tsunami.BaseStats['dmg']+=25"],
            ["Increase Tsunami Width by 100%","self.game.player.armory.upgrade('Tsunami');Tsunami.BaseStats['width']*=0.5"],
            ["Decrease Tsunami Hit Speed by 25%","self.game.player.armory.upgrade('Tsunami');Tsunami.BaseStats['dmgtick']*=0.75"],
            ["Increase Tsunami Duration by 50%","self.game.player.armory.upgrade('Tsunami');Tsunami.BaseStats['duration']*=1.5"],
            ["Ultimate: Fire another Tsunami behind you","self.game.player.armory.upgrade('Tsunami');Tsunami.BaseStats['ultimate'] = True"],
    ],
    "Wildfire":[
            ["Wildfire: A Quick Firing Bullet that shoots \n at enemies, burning them, \n dealing Damage over time","self.game.player.armory.upgrade('Wildfire')"],
            ["Increase Wildfire burn damage by 100%","self.game.player.armory.upgrade('Wildfire');Wildfire.BaseStats['burntier']*=2"],
            ["Increase the Wildfire size by 50%","self.game.player.armory.upgrade('Wildfire');Wildfire.BaseStats['size']*=1.5"],
            ["Decrease Wildfire Speed by 50%,\n spending more time on screen","self.game.player.armory.upgrade('Wildfire');Wildfire.BaseStats['speed']*=0.5"],
            ["Decrease Wildfire time between \n hits by 25%","self.game.player.armory.upgrade('Wildfire');Wildfire.BaseStats['dmgtick']*=0.75"],
            ["Decrease Wildfire Cooldown by 50%","self.game.player.armory.upgrade('Wildfire');Wildfire.BaseStats['cooldown'].time*=0.5"],
            ["Ultimate: Make the wildfire attack \n 3 times in a row","self.game.player.armory.upgrade('Wildfire');Wildfire.BaseStats['ultimate'] = True"],
    ],
    #Simple Weapon to start
    "Rain":[
            ["Get a Rain projectile","self.game.player.armory.upgrade('Rain')"],
            ["Double damage of Rain","self.game.player.armory.upgrade('Rain');Rain.BaseStats['dmg']*=2"],
            ["Increase the Rain pierce by 100%","self.game.player.armory.upgrade('Rain');Rain.BaseStats['pierce']*=2"],
            ["Decrease Rain Cooldown by 50%, \n attacking at double the rate","self.game.player.armory.upgrade('Rain');Rain.BaseStats['cooldown'].time*=0.5"],
            ["Decrease Rain time between hits by 25%","self.game.player.armory.upgrade('Rain');Rain.BaseStats['dmgtick']*=0.75"],
            ["Increase the Pierce of Rain by 200%","self.game.player.armory.upgrade('Rain');Rain.BaseStats['pierce']*=3"],
            ["Ultimate: Make the Rain's attack \n freeze enemies in place","self.game.player.armory.upgrade('Rain');Rain.BaseStats['ultimate'] = True"],
    ],
    "Full":[
        ["",""],
    ]
}      


def LevelUp(game):

    game.playing = False;
    #Get Possible Weapons to upgrade
    choices = game.player.armory.getOptions()

    buttons = [ Button(WIDTH/10,2*HEIGHT/16,8*WIDTH/10,3*HEIGHT/16,(150,150,150),(100,100,100),Options[choices[0]][game.player.armory.getLevel(choices[0])][0],Options[choices[0]][game.player.armory.getLevel(choices[0])][1],game),
                Button(WIDTH/10,7*HEIGHT/16,8*WIDTH/10,3*HEIGHT/16,(150,150,150),(100,100,100),Options[choices[1]][game.player.armory.getLevel(choices[1])][0],Options[choices[1]][game.player.armory.getLevel(choices[1])][1],game),
                Button(WIDTH/10,12*HEIGHT/16,8*WIDTH/10,3*HEIGHT/16,(150,150,150),(100,100,100),Options[choices[2]][game.player.armory.getLevel(choices[2])][0],Options[choices[2]][game.player.armory.getLevel(choices[2])][1],game)
    ]

    
    while game.playing == False:
        mousepos = pg.mouse.get_pos()
        isdown = pg.mouse.get_pressed()
        overlay = pg.surface.Surface((WIDTH,HEIGHT),pg.SRCALPHA)
        
        game.screen.blit(overlay,(0,0))
        for i in buttons:
            x = i.check(mousepos,isdown[0])
            if x == True:
                game.playing = True;
                game.prevtime = pg.time.get_ticks()
            i.draw()
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()




#Button
class Button():
    def __init__(self,x,y,w,h,c,dc,text,action,game):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = c
        self.game = game
        self.notpressed = True
        self.truecolor = c
        self.dimmedcolor = dc
        self.text = text
        self.font = pg.font.SysFont("arial", TEXTSIZE);
        self.font_render = self.font.render(self.text,True,(255,255,255))
        self.action = action
    def check(self,mousepos, isdown):
        if self.x<mousepos[0]<self.x+self.w and self.y<mousepos[1]<self.y+self.h and isdown and self.notpressed:
            self.notpressed = False
            self.color = self.dimmedcolor
            exec(self.action)
            return True;
        if isdown == False:
            self.notpressed = True
            self.color = self.truecolor
            return False;
    def draw(self):
        pg.draw.rect(self.game.screen,self.color,(self.x,self.y,self.w,self.h))
        self.game.screen.blit(self.font_render, (self.x, self.y))



    