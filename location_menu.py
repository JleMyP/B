# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from others import Button, Label
from utils import ru



class LocationMenu(object):
  def __init__(self, g):
    self.g = g
    self.menu_bg = g["window"].copy()
    self.menu_bg.fill((255, 255, 255))
    self.menu_bg.blit(g["shadow"], (0, 0))

    btn_img = g["btn_img"]
    font = g["font"]
    exit = g["exit"]
    win_w, win_h = g["win_w"], g["win_h"]

    self.buttons = [
      Button((win_w / 2 - 100, 150, 200, 50), btn_img, font, ru("продолжить"), (0, 0, 0, 150), self.g["locations"]["game"].continue_game, "g['locations']['game'].map"),
      Button((win_w / 2 - 100, 210, 200, 50), btn_img, font, ru("новая игра"), (0, 0, 0, 150), self.g["locations"]["game"].replay),
      Button((win_w / 2 - 100, 270, 200, 50), btn_img, font, ru("настройки"), (0, 0, 0, 150), self.show_settings),
      Button((win_w / 2 - 100, 330, 200, 50), btn_img, font, ru("выход"), (0, 0, 0, 150), exit)
    ]

    self.labels = [
      Label((win_w / 2 - 100, 100, 200, 50), font, ru("МЕНЮ"), (255,255,255,255), (0,0,0,0), centered=True)
    ]


  def show(self, prev=None):
    self.g["locations"]["current"] = self

    if prev == self.g["locations"]["game"]:
      self.menu_bg = self.g["window"].copy()
      self.menu_bg.blit(self.g["shadow"], (0, 0))

    for b in self.buttons:
      b.update(self.__dict__)

    for l in self.labels:
      l.update(self.__dict__)


  def draw(self):
    self.g["window"].blit(self.menu_bg, (0, 0))

    for b in self.buttons:
      if b.visible:
        b.draw()

    for l in self.labels:
      if l.visible:
        l.draw()


  def event(self, events):
    for event in events:
      if event.type == MOUSEBUTTONDOWN:
        for b in self.buttons:
          if b.visible and b.rect.collidepoint(event.pos):
            b.func()
            break
      elif event.type == KEYDOWN:
        pass


  def update(self): pass


  def show_settings(self):
    self.g["locations"]["settings"].show(self)
