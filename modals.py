#ADD MODALS TO ALLOW FOR LEVEL UP SCREENS, LOADING SCREENS, AND MAIN MENU
import pygame as pg
from settings import *
from armory import *

def PauseModal(game):
    game.playing = False;
    others = [["#444444aa",pg.Rect(0,0,WIDTH,HEIGHT)],
              pg.font.SysFont("arial",50).render("Pause",True,"#ffffffff"),
            ]
    buttons = [Button(WIDTH/5,11*HEIGHT/20,WIDTH/5,HEIGHT/10,"#888888","#666666","Continue",WIDTH/20,"self.game.playing = True",game),
               Button(3*WIDTH/5,11*HEIGHT/20,WIDTH/5,HEIGHT/10,"#888888","#666666","Quit",WIDTH/20,"pg.quit()",game),]
    while game.playing == False:
        mousepos = pg.mouse.get_pos()
        isdown = pg.mouse.get_pressed()
        overlay = pg.surface.Surface((WIDTH,HEIGHT),pg.SRCALPHA)
        
        pg.draw.rect(overlay,others[0][0],others[0][1])
        game.screen.blit(others[1],(WIDTH/2.5,HEIGHT/3))
        game.screen.blit(overlay,(0,0))
        for i in buttons:
            i.check(mousepos,isdown[0])
            i.draw()
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
Options = {
    "Tornado":[
            ["A low damage tornado that spins around the character","game.player.armory.upgrade('Tornado');"],
            ["Increase Tornado Damage by 3 per hit","game.player.armory.upgrade('Tornado');Tornado.BaseStats['dmg']+=3"],
            ["Increase Tornado Size by 50%","game.player.armory.upgrade('Tornado');Tornado.BaseStats['size']*=1.5"],
            ["Make Tornado Attack 25% more","game.player.armory.upgrade('Tornado');Tornado.BaseStats['dmgtick']*=0.75"],
            ["Increase Tornado Damage by 5 per hit","game.player.armory.upgrade('Tornado');Tornado.BaseStats['dmg']+=5"],
            ["Increase Tornado Size by 50%","game.player.armory.upgrade('Tornado');Tornado.BaseStats['size']*=1.5"],
            ["Ultimate:Slow all enemies in the range of the Tornado","game.player.armory.upgrade('Tornado');Tornado.BaseStats['ultimate']=True"],
            ],
    "Earthquake":[
            ["Random, high damage earthquake that appear for short times at spots on your screen","game.player.armory.upgrade('Earthquake');"],
            ["Decrease Earthquake Cooldown by 20%","game.player.armory.upgrade('Earthquake');Earthquake.BaseStats['cooldown'].time*=0.8"],
            ["Increase Earthquake Dmg by 20","game.player.armory.upgrade('Earthquake');Earthquake.BaseStats['dmg'] += 20"],
            ["Increase Earthquake Size by 50%","game.player.armory.upgrade('Earthquake');Earthquake.BaseStats['size'] *= 1.5"],
            ["Increase Earthquake Duration by 100%","game.player.armory.upgrade('Earthquake');Earthquake.BaseStats['duration'] *= 2"],
            ["Increase Earthquake Dmg by 20","game.player.armory.upgrade('Earthquake');Earthquake.BaseStats['dmg'] += 20"],
            ["Ultimate: Slowly increases in size over its duration","game.player.armory.upgrade('Earthquake');Earthquake.BaseStats['ultimate']=True"],
    ],
    "Landslide":[
        ["Rocks that spin around you, sliding in a radius around you","game.player.armory.upgrade('Landslide');"],
        ["Increase Landslide Damage by 5 per hit","game.player.armory.upgrade('Landslide');Landslide.BaseStats['dmg']+=5"],
        ["Add 2 to the Amount of Landslides","game.player.armory.upgrade('Landslide');Landslide.BaseStats['amount']+=2"],
        ["Increase Landslide Spin speed by 100%","game.player.armory.upgrade('Landslide');Landslide.BaseStats['speed']*=2"],
        ["Make the radius the Landslides orbit around 75% size","game.player.armory.upgrade('Landslide');Landslide.BaseStats['spinradius']*=0.75"],
        ["Increase Landslide Rock Size by 50%","game.player.armory.upgrade('Landslide');Landslide.BaseStats['rockradius']*=1.5"],
        ["Ultimate: Adds two radii of landslides, spinning twice","game.player.armory.upgrade('Landslide');Landslide.BaseStats['dmg']+=5"],
    ],
    "Plague":[
            ["Flies that appear from you and damage things near you","game.player.armory.upgrade('Plague');"],
            ["Decrease Plague Cooldown by 20%","game.player.armory.upgrade('Plague');Plague.BaseStats['cooldown'].time*=0.8"],
            ["Increase Fly Speed by 100%","game.player.armory.upgrade('Plague')Plague.BaseStats['speed'] *= 2"],
            ["Increase Flies by 100%","game.player.armory.upgrade('Plague');Plague.BaseStats['amount'] *= 2"],
            ["Increase Plague Duration by 100%","game.player.armory.upgrade('Plague');Plague.BaseStats['duration'] *= 2"],
            ["Increase Plague Dmg by 5","game.player.armory.upgrade('Plague');Plague.BaseStats['dmg'] += 5"],
            ["Ultimate: Poisonous Flies that deal Damage over time to enemies","game.player.armory.upgrade('Plague');Plague.BaseStats['ultimate']=True"],
    ],
    "Tsunami":[
            ["A Wave that shoots infront of you at high speeds, melting enemies","game.player.armory.upgrade('Tsunami')"],
            ["Decrease Tsunami Cooldown by 20%","game.player.armory.upgrade('Tsunami');Tsunami.BaseStats['cooldown'].time*=0.8"],
            ["Increase Tsunami Dmg by 25","game.player.armory.upgrade('Tsunami');Tsunami.BaseStats['dmg']+=25"],
            ["Increase Tsunami Width by 100%","game.player.armory.upgrade('Tsunami');Tsunami.BaseStats['width']*=0.5"],
            ["Decrease Tsunami Hit Speed by 25%","game.player.armory.upgrade('Tsunami');Tsunami.BaseStats['dmgtick']*=0.75"],
            ["Increase Tsunami Duration by 50%","game.player.armory.upgrade('Tsunami');Tsunami.BaseStats['duration']*=1.5"],
            ["Ultimate: Fire another Tsunami behind you","game.player.armory.upgrade('Tsunami');Tsunami.BaseStats['ultimate'] = True"],
    ],
    "None":[
        ["",""]
    ]
}      


