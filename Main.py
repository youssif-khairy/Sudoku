import sys
import pygame as pg
import numpy as np


class Dimension(object):
    def __init__(self,r,c):
        self.row = r
        self.col = c


class Cell(object):

    def __init__(self,scren,x,y,w,h,is_changable,txt=''):
        font = pg.font.Font(None, 32)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.txt = txt
        self.rect = pg.Rect(x, y, w, h)
        self.actve = False
        self.scren = scren
        self.clr = (120, 120, 120)
        self.is_changable = is_changable
        text_layer = font.render(self.txt, True, (255, 0, 0))
        scren.blit(text_layer, ((self.rect.x + 22), (self.rect.y + 22)))
        pg.draw.rect(scren,self.clr,self.rect,2)
        pg.display.update()

    def handle_event(self,event):
        handled = False
        font = pg.font.Font(None, 32)
        white = (255, 255, 255)
        clr1 = (120, 120, 120)
        clr2 = (60, 60, 60)

        if self.is_changable:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.actve = not self.actve
                else:
                    self.actve = False

                if self.actve:
                    self.clr = clr2
                else:
                    self.clr = clr1
                pg.draw.rect(self.scren, self.clr, self.rect, 2)  # 2 = border
                pg.display.flip()
            if event.type == pg.KEYDOWN:
                if self.actve:
                    if event.key == pg.K_RETURN:
                        self.actve = False
                        self.clr = clr1
                        pg.draw.rect(self.scren, self.clr, self.rect,2)
                        pg.display.flip()
                    elif event.key == pg.K_BACKSPACE:
                        self.txt = ''
                        pg.draw.rect(self.scren, white, self.rect)
                        pg.display.flip()
                    else:
                        pg.draw.rect(self.scren, white, self.rect)
                        pg.display.flip()
                        self.txt = event.unicode
                        if not self.txt.isdigit() or self.txt == "0":
                            self.txt = ""
                        else:
                            handled = True
                if self.is_changable:
                    text_layer = font.render(self.txt, True, (0,0,0))
                else:
                    text_layer = font.render(self.txt, True, (255, 0, 0))
                self.scren.blit(text_layer, ((self.rect.x +22), (self.rect.y +22)))
                pg.draw.rect(self.scren, self.clr, self.rect, 2)  # 2 = border
                pg.display.flip()
        return handled

    def reform_cell(self,txt,is_changable):
        #clear
        font = pg.font.Font(None, 32)
        white = (255, 255, 255)
        self.txt = ''
        pg.draw.rect(self.scren, white, self.rect)
        pg.display.flip()
        #append new
        if is_changable:
            text_layer = font.render(txt, True, (0, 0, 0))
        else:
            text_layer = font.render(txt, True, (255, 0, 0))
        self.scren.blit(text_layer, ((self.rect.x + 22), (self.rect.y + 22)))
        pg.draw.rect(self.scren, self.clr, self.rect, 2)  # 2 = border
        pg.display.flip()

    def delet_movement(self):
        white = (255,255,255)
        pg.draw.rect(self.scren, white, self.rect)
        pg.display.flip()


board = [[0,3,8,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,2,0],
         [5,1,9,0,0,0,0,4,0],
         [0,2,0,7,0,0,0,0,0],
         [0,0,0,0,9,8,6,0,0],
         [8,5,3,0,0,0,0,0,0],
         [0,9,0,1,2,0,5,0,0],
         [4,0,0,0,0,0,1,0,0],
         [0,0,0,4,0,0,7,0,0]]


board = [[5,1,7,6,0,0,0,3,4],
         [2,8,9,0,0,4,0,0,0],
         [3,4,6,2,0,5,0,9,0],
         [6,0,2,0,0,0,0,1,0],
         [0,3,8,0,0,6,0,4,7],
         [0,0,0,0,0,0,0,0,0],
         [0,9,0,0,0,0,0,7,8],
         [7,0,3,4,0,0,5,6,0],
         [0,0,0,0,0,0,0,0,0]]


