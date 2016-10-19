# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from others import Button, Label
from utils import ru



class LocationSettings(object):
  def __init__(self, g):
    self.g = g
    self.new_settings = {}

    win_w, win_g = g["win_w"], g["win_h"]
    menu_btn_img = g["menu_btn_img"]
    btn_img = g["btn_img"]
    font = g["font"]

    self.buttons = [
      #Button((win_w / 2 + 100, 200, 200, 50), btn_img, font, ru("{new_settings[control]}"), (0,0,0,255), self.change_control),
      #Button((win_w / 2 - 100, 340, 200, 50), btn_img, font, ru("принять"), (0, 0, 0, 150), self.apply_settings),
      #Button((win_w / 2 - 100, 400, 200, 50), btn_img, font, ru("отмена"), (0, 0, 0, 150), self.show_menu

      Button((win_w / 2 - 100, 150, 200, 50), btn_img, font, ru("продолжить"), (0, 0, 0, 150), dir, "g['locations']['game'].map"),
      Button((win_w / 2 - 100, 210, 200, 50), btn_img, font, ru("новая игра"), (0, 0, 0, 150), dir),
      Button((win_w / 2 - 100, 270, 200, 50), btn_img, font, ru("настройки"), (0, 0, 0, 150), dir),
      Button((win_w / 2 - 100, 330, 200, 50), btn_img, font, ru("выход"), (0, 0, 0, 150), dir)
    ]

    self.labels = [
#      Label((win_w / 2 - 100, 100, 200, 50), font, ru("НАСТРОЙКИ"), (255,255,255,255), (0,0,0,0), centered=True),
#      Label((win_w / 2 - 300, 200), font, ru("Управление:"), (255,255,255,255), (0,0,0,0))
    ]


  def draw(self):
    self.g["window"].blit(self.g["menu_bg"], (0, 0))

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


  def show_menu(self):
    self.g["locations"]["menu"].show(self)


  def show(self, prev):
    self.g["locations"]["current"] = self
    self.new_settings.clear()
    self.new_settings.update(self.g["current_settings"])

    for b in self.buttons:
      b.update(self.__dict__)

    for l in self.labels:
      l.update(self.__dict__)


  def apply():
    self.g.joy.change_control(self.new_settings["control"])
    self.g.joy2.change_control(self.new_settings["control"])

    self.g.current_settings.clear()
    self.g.current_settings.update(self.new_settings)

    self.show_menu()


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