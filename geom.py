# -*- coding: utf-8 -*-

from math import *



def convert(a):
  a = a % 360
  return a + 360 if a < 0 else a


def m_vektor(p1, p2):
  m = (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2
  return m ** 0.5


def mv(v):
  return (v[0] ** 2 + v[1] ** 2) ** 0.5


def c_vektor(p1, p2):
  x = p1[0] + (p2[0] - p1[0]) / 2
  y = p1[1] + (p2[1] - p1[1]) / 2
  return x, y


def ln_vektor(p1, p2, ln):
  k = ln / m_vektor(p1, p2)
  return (p2[0] - p1[0]) * k, (p2[1] - p1[1]) * k


def sum_v_in_point(x1, y1, x2, y2):
  return x2 + (x1 - x2) / 2, y2 + (y1 - y2) / 2


def c_okr(r, a=360):
  return pi * r / 180 * a


def s_okr(r, a=360):
  return pi * r ** 2 / 360 * a


def init_lists():
  sin_list = [sct(a, 1) for a in range(361)]
  cos_list = [sct(a, 2) for a in range(361)]
  tan_list = [sct(a, 3) for a in range(361)]
  tan_list[90] = tan_list[270] = None

  return sin_list, cos_list, tan_list


def sct(a, typ=1):
  rad = radians(a)

  if typ == 1:
    return 0 if a % 180 == 0 else sin(rad)
  elif typ == 2:
    return 0 if a in (90, 270) else cos(rad)
  elif typ == 3:
    return 0 if a % 180 == 0 else tan(rad)
  elif typ == 4:
    return None if a % 180 == 0 else 1 / tan(rad)


def asct(x, typ=1):
  sct_list = [sin_list, cos_list, tan_list][typ - 1]

  if x in sct_list:
    a = sct_list.index(x)
    return 360 - a if a > 180 else a

  for a in range(360):
    if sct_list[a] < x < sct_list[a + 1]:
      return 360 - a if a > 180 else a


def gip(a, b, c=None):
  if not c:
     return (a ** 2 + b ** 2) ** 0.5

  if not a:
     return (c ** 2 - b ** 2) ** 0.5

  if not b:
    return (c ** 2 - a ** 2) ** 0.5


def v_to_func_from_x(v, x):
  return x * v[1] / v[0]


def v_to_func_from_y(v, y):
  return y * v[0] / v[1]


def move(angle, ln, pos=(0, 0)):
  x, y = ln * sct(angle, 2), -ln * sct(angle)
  return [x + pos[0], y + pos[1]]


def angle_to_point(pos1, pos2):
  x1, y1 = pos1
  x2, y2 = pos2
  ln = m_vektor(pos1, pos2)
  sin = abs(y2 - y1) / ln
  a = asct(sin)

  if y1 < y2 :
    a = -a

  if x1 > x2 :
    a = 180 - a

  return convert(a)


def get_func(p1, p2, type=1):
  angle = angle_to_point(p1, p2)
  return get_func_a(p1, angle, type)


def get_func_a(pos, angle, type=1):
  a = -sct(angle, 3)

  if angle in (90, 270):
    if type == 2:
      return lambda x:  pos[0]
    else:
      return None
  elif angle in (0, 180):
    if type == 1:
      return lambda x: pos[1]
    else:
      return None

  b = pos[1] - pos[0] * a

  if type == 1:
    return lambda x: (a * x + b if x is not None else (a, b))
  elif type == 2:
    return lambda y: (float(y) - b) / a
  else:
    return a, b


def point_in_lines(p1, p2, p3, p4):
  if p1[0] == p2[0]:
    x = p1[0]
    y = get_func(p3, p4)(x)

    return x, y
  elif p3[0] == p4[0]:
    x = p3[0]
    y = get_func(p1, p2)(x)

    return x, y
  else:
    a1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b1 = p1[1] - a1 * p1[0]
    a2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
    b2 = p3[1] - a2 * p3[0]

    if a1 == a2:
      return None

    x = (b2 - b1) / (a1 - a2)
    y = a1 * x + b1

    return x, y


def point_in_lines_f(funcx1, funcy1, funcx2, funcy2, interval=None):
  if not funcx1 and not funcx2 or not funcy1 and not funcy2:
    return None
  elif not funcx2:
    y = funcx1(funcy2(0))

    if interval and interval[0] <= y <= interval[1] or not interval:
      return y
    else:
      return None
  elif not funcy2:
    y = funcx2(0)

    if funcx1:
      a, b = funcx1(None)
      x = (y - b) / a
    else:
      x = funcy1(0)
  elif not funcx1:
    x = funcy1(0)
  elif not funcy1:
    y = funcx1(0)
    a, b = funcx2(None)
    x = (y - b) / a
  else:
    a1, b1 = funcx1(None)
    a2, b2 = funcx2(None)

    if a1 == a2:
      return None

    x = (b2 - b1) / (a1 - a2)

  if interval and interval[0] <= x <= interval[1] or not interval:
    return x


def circle_collide_line(center, r, funcx, funcy, interval=None):
  x0, y0 = center

  if not funcx:
    x = funcy(0)

    if x0 - r <= x <= x0 + r:
      d = r ** 2 - (x - x0) ** 2
      if d:
          return [y for y in (y0 + d, y0 - d) if not interval or interval[0] <= y <= interval[1]]
      elif not interval or interval[0] <= y0 <= interval[1]:
        return (y0,)

    return False

  elif not funcy:
    y = funcx(0)

    if y0 - r <= y <= y0 + r:
      d = r ** 2 - (y - y0) ** 2

      if d:
        return [x for x in (x0 + d, x0 - d) if not interval or interval[0] <= x <= interval[1]]
      elif not interval or interval[0] <= x0 <= interval[1]:
        return (x0,)

    return False

  a, b = funcx(None)
  aa = 1 + a ** 2
  bb = 2 * (a * b - a * y0 - x0)
  c = x0 ** 2 + (b - y0) ** 2 - r ** 2
  d = bb ** 2 - 4 * aa * c

  if d == 0:
    x1 = -bb / (2 * aa)

    if not interval or interval[0] <= x1 <= interval[1]:
      return (x1,)
  elif d > 0:
    x1, x2 = (-bb + d ** 0.5) / (2 * aa), (-bb - d ** 0.5) / (2 * aa)
    return [x for x in (x1, x2) if not interval or interval[0] <= x <= interval[1]]
  return False

# an = 2Rsin(180/n)
# r = Rcos(180/n)
# a = 2Rsin(pi/n) = 2rtg(pi/n)
sin_list, cos_list, tan_list = init_lists()
