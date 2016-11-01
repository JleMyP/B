# -*- coding: utf-8 -*-

import geom
import pygame
from pygame.locals import *

from utils import min_max
from bot import Bot



class Bulet(pygame.sprite.Sprite):
  def __init__(self, map, camera, pos, dir, through=False, speed=10, r=3):
    pygame.sprite.Sprite.__init__(self)

    self.window = pygame.display.get_surface()
    self.map = map
    self.camera = camera
    self.through = through
    self.rect = pygame.Rect((pos[0] - r, pos[1] - r, r * 2, r * 2))
    self.speedx, self.speedy = geom.move(dir, speed)
    self.fx = geom.get_func_a(pos, dir)
    self.fy = geom.get_func_a(pos, dir, 2)
    self.px, self.py = pos


  def update(self):
    sprites = self.map.bots.sprites() + self.map.walls.sprites()
    lst = []

    if not self.fx:
      interval = min_max(self.py, self.py + self.speedy)

      for x in sprites:
        points = x.collide_line(self.fx, self.fy, interval)

        if points:
          if self.speedy > 0:
            lst.append((x, min(points)))
          else:
            lst.append((x, max(points)))
      lst.sort(key=lambda a: a[1], reverse=(self.speedy < 0))
    else:
      interval = min_max(self.px, self.px + self.speedx)

      for x in sprites:
        points = x.collide_line(self.fx, self.fy, interval)

        if points:
          if self.speedx > 0:
            lst.append((x, min(points)))
          else:
            lst.append((x, max(points)))

      lst.sort(key=lambda a: a[1], reverse=(self.speedx < 0))

    if lst:
      if isinstance(lst[0][0], Bot):
        lst[0][0].kill()

        if self.through:
          return

      self.kill()
    else:
      self.px = self.px + self.speedx
      self.py = self.py + self.speedy
      self.rect.center = self.px, self.py
  

  def draw(self):
    pygame.draw.circle(self.window, (255,0,0), self.rect.move(-self.camera.rect.x, -self.camera.rect.y).center, self.rect.width / 2)
