import pygame as pg, pygame
import globals as g
import os
import time
import threading as t

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
    quit = []
    save = []
    info = []
    pass

#initialization function
def init():
    global board
    pygame.init()
    g.disp = pygame.display.set_mode(g.size) #, flags=g.window_flags"""
    g.clock = pygame.time.Clock()
    loadimages()
    calc_centers(board)
    calc_positions()


def render(board, bigscope, smallscope):
    g.disp.fill(g.colors.bgColor)
    for i in range(9):
        if i == bigscope:
            renderAtCenter(images.square, g.pos[i][smallscope])
        else:
            for e in range(9):
                renderAtCenter(images.square, g.pos[i][e])

        for j in range(9):
            if board[i][j] == "X":
                renderAtCenter(images.x, g.pos[i][j])
            elif board[i][j] == "O":
                renderAtCenter(images.o, g.pos[i][j])
            else:
                pass
    renderAtCenter(images.bigboard, (g.centers[4][0] + g.biggrid_render_offset[0], g.centers[4][1] + g.biggrid_render_offset[1]))
    rect = images.bigboard.get_rect()
    pygame.display.update(rect)


def loadimages():
    images.bigboard = pg.transform.scale(pg.image.load("resources/v2/bigBoard.png").convert_alpha(), g.boardsize)
    images.smallboard = pg.transform.scale(pg.image.load("resources/v2/smallGrid.png").convert_alpha(),g.smallsize)
    images.square = pg.transform.scale(pg.image.load("resources/v2/Square.png").convert_alpha(),g.squaresize)
    images.x = pg.transform.scale(pg.image.load("resources/v2/X.png").convert_alpha(),g.x_o_size)
    images.o = pg.transform.scale(pg.image.load("resources/v2/O.png").convert_alpha(),g.x_o_size)

    for i in range(3):
        quit = pg.transform.scale(pg.image.load("resources/v2/Square.png").convert_alpha(), g.button_size)
        save = pg.transform.scale(pg.image.load("resources/v2/Square.png").convert_alpha(), g.button_size)
        info = pg.transform.scale(pg.image.load("resources/v2/Square.png").convert_alpha(), g.button_size)

        images.quit.append(quit)
        images.save.append(save)
        images.info.append(info)

#part of calc_positions function
def row_pos(currState, jay, kay, aai):
    print(currState[(3 * jay)], end=" | ")
    print(currState[(3 * jay) + 1], end=" | ")
    print(currState[(3 * jay) + 2], end="")
    #print(aai, jay,kay,end="")

    if kay != 2:
        print("   I   ", end="") #mid divider


def calc_centers(currState):
    for i in range(9):
        yIndex = i // 3
        y = (yIndex + 0.5) * g.smallsize[1]
        y += g.board_center_offset[1]

        xIndex = i % 3
        x = (xIndex + 0.5) * g.smallsize[0]
        x += g.board_center_offset[0]

        g.centers[i] = (int(x),int(y))

    g.button_coord = {"quit" : (g.centers[0][0], g.button_y), "save" : (g.centers[1][0], g.button_y), "info" : (g.centers[2][0], g.button_y)}

# 1-3,
def calc_positions():
    c = 0 # counter for the grid we are on right now
    size = g.square[0] #it has to be square aspect ratio
    for center in g.centers:
        for i in range(-1, 2):
            for j in range(-1, 2):
                #j represents column, while i represents row
                #x position depends on column(j), y position on row(i)
                y = center[1] + (i * g.square[1])
                x = center[0] + (j * g.square[0])
                g.pos[c].append((x,y))

        c += 1


def renderAtCenter(img, coord):
    rect = img.get_rect()
    rect.center=coord
    g.disp.blit(img,rect)

    return rect


def generate_sample():
    global board
    render(board, 3, 4)

