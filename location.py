# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *



class Location(object):
  def __init__(self, dict):
    self.locations = dict["locations"]
    self.window = dict["window"]
    self.font = dict["font"]
    self.win_w = dict["win_w"]
    self.win_h = dict["win_h"]


  def show(self, prev=None):
    self.locations["current"] = self

    for b in self.buttons:
      b.update(self.__dict__)

    for l in self.labels:
      l.update(self.__dict__)


  def shower_location(self, location):
    return lambda x=0: self.locations[location].show(self)


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


  def draw(self):
    for b in self.buttons:
      if b.visible:
        b.draw()

    for l in self.labels:
      if l.visible:
        l.draw()