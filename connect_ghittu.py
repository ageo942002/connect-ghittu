#!/usr/bin/env python
# coding: utf-8

# In[23]:
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


import pygame
import sys
import numpy as np
#I LOVE YOU MY DOLL
ROWS = 6
COLS = 7
CELL = 100

WIDTH = COLS * CELL
HEIGHT = (ROWS + 1) * CELL

BLUE = (30, 80, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRID = (200, 200, 200)
RED = (255, 50, 50)

FPS = 60
DROP_SPEED = 20

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Ghittu")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 36)
small_font = pygame.font.SysFont("arial", 28)

coin1 = pygame.image.load(resource_path("coin1.jpeg")).convert_alpha()
coin2 = pygame.image.load(resource_path("coin2.jpeg")).convert_alpha()

coin1 = pygame.transform.scale(coin1, (CELL, CELL))
coin2 = pygame.transform.scale(coin2, (CELL, CELL))

def make_circle(img):
    size = img.get_size()
    mask = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.circle(mask, (255,255,255,255),
                       (size[0]//2, size[1]//2),
                       size[0]//2)
    img.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    return img

coin1 = make_circle(coin1)
coin2 = make_circle(coin2)

board = np.zeros((ROWS, COLS))
turn = 1
score1 = 0
score2 = 0

#I MARRY U ONE DAY
def draw_header():
    title = font.render("Connect Ghittu", True, WHITE)
    score = small_font.render(
        f"Player 1: {score1}    Player 2: {score2}", True, WHITE
    )
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))
    screen.blit(score, (WIDTH//2 - score.get_width()//2, 50))

def draw_board():
    screen.fill(BLACK)
    draw_header()

    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(
                screen, BLUE,
                (c*CELL, (r+1)*CELL, CELL, CELL)
            )
            pygame.draw.rect(
                screen, GRID,
                (c*CELL, (r+1)*CELL, CELL, CELL), 2
            )

    for c in range(COLS):
        for r in range(ROWS):
            x = c * CELL
            y = HEIGHT - (r+1) * CELL
            if board[r][c] == 1:
                screen.blit(coin1, (x, y))
            elif board[r][c] == 2:
                screen.blit(coin2, (x, y))

    pygame.display.update()

def get_next_open_row(col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r
    return None
#GHITTU BABYYYYYYY
def animate_drop(col, row, coin_img):
    x = col * CELL
    y = 0
    target_y = HEIGHT - (row+1) * CELL
    while y < target_y:
        draw_board()
        screen.blit(coin_img, (x, y))
        pygame.display.update()
        y += DROP_SPEED
        clock.tick(FPS)

def check_win(piece):
    # Horizontal
    for c in range(COLS-3):
        for r in range(ROWS):
            if all(board[r][c+i] == piece for i in range(4)):
                return [(r, c+i) for i in range(4)]

    # Vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return [(r+i, c) for i in range(4)]

    # Positive diagonal
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return [(r+i, c+i) for i in range(4)]

    # Negative diagonal
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return [(r-i, c+i) for i in range(4)]

    return None

def draw_win_line(win_cells):
    start = win_cells[0]
    end = win_cells[-1]

    start_pos = (
        start[1]*CELL + CELL//2,
        HEIGHT - (start[0]+1)*CELL + CELL//2
    )
    end_pos = (
        end[1]*CELL + CELL//2,
        HEIGHT - (end[0]+1)*CELL + CELL//2
    )

    pygame.draw.line(screen, RED, start_pos, end_pos, 8)
    pygame.display.update()
#SEND CHEKKK
def reset_board():
    global board
    board = np.zeros((ROWS, COLS))

draw_board()
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            col = event.pos[0] // CELL
            if 0 <= col < COLS:
                row = get_next_open_row(col)
                if row is not None:
                    coin = coin1 if turn == 1 else coin2
                    animate_drop(col, row, coin)
                    board[row][col] = turn

                    win = check_win(turn)
                    draw_board()

                    if win:
                        if turn == 1:
                            score1 += 1
                        else:
                            score2 += 1

                        draw_win_line(win)
                        pygame.time.delay(1200)
                        reset_board()

                    turn = 2 if turn == 1 else 1
                    draw_board()


# In[ ]:




