import pygame as pg, pygame
import globals as g
import os
import time

#vars
board = [['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_']]
#contaiiner for images
class images:
    pass

#initialization function
def init():
    global board
    pygame.init()
    g.disp = pygame.display.set_mode(g.size)
    g.clock = pygame.time.Clock()
    loadimages()


def render(board, bigscope, smallscope):
    pass

def loadimages():
    images.bigboard = pg.transform.scale(pg.image.load("resources/bigboard.png").convert_alpha(), g.boardsize)
    images.smallboard = pg.transform.scale(pg.image.load("resources/smallboard.png").convert_alpha(),g.smallsize)
    images.square = pg.transform.scale(pg.image.load("resources/square.png").convert_alpha(),g.squaresize)
    images.x = pg.transform.scale(pg.image.load("resources/x.png").convert_alpha(),g.x_o_size)
    images.o = pg.transform.scale(pg.image.load("resources/o.png").convert_alpha(),g.x_o_size)

#part of calc_positions function
def row_pos(currState, jay, kay, aai):
    print(currState[(3 * jay)], end=" | ")
    print(currState[(3 * jay) + 1], end=" | ")
    print(currState[(3 * jay) + 2], end="")
    print(aai, jay,kay,end="")

    #g.pos[(3 * jay)] =

    if kay != 2:
        print("   I   ", end="") #mid divider



def calc_centers(currState):
    #os.system("cls")
    for i in range(3):
        for j in range(3):
            for k in range(3):
                row_pos(currState[(3 * i) + k], j, k, i)

                g.centers[(3*i) + k] = (int(g.smallsize[0]*(k + 0.5) + g.board_center_offset[0]), int(g.smallsize[1]*(i+0.5) + g.board_center_offset[1]))

            print("\n")
        if (i != 2):
            for a in range(44):
                print("_", end="")
        print("\n")

def calc_positions():
    c = 0
    size = g.squaresize[0] #it has to be square aspect ratio
    for center in g.centers:
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = center[0] + (size * i)
                y = center[1] + (size * j)
                g.pos[c].append((x,y))

        c += 1

def sample_show():
    g.disp.fill(g.colors.bgColor)
    g.disp.blit(images.bigboard, g.board_center_offset)
    for each in g.pos:
        for pos in each:
            renderAtCenter(images.x, pos)

    pygame.display.update()

def renderAtCenter(img, coord):
    rect=img.get_rect()
    rect.center=coord
    g.disp.blit(img,rect)


init()
calc_centers(board)
calc_positions()
sample_show()

while 1:
    for event in pygame.event.get():
        pass

print(g.centers)