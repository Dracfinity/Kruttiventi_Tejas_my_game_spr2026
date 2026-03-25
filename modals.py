#ADD MODALS TO ALLOW FOR LEVEL UP SCREENS, LOADING SCREENS, AND MAIN MENU
import pygame as pg
from settings import *

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
        game.screen.blit(others[1],(HEIGHT/2,WIDTH/2))
        game.screen.blit(overlay,(0,0))
        for i in buttons:
            i.check(mousepos,isdown[0])
            i.draw()
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
    




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
        self.font = pg.font.SysFont("arial", int(size));#fontFit(text,int(w*0.9),int(h*0.9))
        self.action = action
    def check(self,mousepos, isdown):
        if self.x<mousepos[0]<self.x+self.w and self.y<mousepos[1]<self.y+self.h and isdown and self.notpressed:
            self.notpressed = False
            self.color = self.dimmedcolor
            exec(self.action)
        if isdown == False:
            self.notpressed = True
            self.color = self.truecolor
    def draw(self):
        pg.draw.rect(self.game.screen,self.color,(self.x,self.y,self.w,self.h))
        textImg = self.font.render(self.text, True, (255, 255, 255))
        self.game.screen.blit(textImg, (self.x, self.y))


#For Font Fitting
def fontFit(text, boxwidth, boxheight):
    size = boxwidth
    font = pg.font.SysFont("arial", size)
    textImg = font.render(text, True, (255, 255, 255))
    while textImg.get_width() >= boxwidth or textImg.get_height() >= boxheight:
        size -= 1
        font = pg.font.SysFont("arial", size)
        textImg = font.render(text, True, (255, 255, 255))
    return font;
    