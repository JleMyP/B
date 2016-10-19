# -*- coding: utf-8 -*-

import sys
import os
import pygame
from pygame.locals import *
from random import choice, randrange as rnd

from player import Player
from bot import Bot
from block import Block

from location_game import LocationGame
from location_menu import LocationMenu
from location_settings import LocationSettings

from others import Map, Camera, Joy, Joy2, Button, Label
from utils import ru, min_max, ramka

try:
  import android
  android.map_key(android.KEYCODE_BACK, K_ESCAPE)
  os.chdir("/storage/sdcard0/pygame/b/")
  sys.stderr = sys.stdout = open('errors.txt', 'w')
except ImportError:
  android = False
  os.environ['SDL_VIDEO_CENTERED'] = "1"



def exit():
  global runing
  runing = False



def event_callback():
  events = pygame.event.get()

  for event in events:
    if event.type == QUIT:
      return exit()

  locations["current"].event(events)


def draw():
  locations["current"].draw()
  text = font.render('FPS: %i' % clock.get_fps(), True, (0, 0, 0))
  window.blit(text, (win_w - 150, win_h - 40))
  pygame.display.update()



pygame.init()

if android:
  window = pygame.display.set_mode((0, 0), FULLSCREEN)
  win_w, win_h = window.get_size()
  control = "touch"
else:
  win_w, win_h = 1100, 650
  window = pygame.display.set_mode((win_w, win_h))
  control = "joy" if pygame.joystick.get_count() else "key"


pygame.display.set_caption("B")
clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 30)


player = Player((100, 100), 30, 5)
joy, joy2 = Joy(control, player, 100, 30), Joy2(control, player, 100, 30)

current_settings = { "control": control }

shadow = pygame.Surface((win_w, win_h))
shadow.fill((0, 0, 0))
shadow.set_alpha(150)
menu_bg = window.copy()
menu_bg.fill((255, 255, 255))
menu_bg.blit(shadow, (0, 0))
btn_img = ramka(None, 200, 50, 10, (0, 255, 0), lw=4, alpha=150)
menu_btn_img = ramka(None, 50, 50, 10, (0, 255, 0), (0, 0, 0), lw=4, alpha=150)


locations = {}
g = globals()

locations["game"] = LocationGame(g)
locations["menu"] = LocationMenu(g)
locations["settings"] = LocationSettings(g)

locations["menu"].show()


runing = True
while runing:
  event_callback()
  locations["current"].update()
  draw()
  clock.tick(60)

#sys.stdout.close()
pygame.quit()
