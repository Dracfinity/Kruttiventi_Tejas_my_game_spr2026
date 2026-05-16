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
from os import path
from settings import *
from sprites import *
from utils import *
from mob import *
from modals import *

# import stuff

#The Game
class Game:
    def __init__(self):
        pg.init()
        # setting up pygame screen with width and height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.time = 0;
        self.currenttime = 0;
        self.prevtime = 0;
        MainMenuModal(self)

    
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.player = Player(self, 0 ,0)
        self.spawner = Spawner(self)
        self.run()

    def run(self):
        while self.running:
            self.currenttime = pg.time.get_ticks()
            self.dt = self.currenttime-self.prevtime
            self.prevtime = pg.time.get_ticks()
            if self.playing == True:
                self.time += self.dt;
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
            """
            if event.type == pg.MOUSEBUTTONUP:
                #If the MouseCooldown is ready
                if self.game_cooldowns["mouseup"].ready():
                    print("Used Mouse")
                    #Restart Cooldown
                    self.game_cooldowns["mouseup"].start()
                else:
                    print("not ready yet")
            """
        justpressed = pg.key.get_just_pressed()
        if justpressed[pg.K_p]:
            PauseModal(self)
        #if justpressed[pg.K_l]:
            #LevelUp(self)
    

    def quit(self):
        pass

    def update(self):
        #immunity frames
        if(self.player.i_frames.ready()):
            if(bool(len(pg.sprite.spritecollide(self.player,self.all_mobs,False)))):
                self.player.i_frames.start()
                self.player.health-=1;
                if(self.player.health <= 0):
                    DeathModal(self)
                    
        if(bool(len(pg.sprite.spritecollide(self.player,self.all_powerups,True)))):
                self.player.i_frames.start()
                if self.player.canHeal == True:
                    self.player.health+=15;
                    if self.player.health > self.player.maxhealth:
                        self.player.health = self.player.maxhealth;


        #update all
        self.spawner.update()
        self.player.get_keys()
        self.all_sprites.update()
        self.clock.tick(FPS)

    
    def draw(self):
        self.screen.fill((0,50,0))
        #Time
        self.draw_text(str(self.time/1000), int(TEXTSIZE), WHITE, (WIDTH-int(TEXTSIZE/2))/2, TILESIZE*3);
        #Level Screen
        self.all_sprites.draw(self.screen);
        #EXP bar
        pg.draw.rect(self.screen,(100,100,100),(0,0,WIDTH,TILESIZE));
        pg.draw.rect(self.screen,(100,100,255),(0,0,(self.player.exp/(self.player.exptolvlup))*WIDTH,TILESIZE));
        self.draw_text("Level:"+str(self.player.level), int(TEXTSIZE/2), WHITE, WIDTH/20, (TILESIZE-int(TEXTSIZE/2))/2);
        #Health bar
        pg.draw.rect(self.screen,(100,100,100),(0,TILESIZE,WIDTH,TILESIZE));
        pg.draw.rect(self.screen,(150,0,0),(0,TILESIZE,(self.player.health/(self.player.maxhealth))*WIDTH,TILESIZE));
        self.draw_text("Health:"+str(self.player.health), int(TEXTSIZE/2), WHITE, WIDTH/20, (TILESIZE-int(TEXTSIZE/2))/2+TILESIZE);
        pg.display.flip();

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial');
        font = pg.font.Font(font_name, size);
        text_surface = font.render(text, True, color);
        text_rect = text_surface.get_rect();
        text_rect.midtop = (x,y);
        self.screen.blit(text_surface, text_rect);

if __name__ == "__main__":
    g = Game()

#while g.running:
g.new()


pg.quit()


    

    
