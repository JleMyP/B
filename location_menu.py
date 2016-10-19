# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

from others import Map, Camera, Joy, Joy2, Button, Label
from location_game import LocationGame
from utils import ru



class LocationMenu(object):
  def __init__(self, g):
    self.g = g
    self.menu_bg = g.window.copy()
    self.menu_bg.fill((255, 255, 255))
    self.menu_bg.blit(shadow, (0, 0))

    self.buttons = [
      Button((win_w / 2 - 100, 150, 200, 50), g.btn_img, g.font, ru("продолжить"), (0, 0, 0, 150), self.continue_game, "self.g.locations.game.map"),
      Button((win_w / 2 - 100, 210, 200, 50), g.btn_img, g.font, ru("новая игра"), (0, 0, 0, 150), self.replay),
      Button((win_w / 2 - 100, 270, 200, 50), g.btn_img, g.font, ru("настройки"), (0, 0, 0, 150), self.show_settings),
      Button((win_w / 2 - 100, 330, 200, 50), g.btn_img, g.font, ru("выход"), (0, 0, 0, 150), g.exit)
    ]

    self.labels = [
      Label((g.win_w / 2 - 100, 100, 200, 50), g.font, ru("МЕНЮ"), (255,255,255,255), (0,0,0,0), centered=True)
    ]


  def show(self, prev):
    self.g.locations["current"] = self

    if pref is LocationGame:
      self.menu_bg = self.g.window.copy()
      self.menu_bg.blit(self.g.shadow, (0, 0))

    for b in self.buttons:
      b.update(self.g)

    for l in slf.labels:
      l.update(self.g)


  def draw(self):
    self.g.window.blit(self.menu_bg, (0, 0))

    for b in self.buttons:
      if b.visible:
        b.draw()

    for l in slf.labels:
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


  def exit():
    global runing
    runing = False
