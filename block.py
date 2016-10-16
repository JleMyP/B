import geom
import pygame
from pygame.locals import *

from utils import *



class Block(pygame.sprite.Sprite):
  def __init__(self, points, camera):
    pygame.sprite.Sprite.__init__(self)

    if isinstance(points, tuple):
      x, y, w, h = points
      points = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]

    x1, x2 = min_max([p[0] for p in points])
    y1, y2 = min_max([p[1] for p in points])
    self.rect = pygame.Rect((x1, y1, x2 - x1 + 2, y2 - y1 + 2))

    image = pygame.Surface((x2 - x1 + 3, y2 - y1 + 3))
    image.fill(0)
    pp = [(p[0] - x1 + 1, p[1] - y1 + 1) for p in points]
    pygame.draw.polygon(image, (80, 170, 255), pp)
    pygame.draw.lines(image, (0, 0, 255), True, pp, 3)
    image.set_colorkey((0, 0, 0))
    self.image = image.convert_alpha()
    
    self.camera = camera
    self.points = points + [points[0]]
    self.func_list = [
      (geom.get_func(self.points[i], self.points[i + 1]), geom.get_func(self.points[i], self.points[i + 1], 2))
      for i in range(len(points))
    ]
  

  def draw(self):
    window = pygame.display.get_surface()
    window.blit(self.image, self.rect.move(-self.camera.rect.x, -self.camera.rect.y))
  

  def collide_line_old(self, funcx, funcy, interval=None):
    points = []

    if not funcx:
      if not interval:
        if self.rect.left <= funcy(0) <= self.rect.right:
          points += [self.rect.top, self.rect.bottom]
      elif interval[0] <= self.rect.top <= interval[1]:
        points.append(self.rect.top)
      elif interval[0] <= self.rect.bottom <= interval[1]:
        points.append(self.rect.bottom)
    elif not funcy:
      if not interval:
        if self.rect.top <= funcx(0) <= self.rect.bottom:
         points += [self.rect.left, self.rect.right]
      elif interval[0] <= self.rect.left <= interval[1]:
        points.append(self.rect.left)
      elif interval[0] <= self.rect.right <= interval[1]:
        points.append(self.rect.right)
    else:
      ctop, cbottom = funcy(self.rect.top), funcy(self.rect.bottom)
      ps = []

      if self.rect.left <= ctop <= self.rect.right:
        ps.append(ctop)

      if self.rect.left <= cbottom <= self.rect.right:
        ps.append(cbottom)

      if self.rect.top <= funcx(self.rect.left) <= self.rect.bottom:
        ps.append(self.rect.left)

      if self.rect.top <= funcx(self.rect.right) <= self.rect.bottom:
        ps.append(self.rect.right)

      if interval:
        points += [p for p in ps if interval[0] <= p <= interval[1]]
      else:
        points += ps

    return points
  

  def collide_line(self, funcx, funcy, interval=None):
    points = []

    for i in range(len(self.func_list)):
      fx, fy = self.func_list[i]
      p = geom.point_in_lines_f(fx, fy, funcx, funcy, interval)

      if not p:
        continue

      if not fx and funcx:
        y1, y2 = min_max(self.points[i][1], self.points[i + 1][1])

        if y1 <= funcx(p) <= y2:
          points.append(p)
      elif not fy and not funcx:
        x1, x2 = min_max(self.points[i][0], self.points[i + 1][0])

        if x1 <= funcy(p) <= x2:
          points.append(p)
      else:
        x1, x2 = min_max(self.points[i][0], self.points[i + 1][0])

        if x1 <= p <= x2:
          points.append(p)

    return points