def is_solved(boarD):
    for i in range(9):
        if 0 in boarD[i]:
            return False
    return True


def pickNormal(boarD):
    for i in range(9):
        for j in range(9):
            if boarD[i][j] == 0:
                return Dimension(i,j)


def pickCell(boarD):
    temp_row = 0
    best_row_count = 10
    temp_col = 0
    bes_col_count = 10
    for i in range(9):
        for j in range(9):
            if boarD[i][j] == 0:
                temp_row+=1
            if boarD[j][i] == 0:
                temp_col+=1
        if best_row_count > temp_row:
            # and 0 in boarD[i]:
            best_row_count = temp_row
            best_row = i
        if bes_col_count > temp_col:
            #and 0 in [row[i] for row in boarD]:
            bes_col_count = temp_col
            best_col = i
        temp_row = temp_col = 0

    if boarD[best_row][best_col] == 0:
        return Dimension(best_row,best_col)
    else:
        if best_row_count<=bes_col_count:
            for x in range(9):
                if boarD[best_row][x] == 0:
                    return Dimension(best_row,x)
                else:
                    return pickNormal(boarD)
        else:
            for x in range(9):
                if boarD[x][best_col] == 0:
                    return Dimension(x,best_col)
                else:
                    return pickNormal(boarD)

    """
    temp_row = temp_col = 0
    best_row_count = best_col_count = 9
    #best row then best col for it
    for i in range(9):
        for j in range(9):
            if boarD[i][j] != 0:
                temp_row+=1

        if best_row_count > temp_row:
            best_row_count = temp_row
            best_row = i
        temp_row = 0
    for col in range(9):
        if boarD[best_row][col] != 0:
            for row in range(9):
                if boarD[row][col] != 0:
                    temp_col+=1
        if best_col_count > temp_col:
            best_col = i
        temp_col = 0

    #best col then best row for it
    best_row_count2 = best_col_count2 = 9
    temp_row = temp_col = 0

    for i in range(9):
        for j in range(9):
            if boarD[j][i] != 0:
                temp_col += 1

        if best_col_count2 > temp_col:
            best_col_count2 = temp_col
            best_col2 = i
        temp_col = 0
    for r in range(9):
        if boarD[r][best_col2] != 0:
            for c in range(9):
                if boarD[r][c] != 0:
                    temp_row += 1
        if best_row_count2 > temp_row:
            best_row2 = i
        temp_row = 0
    if best_col_count+best_row_count <= best_col_count2+best_row_count2:
        return Dimension(best_row, best_col)
    return Dimension(best_row2, best_col2)
    """


def is_Valid(boarDy,x,y,val):

    #row and col validation
    for k in range(9):
        if boarDy[k][y] == val:
            return False
        if boarDy[x][k] == val:
            return False

    #block validation
    # first cell in block
    Rx = abs(x - (x%3))
    Ry = abs(y - (y%3))
    for k in range(9):
        if boarDy[Rx][Ry] == val:
            return False
        if (k + 1) % 3 == 0:
            Rx += 1
            Ry -= 2
        else:
            Ry+=1
    return True


def solve(boarD):
    if is_solved(boarD):
        return True
    d = pickCell(boarD)
    for i in range(1,10):
        if is_Valid(boarD, d.row, d.col, i):
            boarD[d.row][d.col] = i
            if solve(boarD):
                return True
            boarD[d.row][d.col] = 0
    return False


def init_grid():

    cnst = 3
    x = 54
    y = 54
    arr = []
    for i in range(9):
        for j in range(9):
            if board[j][i]!=0:
                arr.append(Cell(screen, 54 * i + i + cnst, 54 * j + j + cnst, 54, 54,False,str(board[j][i])))
            else:
                arr.append(Cell(screen, 54 * i + i + cnst, 54 * j + j + cnst, 54, 54,True))
    pg.display.update()
    return arr


