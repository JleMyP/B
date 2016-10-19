# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from random import choice, randrange as rnd

from bot import Bot
from block import Block
from others import Map, Camera, Joy, Joy2, Button, Label
from utils import ru



class LocationGame(object):
  def __init__(self, g):
    self.g = g
    win_w, win_h = g["win_w"], g["win_h"]
    self.camera = Camera(win_w, win_h)
    self.map = None

    menu_btn_img = g["menu_btn_img"]
    btn_img = g["btn_img"]
    font = g["font"]
    player = g["player"]

    self.g["joy"].camera = self.g["joy2"].camera = self.camera

    self.buttons = [
      Button((win_w - 60, 10, 50, 50), menu_btn_img, font, "| |", (0, 0, 0, 150), self.show_menu, "g['current_settings']['control'] == 'touch'"),
      Button((20, win_h - 70, 200, 50), btn_img, font, ru("{g[player].weapon[name]}"), (0, 0, 0, 150), player.change_weapon,
        "g['current_settings']['control'] == 'touch'"),
      Button((240, win_h - 70, 200, 50), btn_img, font, ru("перезарядка"), (0, 0, 0, 150), player.reload_weapon,
        "g['current_settings']['control'] == 'touch' and g['player'].weapon['type'] != 2")
    ]

    self.labels = [
      Label((20, 110), font, ru("{g[player].weapon[name]}"), (0, 0, 0, 150)),
      Label((20, 150), font, "clip: {g[player].weapon[clip]}/{g[player].weapon[full clip]}", (0, 0, 0, 150), (255,255,255),
        "g['player'].weapon['type'] != 2"),
      Label((20, 190), font, "ammo: {g[player].weapon[ammo]}", (0, 0, 0, 150), (255,255,255), "g['player'].weapon['type'] != 2")
    ]


  def continue_game(self):
    self.g["locations"]["current"] = self


  def replay(self):
    self.init_lvl1()
    self.continue_game()


  def show_menu(self):
    self.g["locations"]["menu"].show(self)


  def update(self):
    for b in self.buttons:
      b.update(self.__dict__)

    for l in self.labels:
      l.update(self.__dict__)

    if self.map:
      self.map.update()


  def draw(self):
    window = self.g["window"]
    player = self.g["player"]
    current_settings = self.g["current_settings"]
    joy, joy2 = self.g["joy"], self.g["joy2"]

    window.fill((255, 255, 255))
    
    if self.map:
      self.map.draw()

    for b in self.buttons:
      if b.visible:
        b.draw()

    for l in self.labels:
      if l.visible:
        l.draw()

    window.blit(player.weapon["image"], (20, 60))
    player.draw_bars()

    if current_settings["control"] == "touch":
      if joy.visible:
        joy.draw()
      if joy2.visible:
        joy2.draw()


  def event(self, events):
    current_settings = self.g["current_settings"]
    joy, joy2 = self.g["joy"], self.g["joy2"]

    for event in events:
      if event.type == KEYDOWN and event.key == K_ESCAPE:
        return self.show_menu()
      elif event.type == MOUSEBUTTONDOWN:
        for b in self.buttons:
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


  def init_lvl1(self):
    player = self.g["player"]
    camera = self.camera
    win_w, win_h = self.g["win_w"], self.g["win_h"]

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
    self.map = Map('intro', map_w, map_h, camera, player, (100, 100), walls, bots)
