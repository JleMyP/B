# -*- coding: utf-8 -*-

import geom
import sys
import os
import pygame
from pygame.locals import *
from random import choice, randrange as rnd

try:
  import android
  android.map_key(android.KEYCODE_BACK, K_ESCAPE)
  os.chdir("/storage/sdcard0/pygame/b/")
  sys.stderr = sys.stdout = open('errors.txt', 'w')
except:
  android = False
  os.environ['SDL_VIDEO_CENTERED'] = "1"

from player import Player
from bot import Bot
from block import Block
from others import Map, Camera, Joy, Joy2
from utils import ru, min_max, ramka



def init_lvl1():
  map_w, map_h = win_w + 200, win_h + 200
  player.__init__((0, 0), 40, 5)
  camera = Camera(None, map_w, map_h)
  joy.camera = joy2.camera = camera

  walls = [
    Block((0, 0, 20, map_h), camera),
    Block((20, 0, map_w - 20, 20), camera),
    Block((map_w - 20, 20, 20, map_h - 20), camera),
    Block((20, map_h - 20, map_w - 40, 20), camera),
    Block((460, 20, 20, map_h / 2 - 50), camera),
    Block((460, map_h / 2 + 30, 20, map_h / 2 - 50), camera),
    Block((780, 20, 20, map_h / 2 * 0.75), camera),
    Block((780, map_h / 2 * 1.25 - 20, 20, map_h / 2 * 0.75), camera),
    Block([(200, 400), (300, 500), (220, 470)], camera)
  ]

  bots = [Bot([(rnd(550, map_w - 50), rnd(50, map_h - 50))], 90, 200) for x in xrange(10)]    
  map = Map('intro', map_w, map_h, camera, player, (100, 100), walls, bots)
  return camera, map


def show_menu():
  global location, menu_bg
  location = locations["menu"]
  menu_bg = window.copy()
  menu_bg.blit(shadow, (0, 0))


def continue_game():
  global location
  location = locations["game"]


def replay():
  global camera, map, location
  camera, map = init_lvl1()
  location = locations["game"]


def exit():
  global runing
  runing = False


def update_menu():
  pass


def update_game():
  map.update()


def event_callback():
  events = pygame.event.get()

  for event in events:
    if event.type == QUIT:
      return exit()

  location[0](events)


def event_game(events):
  for event in events:
    if event.type == KEYDOWN and event.key == K_ESCAPE:
      return show_menu()
    elif event.type == MOUSEBUTTONDOWN:
      if control == "touch":
        for b in buttons:
          if eval(b[5]) and b[0].collidepoint(event.pos):
            b[4]()
            break
        else:
          if event.pos[0] < win_w / 2 - joy.r1:
            joy.set_center(event.pos)
          elif event.pos[0] > win_w / 2 + joy2.r1:
            joy2.set_center(event.pos)
    elif event.type == MOUSEBUTTONUP:
      if control == "touch":
        if joy.visible:
          joy.set_center(None)
        elif joy2.visible:
          joy2.set_center(None)
                    
  joy.calc(events)
  joy2.calc(events)


def event_menu(events):
  for event in events:
    if event.type == MOUSEBUTTONDOWN:
      for b in menu_buttons:
        if eval(b[5]) and b[0].collidepoint(event.pos):
          b[4]()
          break
    elif event.type == KEYDOWN:
      pass
            

def draw():
  location[2]()
  text = font.render('FPS: %i' % clock.get_fps(), True, (0, 0, 0))
  window.blit(text, (win_w - 150, win_h - 40))
  pygame.display.update()


