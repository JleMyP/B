# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from location import Location

from others import Button, Label
from utils import ru



class LocationMenu(Location):
  def __init__(self, g):
    Location.__init__(self, g)

    self.shadow = g["shadow"]
    self.bg = g["window"].copy()
    self.bg.fill((255, 255, 255))
    self.bg.blit(g["shadow"], (0, 0))

    btn_img = g["btn_img"]
    btn_img2 = g["btn_img2"]
    exit = g["exit"]

    self.buttons = [
      Button((self.win_w / 2 - 100, 150, 200, 50), btn_img, self.font, ru("продолжить"), (0,0,0,150), self.shower_location("game"), "locations['game'].map"),
      Button((self.win_w / 2 - 100, 210, 200, 50), btn_img, self.font, ru("новая игра"), (0,0,0,150), self.locations["game"].replay),
      Button((self.win_w / 2 - 100, 270, 200, 50), btn_img, self.font, ru("настройки"), (0,0,0,150), self.shower_location("settings")),
      Button((self.win_w / 2 - 100, 330, 200, 50), btn_img2, self.font, ru("выход"), (0,0,0,150), exit)
    ]

    self.labels = [
      Label((self.win_w / 2 - 100, 100, 200, 50), self.font, ru("МЕНЮ"), (255,255,255,255), (0,0,0,255))
    ]


  def show(self, prev=None):
    if prev == self.locations["game"]:
      self.bg = self.window.copy()
      self.bg.blit(self.shadow, (0, 0))

    Location.show(self)


  def draw(self):
    self.window.blit(self.bg, (0, 0))

    Location.draw(self)
