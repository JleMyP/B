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
    self.locations = g["locations"]
    self.window = g["window"]
    self.win_w, self.win_h = g["win_w"], g["win_h"]
    self.current_settings = g["current_settings"]
    self.player = g["player"]
    self.joy = g["joy"]
    self.joy2 = g["joy2"]

    self.camera = Camera(self.win_w, self.win_h)
    self.map = None

    menu_btn_img = g["menu_btn_img"]
    btn_img = g["btn_img"]
    font = g["font"]

    g["joy"].camera = g["joy2"].camera = self.camera

    self.buttons = [
      Button((self.win_w - 60, 10, 50, 50), menu_btn_img, font, "| |", (0, 0, 0, 150), self.show_menu, "current_settings['control'] == 'touch'"),
      Button((20, self.win_h - 70, 200, 50), btn_img, font, ru("{player.weapon[name]}"), (0, 0, 0, 150), self.player.change_weapon,
        "current_settings['control'] == 'touch'"),
      Button((240, self.win_h - 70, 200, 50), btn_img, font, ru("перезарядка"), (0, 0, 0, 150), self.player.reload_weapon,
        "current_settings['control'] == 'touch' and player.weapon['type'] != 2")
    ]

    self.labels = [
      Label((20, 110), font, ru("{player.weapon[name]}"), (0, 0, 0, 150)),
      Label((20, 150), font, "clip: {player.weapon[clip]}/{player.weapon[full clip]}", (0, 0, 0, 150), (255,255,255),
        "player.weapon['type'] != 2"),
      Label((20, 190), font, "ammo: {player.weapon[ammo]}", (0, 0, 0, 150), (255,255,255), "player.weapon['type'] != 2")
    ]


  def continue_game(self):
    self.locations["current"] = self


  def replay(self):
    self.init_lvl1()
    self.continue_game()


  def show_menu(self):
    self.locations["menu"].show(self)


  def update(self):
    for b in self.buttons:
      b.update(self.__dict__)

    for l in self.labels:
      l.update(self.__dict__)

    if self.map:
      self.map.update()


  def draw(self):
    self.window.fill((255, 255, 255))
    
    if self.map:
      self.map.draw()

    for b in self.buttons:
      if b.visible:
        b.draw()

    for l in self.labels:
      if l.visible:
        l.draw()

    self.window.blit(self.player.weapon["image"], (20, 60))
    self.player.draw_bars()

    if self.current_settings["control"] == "touch":
      if self.joy.visible:
        self.joy.draw()
      if self.joy2.visible:
        self.joy2.draw()


  def event(self, events):
    for event in events:
      if event.type == KEYDOWN and event.key == K_ESCAPE:
        return self.show_menu()
      elif event.type == MOUSEBUTTONDOWN:
        for b in self.buttons:
          if b.visible and b.rect.collidepoint(event.pos):
            b.func()
            break
        else:
          if self.current_settings["control"] == "touch":
            if event.pos[0] < self.win_w / 2 - self.joy.r1:
              self.joy.set_center(event.pos)
            elif event.pos[0] > self.win_w / 2 + self.joy2.r1:
              self.joy2.set_center(event.pos)
      elif event.type == MOUSEBUTTONUP:
        if self.current_settings["control"] == "touch":
          if self.joy.visible:
            self.joy.set_center(None)
          elif self.joy2.visible:
            self.joy2.set_center(None)
  
    self.joy.calc(events)
    self.joy2.calc(events)


  def init_lvl1(self):
    map_w, map_h = self.win_w + 200, self.win_h + 200
    self.player.__init__((0, 0), 40, 5)
    self.camera.resize(map_w, map_h)

    walls = [
      Block((0, 0, 20, map_h), self.camera),
      Block((20, 0, map_w - 20, 20), self.camera),
      Block((map_w - 20, 20, 20, map_h - 20), self.camera),
      Block((20, map_h - 20, map_w - 40, 20), self.camera),
      Block((460, 20, 20, map_h / 2 - 50), self.camera),
      Block((460, map_h / 2 + 30, 20, map_h / 2 - 50), self.camera),
      Block((780, 20, 20, map_h / 2 * 0.75), self.camera),
      Block((780, map_h / 2 * 1.25 - 20, 20, map_h / 2 * 0.75), self.camera),
      Block([(200, 400), (300, 500), (220, 470)], self.camera)
    ]

    bots = [Bot([(rnd(550, map_w - 50), rnd(50, map_h - 50))], 90, 200) for x in xrange(10)]    
    self.map = Map('intro', map_w, map_h, self.camera, self.player, (100, 100), walls, bots)
