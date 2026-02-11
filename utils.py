import pygame as pg
from settings import *

Camera = pg.math.Vector2(0,0)

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
    