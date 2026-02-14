import pygame as pg

WIDTH = 800
HEIGHT = 600
TITLE = "Game Development"
FPS = 60

# color values,
# tuple storing RGB values
BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)

#General
FRICTION = 0.95
TILESIZE = 32

#Player Values
PLAYERSPEED = 0.5
PLAYER_HIT_RECT = pg.Rect(0,0,TILESIZE-3,TILESIZE-3)

#Mobs
MOBSPEED = 3