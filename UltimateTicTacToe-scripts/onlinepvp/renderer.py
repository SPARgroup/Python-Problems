import pygame as pg, pygame
import globals as g


def init():
    pygame.init()
    g.disp = pygame.display.set_mode(g.size)
    g.clock = pygame.time.clock(g.FPS)

def render(board):
    pass