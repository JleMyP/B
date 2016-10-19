import geom
import pygame
from pygame.locals import *
from random import choice, randrange as rnd

from utils import *



class Bot(pygame.sprite.Sprite):
  def __init__(self, points, angle, r=200, speed=2, size=30):
    pygame.sprite.Sprite.__init__(self)

    image = pygame.Surface((40, 35))
    image.fill((255, 255, 255))
    image.set_colorkey((255, 255, 255))
    image.blit(pygame.image.load("images/z1.png"), (0, 0))
    self.image = image.convert_alpha()
    self.mask = pygame.mask.from_surface(self.image)
    self.rect = self.image.get_rect()
    
    self.activ, self.chaos = False, None
    self.points, self.angle, self.r = points, angle, r
    self.speed, self.size = speed, size
    self.rect.center = points[0]
    self.dir = None

    if len(self.points) == 1:
      self.chaos = [rnd(360), rnd(50, 150), 0, False]
      self.set_dir(self.chaos[0])
    else:
      self.next = 1
      self.set_dir(geom.angle_to_point(self.rect.center, points[1]))
  

  def set_dir(self, dir):
    if self.dir == dir:
      return

    self.dir = dir
    self.a1 = geom.convert(dir - self.angle / 2)
    self.a2 = geom.convert(dir + self.angle / 2)
    self.fx = geom.get_func_a(self.rect.center, dir)
    self.fy = geom.get_func_a(self.rect.center, dir, 2)
    self.speedx, self.speedy = geom.move(dir, self.speed)
    

  def move(self):
    lst = self.map.walls.sprites() + self.map.bots.sprites() + [self.player]
    lst.remove(self)

    if self.speedx:
      self.rect.move_ip(self.speedx, 0)

      for w in lst:
        if pygame.sprite.collide_rect(self, w):
          if self.speedx < 0:
            self.rect.left = w.rect.right
          else:
            self.rect.right = w.rect.left

          if self.chaos:
            self.chaos[3] = True

    if self.speedy:
      self.rect.move_ip(0, self.speedy)

      for w in lst:
        if pygame.sprite.collide_rect(self, w):
          if self.speedy < 0:
            self.rect.top = w.rect.bottom
          else:
            self.rect.bottom = w.rect.top

          if self.chaos:
            self.chaos[3] = True

    if self.chaos:
      self.chaos[2] += geom.mv((self.speedx, self.speedy))
  

  def calc_path(self):
    if self.rect.center == self.points[self.next]:
      self.next += 1

      if self.next == len(self.points):
        self.next = 0

      self.set_dir(geom.angle_to_point(self.rect.center, self.points[self.next]))
    elif geom.m_vektor(self.rect.center, self.points[self.next]) < self.speed:
      self.speedx = self.points[self.next][0] - self.rect.centerx
      self.speedy = self.points[self.next][0] - self.rect.centery
  

  def calc_path_chaos(self):
    if self.chaos[2] >= self.chaos[1] or self.chaos[3]:
      self.chaos = [rnd(360), rnd(50, 150), 0, False]
      self.set_dir(self.chaos[0])
  

  def find(self):
    if geom.m_vektor(self.player.rect.center, self.rect.center) > self.r:
      return False

    a = geom.angle_to_point(self.rect.center, self.player.rect.center)

    return (self.dir - self.angle / 2 < 0 or self.dir + self.angle / 2 > 360) and (a >= self.a1 or a <= self.a2) \
      or self.a2 - self.a1 == self.angle and self.a1 <= a <= self.a2


  def find_wall(self):
    if not self.fx:
      interval = min_max(self.rect.centery, self.player.rect.centery)
    else:
      interval = min_max(self.rect.centerx, self.player.rect.centerx)

    for w in self.map.walls.sprites():
      points = w.collide_line(self.fx, self.fy, interval)

      if points:
        return w

    return False


  def update(self):
    if not self.activ:
      self.activ = self.find() and not self.find_wall()

      if self.activ:
        self.speed *= 2
    elif self.find_wall():
      self.activ = False
      self.speed /= 2

    if self.activ:
      self.set_dir(geom.angle_to_point(self.rect.center, self.player.rect.center))
    else:
      if self.chaos:
        self.calc_path_chaos()
      else:
        self.calc_path()

    self.move()


  def draw(self):
    window = pygame.display.get_surface()
    rect = self.rect.move(-self.camera.rect.x, -self.camera.rect.y)

    p1 = geom.move(self.dir - self.angle / 2, self.r, rect.center)
    p2 = geom.move(self.dir + self.angle / 2, self.r, rect.center)
    pygame.draw.line(window, 0, rect.center, p1, 2)
    pygame.draw.line(window, 0, rect.center, p2, 2)

    a1 = geom.radians(self.dir - self.angle / 2)
    a2 = geom.radians(self.dir + self.angle / 2)
    color = (0, 255, 0) if not self.activ else (255, 0, 0)

    pygame.draw.arc(window, color, (rect.centerx - self.r, rect.centery - self.r, self.r * 2, self.r * 2), a1, a2, 5)
    window.blit(self.image, rect)


  def collide_line(self, funcx, funcy, interval=None):
    return geom.circle_collide_line(self.rect.center, self.rect.width / 2, funcx, funcy, interval)