def converter(boarD): # from cell DT to 2d array
    myArr = [[0] * 9 for f in range(9)]
    for i in range(9):
        for j in range(9):
            if boarD[j][i].txt == '':
                myArr[i][j] = 0
            else:
                myArr[i][j] = int(boarD[j][i].txt)

    return myArr


def print_solved():
    green = (0,255,0)
    blue = (0,0,255)
    display_surface = pg.display.set_mode((500, 500))
    font = pg.font.Font('freesansbold.ttf', 32)

    # create a text suface object,
    # on which text is drawn on it.
    text = font.render(' -----------------Solved----------------- ', True, green, blue)

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    pg.center = (500 // 2, 500 // 2)
    display_surface.blit(text,textRect)
    pg.display.update()


def init_pygame():

    pg.init()

    width, height = 500, 500

    global screen
    screen = pg.display.set_mode((width, height))

    screen.fill((255, 255, 255))
    pg.display.set_caption('Soduko game')
    pg.display.flip()


def first_option():
    arr = init_grid()
    grid = np.reshape(arr, (-1, 9))
    ex = False
    solve(board)
    while not ex:

        O = converter(grid)
        if board == O:
            screen = pg.display.set_mode((500, 500))
            screen.fill((255, 255, 255))
            print_solved()
            pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ex = True

            for l in range(9):
                for m in range(9):
                    grid[l][m].handle_event(event)


def second_option_grid_init():
    cnst = 3
    x = 44
    y = 44
    arr = []
    for i in range(9):
        for j in range(9):
            arr.append(Cell(screen, x * i + i + cnst, y * j + j + cnst, x, y, True))
    pg.display.update()
    return arr


def reshape_grid_after_solve(grid,solvedGrid):
    for p in range(9):
        for t in range(9):
            if grid[p, t].txt == '':
                grid[p,t].reform_cell(str(solvedGrid[t,p]),True)
            else:
                grid[p,t].reform_cell(str(solvedGrid[t,p]),False)


def second_option():
    x =420
    #y= 50
    arr = second_option_grid_init()
    grid = np.reshape(arr, (-1, 9))
    font = pg.font.Font(None, 32)

    #solve
    y=150
    rect1 = pg.Rect(x, y, 70, 70)
    clr = (0, 225, 0)
    text_layer = font.render("Solve", True, (200, 200, 0))
    screen.blit(text_layer, ((x + 6), (y + 26)))
    pg.draw.rect(screen, clr, rect1, 1)
    pg.display.update()


    ex = False
    while not ex:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                ex = True
        for p in range(9):
            for t in range(9):
                grid[p,t].handle_event(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            if rect1.collidepoint(event.pos):#solve
                myArr = converter(grid)
                solve(myArr)
                reshape_grid_after_solve(grid,np.reshape(myArr, (-1, 9)))


def clear_screen():
    screen = pg.display.set_mode((500, 500))
    screen.fill((255, 255, 255))
    pg.display.flip()


def init_gui():
    #play
    font = pg.font.Font(None, 32)
    rect = pg.Rect(150, 110, 180, 70)
    clr = (0, 225, 0)
    text_layer = font.render("Play sudoku", True, (200, 200, 0))
    screen.blit(text_layer, ((150 + 22), (110 + 22)))
    pg.draw.rect(screen, clr, rect,1)

    #solve
    rect1 = pg.Rect(150, 235, 180, 70)
    text_layer = font.render("solve sudoku", True, (200, 200, 0))
    screen.blit(text_layer, ((150 + 22), (235 + 22)))
    pg.draw.rect(screen, clr, rect1, 1)
    pg.display.update()

    ex = False
    play = False
    solv = False
    while not ex:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                ex = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):#play
                play = True
                break
            if rect1.collidepoint(event.pos):#solve
                solv = True
                break
    #clear screen
    clear_screen()
    if play:
        first_option()
    if solv:
        second_option()


def sudoku():
    init_pygame()
    init_gui()


sudoku()




