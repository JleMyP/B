# -*- coding: utf-8 -*-

import geom
import pygame
from pygame.locals import *



class Map(object):
  def __init__(self, name, w, h, camera, player, player_pos=(100, 100), walls=(), bots=(), load=False):
    self.name, self.filename = name, 'levels/%s.txt' % name
    self.w, self.h = w, h
    self.camera = camera
    self.player = player
    self.bullets = pygame.sprite.Group()

    if load:
      self.load()
      return

    self.walls = pygame.sprite.Group(*walls)
    self.bots = pygame.sprite.Group(*bots)

    for b in bots:
      b.map = self
      b.camera = camera
      b.player = player

    player.rect.center = player_pos
    camera.set_center(player_pos)
    player.camera = camera
    player.map = self
    #camera.resize(w, h)
   

  def update(self):
    self.player.update()
    self.bullets.update()
    self.bots.update()
  

  def draw(self):
    lst = self.walls.sprites() + self.bots.sprites() + self.bullets.sprites()

    for w in self.camera.rect.collidelistall(lst):
      lst[w].draw()

    self.player.draw()
  

  def save(self):
    with open(self.filename, 'w') as f:
      f.write('WALLS\n')
      for w in self.walls.sprites():
        f.write(str(w.points[:-1]) + '\n')

      f.write('BOTS\n')
      for b in self.bots.sprites():
        f.write(str(b.rect.center) + '\n')



class Camera(object):
  def __init__(self, center, map_w, map_h, shift=30):
    window = pygame.display.get_surface()
    self.win_w, self.win_h = window.get_size()

    self.shift = shift
    self.rect = pygame.Rect((0, 0, self.win_w, self.win_h))
    self.resize(map_w, map_h)

    if center:
      self.set_center(center)
  

  def resize(self, map_w, map_h):
    self.max_x, self.max_y = map_w + self.shift, map_h + self.shift

    if self.win_w >= map_w:
      self.rect.x = -(win_w - map_w) // 2
      self.max_x = self.rect.right

    if self.win_h >= map_h:
      self.rect.y = -(win_h - map_h) // 2
      self.max_y = self.rect.bottom
  

  def set_center(self, center):
    self.rect.center = center

    if self.rect.x < -self.shift:
      self.rect.x = -self.shift

    if self.rect.right > self.max_x:
      self.rect.right = self.max_x

    if self.rect.y < -self.shift:
      self.rect.y = -self.shift

    if self.rect.bottom > self.max_y:
      self.rect.bottom = self.max_y



class Joy(object):
  def __init__(self, control, player, r1=0, r2=0):
    self.control = control
    self.player = player

    if control == "touch":
      self.visible = False
      self.r1, self.r2 = r1, r2
      self.r = r1 - r2 - 10

      image = pygame.Surface((r1 * 2, r1 * 2))
      image.fill(0)
      pygame.draw.circle(image, (0, 255, 0), (r1, r1), r1)
      image.set_colorkey((0, 0, 0))
      image.set_alpha(100)
      self.image = image.convert_alpha()
      self.rect = self.image.get_rect()
    elif control == "joy":
      self.joystick = pygame.joystick.Joystick(0)
      self.fire_button = 0
      self.joystick.init()
  

  def set_center(self, pos):
    if not pos:
      self.visible = False

      if not isinstance(self, Joy2):
        self.player.speedx = self.player.speedy = 0
    else:
      self.rect.center, self.visible = pos, True
  

  def calc(self, events):
    if self.control == "touch" and self.visible:
      self.pos = pygame.mouse.get_pos()

      if self.pos != self.rect.center:
        a = geom.angle_to_point(self.rect.center, self.pos)
        speed = geom.m_vektor(self.rect.center, self.pos)

        if speed > self.r:
          self.pos = geom.move(a, self.r, self.rect.center)
          speed = self.r

        self.player.speedx, self.player.speedy = geom.move(a, self.player.speed * (speed / self.r))
        self.player.set_dir(a)
    elif self.control == "key":
      pressed = pygame.key.get_pressed()

      if pressed[K_LEFT] and not pressed[K_RIGHT] or pressed[K_a] and not pressed[K_d]:
        self.player.speedx = -self.player.speed
      elif pressed[K_RIGHT] and not pressed[K_LEFT] or pressed[K_d] and not pressed[K_a]:
        self.player.speedx = self.player.speed
      else:
        self.player.speedx = 0

      if pressed[K_UP] and not pressed[K_DOWN] or pressed[K_w] and not pressed[K_s]:
        self.player.speedy = -self.player.speed
      elif pressed[K_DOWN] and not pressed[K_UP] or pressed[K_s] and not pressed[K_w]:
        self.player.speedy = self.player.speed
      else:
        self.player.speedy = 0
      
      for e in events:
        if e.type == KEYDOWN:
          if e.key == K_r:
            self.player.reload_weapon()

          if e.key == K_q:
            self.player.change_weapon()
    elif self.control == "joy":
      self.player.speedx = self.player.speed * self.joystick.get_axis(0)
      self.player.speedy = self.player.speed * self.joystick.get_axis(1)
  

  def draw(self):
    window.blit(self.image, self.rect)
    pygame.draw.circle(window, (255, 0, 0), self.pos, self.r2)



class Joy2(Joy):
  fire_key_joy = 5
  mouse_state = "up"
    
  def calc(self, events):
    if self.control == "touch" and self.visible:
      self.pos = pos = pygame.mouse.get_pos()

      if pos != self.rect.center:
        a = geom.angle_to_point(self.rect.center, pos)
        self.player.set_dir(a)

        if geom.m_vektor(self.rect.center, pos) > self.r:
          self.pos = geom.move(a, self.r, self.rect.center)

        self.player.fire()
    elif self.control == "key":
      for e in events:
        if e.type == MOUSEBUTTONDOWN:
          self.mouse_state = "down"
        elif e.type == MOUSEBUTTONUP:
          self.mouse_state = "up"

      self.player.set_dir(geom.angle_to_point(self.player.rect.move(-self.camera.rect.x, -self.camera.rect.y).center, pygame.mouse.get_pos()))

      if pygame.mouse.get_pressed()[0] and self.mouse_state == "down":
        self.player.fire()
    elif self.control == "joy":
      x, y = int(1000 * self.joystick.get_axis(2)), int(1000 * self.joystick.get_axis(3))

      if x != 0 and y != 0:
        self.player.set_dir(geom.angle_to_point((0, 0), (x, y)))
      if self.joystick.get_button(self.fire_button):
        self.player.fire()