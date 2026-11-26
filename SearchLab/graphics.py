import sys
from functools import lru_cache

import pygame

INK = "#eff5ff"
MUTED = "#b2c5d6"
TEAL = "#75e4c2"
PAPER = "#f3f5f1"
WHITE = "#ffffff"


@lru_cache(maxsize=128)
def rounded(width, height, radius, color):
    large = pygame.Surface((width * 3, height * 3), pygame.SRCALPHA)
    pygame.draw.rect(large, color, large.get_rect(), border_radius=radius * 3)
    return pygame.transform.smoothscale(large, (width, height))


def box(screen, rect, color, radius=12):
    rect = pygame.Rect(rect)
    screen.blit(rounded(rect.width, rect.height, radius, color), rect)


@lru_cache(maxsize=1)
def backdrop():
    canvas = pygame.Surface((880, 656))
    for y in range(656):
        f = y / 655
        pygame.draw.line(canvas, (int(21-11*f), int(35-14*f), int(55-21*f)), (0,y), (879,y))
    for x in range(8,880,20):
        for y in range(8,656,20):
            canvas.set_at((x,y), (44,62,80))
    return canvas


def card(screen, rect, interior, edge):
    bounds = pygame.Rect(rect)
    box(screen,bounds.move(0,4),"#0a1420",15)
    box(screen,bounds,edge,15)
    box(screen,bounds.inflate(-2,-2),interior,14)


def heading(screen,label,title,subtitle):
    points = [(44,44),(63,27),(65,61),(83,45)]
    for a,b in ((0,1),(0,2),(1,3),(2,3)):
        pygame.draw.aaline(screen,TEAL,points[a],points[b])
    for i,(x,y) in enumerate(points):
        box(screen,(x-4,y-4,8,8),TEAL if i%2 else WHITE,4)
    label(title,102,16,32,INK,True)
    label(subtitle,104,61,17,MUTED)


def native_display():
    if sys.platform == "win32":
        import ctypes
        try:
            ctypes.windll.user32.SetProcessDpiAwarenessContext(-4)
        except AttributeError:
            ctypes.windll.user32.SetProcessDPIAware()
    pygame.init()
    return pygame.display.set_mode((880, 656))
