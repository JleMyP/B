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
except ImportError:
  android = False
  os.environ['SDL_VIDEO_CENTERED'] = "1"

from player import Player
from bot import Bot
from block import Block
from others import Map, Camera, Joy, Joy2, Button, Label
from utils import ru, min_max, ramka



def init_lvl1():
  map_w, map_h = win_w + 200, win_h + 200
  player.__init__((0, 0), 40, 5)
  camera.resize(map_w, map_h)

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
  return map


def show_menu(back=False):
  global location, menu_bg
  location = locations["menu"]

  if not back:
    menu_bg = window.copy()
    menu_bg.blit(shadow, (0, 0))

  g = globals()
  for b in menu_buttons:
    b.update(g)

  for l in menu_labels:
    l.update(g)


def show_settings():
  global location, menu_bg
  location = locations["settings"]
  new_settings.clear()
  new_settings.update(current_settings)

  g = globals()
  for b in settings_buttons:
    b.update(g)

  for l in settings_labels:
    l.update(g)


def apply_settings():
  current_settings.clear()
  current_settings.update(new_settings)

  joy.change_control(current_settings["control"])
  joy2.change_control(current_settings["control"])

  show_menu(True)


def change_control():
  if new_settings["control"] == "key":
    new_settings["control"] = "touch"
  elif new_settings["control"] == "touch":
    new_settings["control"] = "joy"
  else:
    new_settings["control"] = "key"

  g = globals()
  for b in settings_buttons:
    b.update(g)


def continue_game():
  global location
  location = locations["game"]


def replay():
  global map
  map = init_lvl1()
  continue_game()


def exit():
  global runing
  runing = False


def update_menu():
  pass


def update_settings():
  pass


def update_game():
  g = globals()

  for b in game_buttons:
    b.update(g)

  for l in game_labels:
    l.update(g)

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
      for b in game_buttons:
        if b.visible and b.rect.collidepoint(event.pos):
          b.func()
          break
      else:
        if current_settings["control"] == "touch":
          if event.pos[0] < win_w / 2 - joy.r1:
            joy.set_center(event.pos)
          elif event.pos[0] > win_w / 2 + joy2.r1:
            joy2.set_center(event.pos)
    elif event.type == MOUSEBUTTONUP:
      if current_settings["control"] == "touch":
        if joy.visible:
          joy.set_center(None)
        elif joy2.visible:
          joy2.set_center(None)
  
  joy.calc(events)
  joy2.calc(events)


def event_settings(events):
  for event in events:
    if event.type == MOUSEBUTTONDOWN:
      for b in settings_buttons:
        if b.visible and b.rect.collidepoint(event.pos):
          b.func()
          break
    elif event.type == KEYDOWN:
      pass


def event_menu(events):
  for event in events:
    if event.type == MOUSEBUTTONDOWN:
      for b in menu_buttons:
        if b.visible and b.rect.collidepoint(event.pos):
          b.func()
          break
    elif event.type == KEYDOWN:
      pass


def draw():
  location[2]()
  text = font.render('FPS: %i' % clock.get_fps(), True, (0, 0, 0))
  window.blit(text, (win_w - 150, win_h - 40))
  pygame.display.update()


def draw_menu():
  window.blit(menu_bg, (0, 0))

  for b in menu_buttons:
    if b.visible:
      b.draw()

  for l in menu_labels:
    if l.visible:
      l.draw()


def draw_settings():
  window.blit(menu_bg, (0, 0))

  for b in settings_buttons:
    if b.visible:
      b.draw()

  for l in settings_labels:
    if l.visible:
      l.draw()


def draw_game():
  window.fill((255, 255, 255))
  map.draw()

  for b in game_buttons:
    if b.visible:
      b.draw()

  for l in game_labels:
    if l.visible:
      l.draw()

  window.blit(player.weapon["image"], (20, 60))
  player.draw_bars()

  if current_settings["control"] == "touch":
    if joy.visible:
      joy.draw()
    if joy2.visible:
      joy2.draw()



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