def LevelUp(game):
    game.playing = False;
    
    #Get Possible Weapons to upgrade
    choices = game.player.armory.getOptions()

    buttons = [
        Button(WIDTH/13,HEIGHT/10,3*WIDTH/3,8*HEIGHT/10,(150,150,150),(100,100,100),Options[choices[0]][game.player.armory.getLevel(choices[0])][0],TILESIZE/20,Options[choices[0]][game.player.armory.getLevel(choices[0])][1],game),
        Button(5*WIDTH/13,HEIGHT/10,3*WIDTH/3,8*HEIGHT/10,(150,150,150),(100,100,100),Options[choices[0]][game.player.armory.getLevel(choices[0])][0],TILESIZE/20,Options[choices[1]][game.player.armory.getLevel(choices[1])][1],game),
        Button(9*WIDTH/13,HEIGHT/10,3*WIDTH/3,8*HEIGHT/10,(150,150,150),(100,100,100),Options[choices[0]][game.player.armory.getLevel(choices[0])][0],TILESIZE/20,Options[choices[2]][game.player.armory.getLevel(choices[2])][1],game)
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
            i.draw()
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()




#Button
class Button():
    def __init__(self,x,y,w,h,c,dc,text,size,action,game):
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
        self.font = pg.font.SysFont("arial", int(size));
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
        textImg = self.font.render(self.text, True, (255, 255, 255))
        self.game.screen.blit(textImg, (self.x, self.y))



    