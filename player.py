# -*- coding: utf-8 -*-

import geom
import pygame
from pygame.locals import *

from utils import *
from bullet import Bulet



class Player(pygame.sprite.Sprite):
  def __init__(self, pos, w, speed):
    pygame.sprite.Sprite.__init__(self)

    self.window = pygame.display.get_surface()
    self.image = pygame.image.load("images/small.png").convert_alpha()
    self.rect = pygame.Rect(pos + (max(self.image.get_size()),)*2)
    self.bar = pygame.Rect((20, 20, 200, 40))

    self.speed = speed
    self.dir = 0
    self.speedx = self.speedy = 0
    self.hp = self.full_hp = 100

    self.reload_images = [pygame.image.load("images/reload/%i.png" % x).convert_alpha() for x in range(15)]

    image_pistolet = pygame.image.load("images/1.png").convert_alpha()
    image_mp5 = pygame.image.load("images/5.png").convert_alpha()
    image_bita = pygame.image.load("images/knife1.png").convert_alpha()

    self.weapons = [
      {
        'type': 1, 'name': ru("пигаль"), 'reload delay set': 30,
        'delay set': 15, 'delay': 0, 'reload delay': 0, 'damag': 5,
        'clip': 6, 'full clip': 6, 'ammo': 36,
        'single shot': True, 'through': False,
        'image': image_pistolet
      },
      {
        'type': 1, 'name': 'mp5', 'reload delay set': 30,
        'delay set': 5, 'delay': 0, 'reload delay': 0, 'damag': 5,
        'clip': 30, 'full clip': 30, 'ammo': 120,
        'single shot': False, 'through': False,
        'image': image_mp5
      },
      {
        'type': 2, 'name': ru("меч ыыы"), 'distance': 50, 'delay set': 15,
        'delay': 0, 'side': 1, 'angle': None, 'n': 0,
        'image': image_bita
      }
    ]

    self.weapon = self.weapons[0]
    self.update_image()
  
  
  def set_dir(self, dir):
    if self.dir == dir:
      return

    self.dir = dir
    self.update_image()


  def change_weapon(self):
    if self.weapon.get('angle'):
      return

    if self.weapon.get('reload delay'):
      self.weapon['reload delay'] = 0

    n = self.weapons.index(self.weapon) + 1
    self.weapon = self.weapons[n if n != len(self.weapons) else 0]


  def reload_weapon(self):
    if self.weapon.get('ammo') and self.weapon['clip'] != self.weapon['full clip'] and not self.weapon["reload delay"]:
      self.weapon["reload delay"] = self.weapon["reload delay set"]


  def fire(self):
    if self.weapon['delay']:
      return

    if self.weapon.get('clip') and not self.weapon["reload delay"]:
      self.weapon["clip"] -= 1

      if self.weapon["clip"]:
        self.weapon['delay'] = self.weapon['delay set']

      self.map.bullets.add(Bulet(self.map, self.camera, self.rect.center, self.dir, self.weapon["through"], 30))
    elif self.weapon.get('angle', 1) is None:
      self.weapon['angle'] = self.dir - 60 * self.weapon['side']
      self.weapon['n'] = 12


  def update_image(self):
    if self.weapon.get("full clip") and self.weapon["reload delay"]:
      img = self.reload_images[(self.weapon["reload delay"] - 1) / 2]
    else:
      img = self.image

    self.img_rot = pygame.transform.rotate(img, self.dir)
    rect = img.get_rect()
    rect.center = self.rect.center
    self.rect = rect
    self.mask = pygame.mask.from_surface(pygame.transform.rotate(self.img_rot, self.dir))


  def update_weapons(self):
    if self.weapon['delay']:
      self.weapon['delay'] -= 1

    if self.weapon.get('reload delay'):
      self.update_image()
      self.weapon['reload delay'] -= 1

      if not self.weapon['reload delay']:
        req = self.weapon["full clip"] - self.weapon["clip"]
        add = req if req <= self.weapon["ammo"] else self.weapon["ammo"]

        self.weapon["clip"] += add
        self.weapon["ammo"] -= add
    elif self.weapon.get('angle') is not None:
      self.weapon['angle'] += self.weapon['side'] * 10
      self.weapon['n'] -= 1

      if not self.weapon['n']:
        self.weapon['delay'], self.weapon['side'] = self.weapon['delay set'], -self.weapon['side']
        self.weapon['angle'] = None
      else:
        fx = geom.get_func_a(self.rect.center, self.weapon['angle'])
        fy = geom.get_func_a(self.rect.center, self.weapon['angle'], 2)
        p = geom.move(self.weapon['angle'], self.weapon['distance'], self.rect.center)
        minx, maxx = min_max(self.rect.centerx, p[0])
        miny, maxy = min_max(self.rect.centery, p[1])
        interval = (miny, maxy) if not fx else (minx, maxx)
        s = pygame.sprite.Sprite()
        s.rect = pygame.Rect((minx, miny, maxx - minx, maxy - miny))

        for w in self.map.walls.sprites():
          if pygame.sprite.collide_rect(s, w) and w.collide_line(fx, fy, interval):
            self.weapon['delay'], self.weapon['angle'] = self.weapon['delay set'] * 2, None
            break
        else:
          for b in self.map.bots.sprites():
            if geom.m_vektor(self.rect.center, b.rect.center) < (self.rect.width + b.rect.width) / 2 + \
              self.weapon['distance']:
              #xx = min_max(self.rect.centerx, b.rect.centerx)
              #yy = min_max(self.rect.centery, b.rect.centery)

              if b.collide_line(fx, fy, interval):
                b.kill()
                break
  

  def update(self):
    self.update_weapons()
    sprites = self.map.walls.sprites() + self.map.bots.sprites()

    if self.speedx:
      self.rect.move_ip(self.speedx, 0)

      for w in sprites:
        if pygame.sprite.collide_rect(self, w):
          if self.speedx < 0:
            self.rect.left = w.rect.right
          else:
            self.rect.right = w.rect.left

    if self.speedy:
      self.rect.move_ip(0, self.speedy)

      for w in sprites:
        if pygame.sprite.collide_rect(self, w):
          if self.speedy < 0:
            self.rect.top = w.rect.bottom
          else:
            self.rect.bottom = w.rect.top

    if self.camera.rect.center != self.rect.center:
      self.camera.set_center(self.rect.center)
    

  def update2(self):
    self.update_weapons()

    if self.speedx:
      self.rect.move_ip(self.speedx, 0)

      for s in self.map.walls.sprites() + self.map.bots.sprites():
        if pygame.sprite.collide_mask(self, s):
          self.rect.move_ip(-self.speedx, 0)
          break
                  
    if self.speedy:
      self.rect.move_ip(0, self.speedy)

      for s in self.map.walls.sprites() + self.map.bots.sprites():
        if pygame.sprite.collide_mask(self, s):
          self.rect.move_ip(0, -self.speedy)
          break

    if self.camera.rect.center != self.rect.center:
      self.camera.set_center(self.rect.center)


  def draw(self):
    rect = self.rect.move(-self.camera.rect.x, -self.camera.rect.y)

    if self.weapon.get('angle') is not None:
      p = geom.move(self.weapon['angle'], self.weapon['distance'], rect.center)
      pygame.draw.line(self.window, (255, 0, 0), rect.center, p, 4)

    self.window.blit(self.img_rot, rect)
  

  def draw_bars(self):
    ramka(self.window, self.bar.width * self.hp / self.full_hp, self.bar.height, 10, (255, 0, 0), (255, 0, 0), self.bar.topleft)
    self.window.blit(ramka(None, self.bar.width, self.bar.height, 10, (0, 0, 0), (0, 0, 255), lw=5), self.bar)
    
    if self.weapon.get('reload delay'):
      rect = self.rect.move(-self.camera.rect.x, -self.camera.rect.y)
      pos = rect.centerx - 50, rect.centery - rect.height - 40
      progress = 100 * (1 - float(self.weapon['reload delay']) / self.weapon['reload delay set'])

      self.window.blit(ramka(None, progress, self.bar.height, 10, (0, 255, 0), (0, 255, 0), alpha=150), pos)
      self.window.blit(ramka(None, 100, self.bar.height, 10, (0, 0, 0), (0, 0, 255), lw=5, alpha=150), pos)
