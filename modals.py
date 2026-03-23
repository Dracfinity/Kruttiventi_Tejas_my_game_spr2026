#ADD MODALS TO ALLOW FOR LEVEL UP SCREENS, LOADING SCREENS, AND MAIN MENU
import pygame as pg

def PauseModal(game):
    game.playing = False;
    buttons = [Button(250,500,100,100,"#ff0000",game.screen),Button(450,500,100,100,"#ff0000",game.screen)]
    while game.playing == False:
        
        for i in buttons():
            buttons[i].check()
        pg.time.Clock.tick(60)
    




class Button():
    def __init__(self,x,y,w,h,color,screen):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.screen = screen
        self.notpressed = True
        pass;
    def check(self,mousepos, isdown):
        if self.x<mousepos.x<self.x+self.w and self.y<mousepos.y<self.y+self.h and isdown and self.notpressed:
            print("pressed")
            self.notpressed = False
        if isdown == False:
            self.notpressed = True
    def draw(self):
        pg.draw.rect(self.screen,self.color,(self.x,self.y,self.w,self.h))
        pg.display.flip()
