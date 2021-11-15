import pygame
from pygame import key
import numpy as np
from pygame import draw
import pygame.gfxdraw
import sys
pygame.font.init()

FPS = 60
KEY_DELAY = 10

WIDTH, HEIGHT = 470, 470
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SQUARE_LENGTH = 150
WALL_LENGTH = 10
pygame.display.set_caption("Tic-Tac-Toe")

H_WALL_1 = pygame.Rect(0, (HEIGHT-20)/3, WIDTH, WALL_LENGTH)
H_WALL_2 = pygame.Rect(0, ((HEIGHT-20)/3)*2+WALL_LENGTH, WIDTH, WALL_LENGTH)
V_WALL_1 = pygame.Rect((WIDTH-20)/3, 0, WALL_LENGTH, HEIGHT)
V_WALL_2 = pygame.Rect(((WIDTH-20)/3)*2+WALL_LENGTH, 0, WALL_LENGTH, HEIGHT)

WINNER_FONT = pygame.font.SysFont('comicsans', 150)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

def cursor_movement(keys_pressed, cursor_loc, board, MAX_MIN):
    key_en = True
    # moving cursor
    if keys_pressed[pygame.K_LEFT] and cursor_loc[1] > 0: #LEFT
        cursor_loc[1] -= 1
        key_en = False
    if keys_pressed[pygame.K_RIGHT] and cursor_loc[1] < 2: #RIGHT
        cursor_loc[1] += 1
        key_en = False
    if keys_pressed[pygame.K_UP] and cursor_loc[0] > 0: #UP
        cursor_loc[0] -= 1
        key_en = False
    if keys_pressed[pygame.K_DOWN] and cursor_loc[0] < 2: #DOWN
        cursor_loc[0] += 1
        key_en = False

    # place marker
    if keys_pressed[pygame.K_SPACE] and MAX_MIN:
        if board[cursor_loc[0], cursor_loc[1]] == 0:
            board[cursor_loc[0], cursor_loc[1]] = 1
            utility, e = goal_test(board)
            if utility != 2:
                draw_finish(board, utility, e)
            key_en = False
            MAX_MIN = False
    if keys_pressed[pygame.K_SPACE] and not MAX_MIN:
        if board[cursor_loc[0], cursor_loc[1]] == 0:
            board[cursor_loc[0], cursor_loc[1]] = 2
            utility, e = goal_test(board)
            if utility != 2:
                draw_finish(board, utility, e)
            key_en = False
            MAX_MIN = True

    return board, cursor_loc, key_en, MAX_MIN

def draw_window(cursor_loc, board, MAX_MIN):

    #draw background
    WIN.fill(WHITE)

    #draw grid
    pygame.draw.rect(WIN, BLACK, H_WALL_1)
    pygame.draw.rect(WIN, BLACK, H_WALL_2)
    pygame.draw.rect(WIN, BLACK, V_WALL_1)
    pygame.draw.rect(WIN, BLACK, V_WALL_2)

    #draw select cursor
    draw_cursor(cursor_loc, MAX_MIN)

    #draw O, X
    draw_board(board)
   
    #check draw
    if 0 not in board:
        draw_winner("DRAW", 1)

    pygame.display.update()

def draw_cursor(loc, MAX_MIN):
    if MAX_MIN:
        C = RED
    else:
        C = BLUE
    pygame.draw.rect(WIN, C, pygame.Rect(
        SQUARE_LENGTH*loc[1]+WALL_LENGTH*loc[1], 
        SQUARE_LENGTH*loc[0]+WALL_LENGTH*loc[0], 
        SQUARE_LENGTH, SQUARE_LENGTH))
    pygame.draw.rect(WIN, WHITE, pygame.Rect(
        SQUARE_LENGTH*loc[1]+WALL_LENGTH*loc[1]+10, 
        SQUARE_LENGTH*loc[0]+WALL_LENGTH*loc[0]+10, 
        SQUARE_LENGTH-20, SQUARE_LENGTH-20))

# MAX - BLUE - CROSS  - 1
# MIN - RED  - CIRCLE - 2
def draw_ox(x, y, ox):
    if ox == 2: # MIN
        x = x+75
        y = y+75
        pygame.gfxdraw.aacircle(WIN, x, y, 55, BLUE)
    elif ox == 1: # MAX
        pygame.gfxdraw.line(WIN, 
        x+10, y+10, 
        x+SQUARE_LENGTH-10, y+SQUARE_LENGTH-10, RED) # draw \
        pygame.gfxdraw.line(WIN, 
        x+SQUARE_LENGTH-10, y+10, 
        x+10, y+SQUARE_LENGTH-10, RED) # draw /


def draw_board(board):
    for i in range(3):
        for j in range(3):
            if board[i, j] != 0:
                draw_ox(SQUARE_LENGTH*j+WALL_LENGTH*j, 
                SQUARE_LENGTH*i+WALL_LENGTH*i, board[i, j])

