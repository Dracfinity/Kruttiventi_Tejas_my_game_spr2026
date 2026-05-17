import pygame as pg

WIDTH = 1000
HEIGHT = 800
TITLE = "Game Development"
FPS = 48

# color values,
# tuple storing RGB values
BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#General
FRICTION = 0.95
TILESIZE = 32
TEXTSIZE = 32

#Player Values
PLAYERSPEED = 0.75
PLAYER_HIT_RECT = pg.Rect(0,0,TILESIZE,TILESIZE)
PLAYERHEALTH = 100;

#Mobs
MOBSPEED = 3
MOB_CAP = 100