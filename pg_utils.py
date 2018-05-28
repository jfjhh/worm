import pygame_sdl2 as pg
from pygame_sdl2.locals import *


pg.init()

width    = 1280
height   = 720
fps      = 4
gfontpx  = 14
gfancy   = False

font     = pg.font.Font("monaco.ttf", gfontpx)
hwidth   = width  / 2
hheight  = height / 2
clock    = pg.time.Clock()

white    = (255, 255, 255)
black    = (  0,   0,   0)
gray     = (127, 127, 127)
darkgray = ( 16,  16,  16)
darkergray = (8,   8,   8)
red      = (255,   0,   0)
green    = (  0, 255,   0)
blue     = (  0,   0, 255)
yellow   = (255, 255,   0)
cyan     = (  0, 255, 255)
magenta  = (255,   0, 255)

bg_color = black
fg_color = white

