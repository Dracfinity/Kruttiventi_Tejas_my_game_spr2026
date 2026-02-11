# game engine using template from Chris Bradfield's "Making Games with Python & Pygame"
# 
'''
Main file responsible for game loop including input, update, and draw methods.

Tools for game development.

# creating pixel art:
https://www.piskelapp.com/

# free game assets:
https://opengameart.org/

# free sprite sheets:
https://www.kenney.nl/assets

# sound effects:
https://www.bfxr.net/
# music:
https://incompetech.com/music/royalty-free/


'''

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from utils import *

# import settings

#The Game
class Game:
    def __init__(self):
        pg.init()
        # setting up pygame screen with width and height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        #setting up a cooldown
        self.game_cooldowns = {
            "mouseup":Cooldown(1000),
            }
        self.load_data()
    

    def load_data(self):
        self.game_dir = path.dirname(__file__)
        self.map = Map(path.join(self.game_dir, 'lv1.txt'))
        print("data has loaded")
    
    #Each New Frame
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self,col,row)
                if tile == 'P':
                    self.player = Player(self,col,row)
                if tile == 'M':
                    Mob(self,col,row)
        self.run()

    def run(self):
        while self.running:
            #Delta Time is the change in time
            self.dt = self.clock.tick(FPS) / 1000
            #Check for what has happened
            self.events()
            #Update Variable
            self.update()
            #Draw the new frame
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                #If the MouseCooldown is ready
                if self.game_cooldowns["mouseup"].ready():
                    print("Used Mouse")
                    #Restart Cooldown
                    self.game_cooldowns["mouseup"].start()
                else:
                    print("not ready yet")
    

    def quit(self):
        pass

    def update(self):
        #immunity frames
        if(self.player.i_frames.ready()):
            self.player.image.fill((255,255,255))
            if(bool(len(pg.sprite.spritecollide(self.player,self.all_mobs,False)))):
                print("collision")
                self.player.i_frames.start()
        else:
            self.player.image.fill((255,150,150))

        #update monsters game awareness to allow for monster ai(not generative ai thank god)    
        for i in self.all_mobs:
            i.game = self

        self.player.get_keys()
        self.all_sprites.update()

    
    def draw(self):
        self.screen.fill((0,0,0))
        pg.draw.rect(self.screen,(100,50,25),(0-Camera.x+(WIDTH)/2,0-Camera.y+(HEIGHT)/2,self.map.width,self.map.height))
        self.draw_text(str(int(self.player.vel.x*1000)/1000)+","+str(int(self.player.vel.y*1000)/1000), 12, WHITE, WIDTH/5, HEIGHT/20)
        #self.draw_text(, 24, WHITE, WIDTH/2, 2*HEIGHT/4)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    g = Game()

while g.running:
    g.new()


pg.quit()


    

    
