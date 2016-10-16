import pygame, geom
from pygame.locals import *



ru = lambda x: str(x).decode("u8")


def min_max(*lst):
    lst = lst[0] if len(lst) == 1 else lst
    return min(lst), max(lst)


def ramka(surf, w, h, r, clr1, clr2=0, pos=(0, 0), lw=2, alpha=255):
    new = False if surf else True
    x, y = pos
    if not surf:
        bg = clr1[0] // 2, clr1[1] // 2, clr1[2] // 2
        surf = pygame.Surface((w, h))
        surf.fill(bg)

    for cx, cy in ((x + r, y + r), (x + w - r, y + r), (x + w - r, y + h - r),
                   (x + r, y + h - r)):
        pygame.draw.circle(surf, clr1, (int(cx), int(cy)), r)
        pygame.draw.circle(surf, clr2, (int(cx), int(cy)), r, lw)

    pygame.draw.rect(surf, clr1, (x, y + r, w, h - 2 * r))
    pygame.draw.rect(surf, clr1, (x + r, y, w - 2 * r, h))
    for p1, p2 in ([(x, y + r), (x, y + h - r)], [(x + r, y), (x + w - r, y)],
                   [(x + w - 2, y + r), (x + w - 2, y + h - r)],
                   [(x + r, y + h - 2), (x + w - r, y + h - 2)]):
        pygame.draw.line(surf, clr2, p1, p2, lw)

    if new:
        surf.set_colorkey(bg)
        surf.set_alpha(alpha)
        return surf.convert_alpha()