camera = Camera(win_w, win_h)
map = None

player = Player((100, 100), 30, 5)
joy, joy2 = Joy(control, player, camera, 100, 30), Joy2(control, player, camera, 100, 30)

current_settings = { "control": control }
new_settings = {}

shadow = pygame.Surface((win_w, win_h))
shadow.fill((0, 0, 0))
shadow.set_alpha(150)
menu_bg = window.copy()
menu_bg.fill((255, 255, 255))
menu_bg.blit(shadow, (0, 0))
btn_img = ramka(None, 200, 50, 10, (0, 255, 0), lw=4, alpha=150)
menu_btn_img = ramka(None, 50, 50, 10, (0, 255, 0), (0, 0, 0), lw=4, alpha=150)

menu_buttons = [
  Button((win_w / 2 - 100, 150, 200, 50), btn_img, font, ru("продолжить"), (0, 0, 0, 150), continue_game, "map"),
  Button((win_w / 2 - 100, 210, 200, 50), btn_img, font, ru("новая игра"), (0, 0, 0, 150), replay),
  Button((win_w / 2 - 100, 270, 200, 50), btn_img, font, ru("настройки"), (0, 0, 0, 150), show_settings),
  Button((win_w / 2 - 100, 330, 200, 50), btn_img, font, ru("выход"), (0, 0, 0, 150), exit)
]

menu_labels = [
  Label((win_w / 2 - 100, 100, 200, 50), font, ru("МЕНЮ"), (255,255,255,255), (0,0,0,0), centered=True)
]

settings_buttons = [
  Button((win_w / 2 + 100, 200, 200, 50), btn_img, font, ru("{new_settings[control]}"), (0,0,0,255), change_control),
  Button((win_w / 2 - 100, 340, 200, 50), btn_img, font, ru("принять"), (0, 0, 0, 150), apply_settings),
  Button((win_w / 2 - 100, 400, 200, 50), btn_img, font, ru("отмена"), (0, 0, 0, 150), lambda x=0: show_menu(True))
]

settings_labels = [
  Label((win_w / 2 - 100, 100, 200, 50), font, ru("НАСТРОЙКИ"), (255,255,255,255), (0,0,0,0), centered=True),
  Label((win_w / 2 - 300, 200), font, ru("Управление:"), (255,255,255,255), (0,0,0,0))
]

game_buttons = [
  Button((win_w - 60, 10, 50, 50), menu_btn_img, font, "| |", (0, 0, 0, 150), show_menu, "current_settings['control'] == 'touch'"),
  Button((20, win_h - 70, 200, 50), btn_img, font, ru("{player.weapon[name]}"), (0, 0, 0, 150), player.change_weapon,
    "current_settings['control'] == 'touch'"),
  Button((240, win_h - 70, 200, 50), btn_img, font, ru("перезарядка"), (0, 0, 0, 150), player.reload_weapon,
    "current_settings['control'] == 'touch' and player.weapon['type'] != 2")
]

game_labels = [
  Label((20, 110), font, ru("{player.weapon[name]}"), (0, 0, 0, 150)),
  Label((20, 150), font, "clip: {player.weapon[clip]}/{player.weapon[full clip]}", (0, 0, 0, 150), (255,255,255), "player.weapon['type'] != 2"),
  Label((20, 190), font, "ammo: {player.weapon[ammo]}", (0, 0, 0, 150), (255,255,255), "player.weapon['type'] != 2")
]

locations = {
  "menu": (event_menu, update_menu, draw_menu),
  "settings": (event_settings, update_settings, draw_settings),
  "game": (event_game, update_game, draw_game)
}
show_menu()


runing = True
while runing:
  event_callback()
  location[1]()
  draw()
  clock.tick(60)

#sys.stdout.close()
pygame.quit()