def goal_test(board):
    goal_list = []
    goal_list.append(board[:, 0])
    goal_list.append(board[:, 1])
    goal_list.append(board[:, 2])
    goal_list.append(board[0, :])
    goal_list.append(board[1, :])
    goal_list.append(board[2, :])
    goal_list.append(np.array([board[0, 0], board[1, 1], board[2, 2]]))
    goal_list.append(np.array([board[0, 2], board[1, 1], board[2, 0]]))

    for e in range(8):
        uq = np.unique(goal_list[e])
        if len(uq) == 1 and uq[0] == 1:
            return 1, e
        elif len(uq) == 1 and uq[0] == 2:
            return -1, e
        elif 0 not in board:
            return 0, e
    
    return 2, e

def draw_finish(board, m, e):
    if m == 1:
        draw_board(board)
        draw_win_line(e)
        draw_winner("MAX WIN", 1)
    elif m == -1:
        draw_board(board)
        draw_win_line(e)
        draw_winner("MIN WIN", 2)
    elif m == 0:
        draw_winner("DRAW", 1)

def draw_winner(text, C):
    if C == 1:
        text_color = RED
    elif C == 2:
        text_color = BLUE

    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit(0)
        
        draw_text = WINNER_FONT.render(text, 1, text_color)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()

# 0, 1, 2: |||
# 3, 4, 5: ---
# 6, 7: \ /
def draw_win_line(e):
    if e == 0:
        x1 = SQUARE_LENGTH/2
        y1 = 0
        x2 = SQUARE_LENGTH/2
        y2 = HEIGHT
    elif e == 1:
        x1 = SQUARE_LENGTH*1.5 + WALL_LENGTH
        y1 = 0
        x2 = SQUARE_LENGTH*1.5 + WALL_LENGTH
        y2 = HEIGHT
    elif e == 2:
        x1 = SQUARE_LENGTH*2.5 + WALL_LENGTH
        y1 = 0
        x2 = SQUARE_LENGTH*2.5 + WALL_LENGTH
        y2 = HEIGHT
    elif e == 3:
        x1 = 0
        y1 = SQUARE_LENGTH/2
        x2 = WIDTH
        y2 = SQUARE_LENGTH/2
    elif e == 4:
        x1 = 0
        y1 = SQUARE_LENGTH*1.5 + WALL_LENGTH
        x2 = WIDTH
        y2 = SQUARE_LENGTH*1.5 + WALL_LENGTH
    elif e == 5:
        x1 = 0
        y1 = SQUARE_LENGTH*2.5 + WALL_LENGTH
        x2 = WIDTH
        y2 = SQUARE_LENGTH*2.5 + WALL_LENGTH
    elif e == 6:
        x1 = 0
        y1 = 0
        x2 = WIDTH
        y2 = HEIGHT
    elif e == 7:
        x1 = WIDTH
        y1 = 0
        x2 = 0
        y2 = HEIGHT
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    pygame.gfxdraw.line(WIN, x1, y1, x2, y2, GREEN)

def alpha_beta_search(board):
    move, a, b = max_value(board, np.NINF, np.Inf, 0)
    print("alpha = {0}, beta = {1}".format(a, b))
    return move

def max_value(board, a, b, depth):
    utility, dummy = goal_test(board)
    if utility != 2:
        return utility

    v = np.NINF

    queue = []
    for r in range(3):
        for c in range(3):
            if board[r, c] != 0:
                continue
            else:
                queue.append([r, c])

    max_move = queue[0]
    for move in queue:
        board_tmp = board.copy()        
        board_tmp[move[0], move[1]] = 1
        min_tmp = min_value(board_tmp, a, b, depth+1)
        if v >= min_tmp:
            v = v
            max_move = max_move
        else:
            v = min_tmp
            max_move = move
        if v >= b:
            return v
        a = max(a, v)

    if depth == 0:
        return max_move, a, b
    else:
        return v

def min_value(board, a, b, depth):
    utility, dummy = goal_test(board)
    if utility != 2:
        return utility
    
    v = np.Inf

    queue = []
    for r in range(3):
        for c in range(3):
            if board[r, c] != 0:
                continue
            else:
                queue.append([r, c])

    for move in queue:
        board_tmp = board.copy()        
        board_tmp[move[0], move[1]] = 2
        v = min(v, max_value(board_tmp, a, b, depth+1))
        if v <= a:
            return v
        b = min(b, v)
    
    return v

def main():
    #initilize board with 3 by 3 zeros
    board = np.zeros((3, 3))

    cursor_loc = [0, 0]

    clock = pygame.time.Clock()
    run = True
    key_en = True
    key_cnt = 0
    MAX_MIN = True # max go first

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #PC's turn
        if MAX_MIN:
            move = alpha_beta_search(board)
            board[move[0], move[1]] = 1
            utility, e = goal_test(board)
            if utility != 2:
                draw_finish(board, utility, e)
            MAX_MIN = False

        #PLAYER's turn
        keys_pressed = pygame.key.get_pressed()
        if key_en:
            board, cursor_loc, key_en, MAX_MIN = cursor_movement(keys_pressed, cursor_loc, board, MAX_MIN)
        else:
            key_cnt+=1
            if key_cnt == KEY_DELAY:
                key_en = True
                key_cnt = 0

        draw_window(cursor_loc, board, MAX_MIN)
    
    pygame.quit()

if __name__ == "__main__":
    main()