def draw_game():
  window.fill((255, 255, 255))
  map.draw()

  if control == "touch":
    for b in buttons:
      if eval(b[5]):
        window.blit(b[1], b[0])
        text = font.render(b[2].format(**globals()), True, b[3], (255, 255, 255))
        text.set_colorkey((255, 255, 255))
        text.set_alpha(b[3][3])
        text = text.convert_alpha()
        trect = text.get_rect()
        trect.center = b[0].center
        window.blit(text, trect)

  for l in labels:
    if eval(l[4]):
      text = font.render(l[3].format(**globals()), True, l[2], (255, 255, 255))
      text.set_colorkey((255, 255, 255))
      text.set_alpha(l[2][3])
      text = text.convert_alpha()

      if l[1]:
        trect = text.get_rect()
        trect.center = l[0].center
      else:
        trect = l[0].topleft

      window.blit(text, trect)

  window.blit(player.weapon["image"], (20, 60))
  player.draw_bars()

  if control == "touch":
    if joy.visible:
      joy.draw()
    if joy2.visible:
      joy2.draw()


def draw_menu():
  window.blit(menu_bg, (0, 0))

  for b in menu_buttons:
    if eval(b[5]):
      window.blit(b[1], b[0])
      text = font.render(b[2].format(**globals()), True, b[3], (255, 255, 255))
      text.set_colorkey((255, 255, 255))
      text.set_alpha(b[3][3])
      text = text.convert_alpha()
      trect = text.get_rect()
      trect.center = b[0].center
      window.blit(text, trect)




pygame.init()

if android:
  window = pygame.display.set_mode((0, 0), FULLSCREEN)
  win_w, win_h = window.get_size()
  control = "touch"
else:
  win_w, win_h = 900, 600
  window = pygame.display.set_mode((win_w, win_h))
  control = "joy" if pygame.joystick.get_count() else "key"
  control = "touch"


pygame.display.set_caption("B")
clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 30)

player = Player((100, 100), 30, 5)
joy, joy2 = Joy(control, player, 100, 30), Joy2(control, player, 100, 30)
camera = map = None

shadow = pygame.Surface((win_w, win_h))
shadow.fill((0, 0, 0))
shadow.set_alpha(150)
menu_bg = window.copy()
menu_bg.fill((255, 255, 255))
menu_bg.blit(shadow, (0, 0))
btn_img = ramka(None, 200, 50, 10, (0, 255, 0), lw=4, alpha=150)
menu_btn_img = ramka(None, 50, 50, 10, (0, 255, 0), (0, 0, 0), lw=4, alpha=150)

menu_buttons = [
  (pygame.Rect((win_w / 2 - 100, 150, 200, 50)), btn_img, ru("продолжить"), (0, 0, 0, 150), continue_game, "camera"),
  (pygame.Rect((win_w / 2 - 100, 210, 200, 50)), btn_img, ru("новая игра"), (0, 0, 0, 150), replay, "1"),
  (pygame.Rect((win_w / 2 - 100, 270, 200, 50)), btn_img, ru("выход"), (0, 0, 0, 150), exit, "1")
]

buttons = [
  (pygame.Rect((20, win_h - 70, 200, 50)), btn_img, ru("{player.weapon[name]}"), (0, 0, 0, 150), player.change_weapon, "True"),
  (pygame.Rect((240, win_h - 70, 200, 50)), btn_img, ru("перезарядка"), (0, 0, 0, 150), player.reload_weapon, "player.weapon['type'] != 2"),
  (pygame.Rect((win_w - 60, 10, 50, 50)), menu_btn_img, "| |", (0, 0, 0, 150), show_menu, "location != locations['menu']")
]

labels = [
#  (pygame.Rect((20, 70, 200, 40)), False, (0, 0, 0, 150), "{player.weapon[name]}", "True"),
  (pygame.Rect((20, 110, 200, 40)), False, (0, 0, 0, 150), "clip: {player.weapon[clip]}/{player.weapon[full clip]}", "player.weapon['type'] != 2"),
  (pygame.Rect((20, 150, 200, 40)), False, (0, 0, 0, 150), "ammo: {player.weapon[ammo]}", "player.weapon['type'] != 2")
]

locations = {
    "menu": (event_menu, update_menu, draw_menu),
    "game": (event_game, update_game, draw_game)
}
location = locations["menu"]


runing = True
while runing:
  event_callback()
  location[1]()
  draw()
  clock.tick(60)

#sys.stdout.close()
pygame.quit()