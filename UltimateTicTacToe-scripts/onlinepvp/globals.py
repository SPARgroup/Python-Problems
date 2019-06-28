disp = None
clock = None
FPS = 60
size = (1200, 1200) #window size
title = "Ultimate TicTacToe Multiplayer v3.0"

boardsize = (600, 600)
smallsize = (boardsize[0]//3, boardsize[1]//3)
x_o_size = (smallsize[0]//3, smallsize[1]//3)
squaresize = x_o_size

pos = [[],[],[],[],[],[],[],[],[]]
centers = [(0,0)] * 9

board_center_offset = (0,0)