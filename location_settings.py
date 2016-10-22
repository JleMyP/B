# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from location import Location

from others import Button, Label
from utils import ru



class LocationSettings(Location):
  def __init__(self, g):
    Location.__init__(self, g)

    self.bg = g["locations"]["menu"].bg
    self.current_settings = g["current_settings"]
    self.joy = g["joy"]
    self.joy2 = g["joy2"]

    self.new_settings = {}

    menu_btn_img = g["menu_btn_img"]
    btn_img = g["btn_img"]

    self.buttons = [
      Button((self.win_w / 2 + 100, 200, 200, 50), btn_img, self.font, ru("{new_settings[control]}"), (0,0,0,150), self.change_control),
      Button((self.win_w / 2 - 100, 340, 200, 50), btn_img, self.font, ru("принять"), (0,0,0,150), self.apply),
      Button((self.win_w / 2 - 100, 400, 200, 50), btn_img, self.font, ru("отмена"), (0,0,0,150), self.shower_location("menu"))
    ]

    self.labels = [
      Label((self.win_w / 2 - 100, 100, 200, 50), self.font, ru("НАСТРОЙКИ"), (255,255,255,255), (0,0,0,0)),
      Label((self.win_w / 2 - 300, 200), self.font, ru("Управление:"), (255,255,255,255), (0,0,0,0))
    ]


  def show(self, prev):
    self.bg = self.locations["menu"].bg
    self.new_settings.clear()
    self.new_settings.update(self.current_settings)

    Location.show(self)


  def draw(self):
    self.window.blit(self.bg, (0, 0))

    Location.draw(self)


  def apply(self):
    self.joy.change_control(self.new_settings["control"])
    self.joy2.change_control(self.new_settings["control"])

    self.current_settings.clear()
    self.current_settings.update(self.new_settings)

    self.locations["menu"].show(self)


  def change_control(self):
    if self.new_settings["control"] == "key":
      self.new_settings["control"] = "touch"
    elif self.new_settings["control"] == "touch":
      self.new_settings["control"] = "joy"
    else:
      self.new_settings["control"] = "key"

    for b in self.buttons:
      b.update(self.__dict__)
