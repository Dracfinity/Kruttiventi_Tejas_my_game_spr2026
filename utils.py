import pygame as pg
from settings import *
from pygame.sprite import Sprite

Camera = pg.math.Vector2(0,0)

#A map to let you load a level from text
class Map:
    def __init__(self, filename):
        self.data = []
        #open a file and close it with with
        with open(filename, 'rt') as f:
            for line in f:
                #add the data without whitespaces to self.data
                self.data.append(line.strip())
        
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

#A spritesheet to make a set of images and sprites from one png
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        new_image = pg.transform.scale(image, (width, height))
        image = new_image
        return image

        
#A cooldown to let you set times between actions can occur
class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        self.time = time
        #start at the beginning
        self.start()
    def start(self):
        self.start_time = pg.time.get_ticks()
    def ready(self):
        # sets current time to 
        current_time = pg.time.get_ticks()
        # if the difference between current and start time are greater than self.time
        # return True
        if current_time - self.start_time >= self.time:
            return True
        return False
    def get_cooldown(self):
        current_time = pg.time.get_ticks()
        return max(self.time - (current_time - self.start_time),0)
    