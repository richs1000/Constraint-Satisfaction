__author__ = 'rsimpson'

import random

# size of the board (NxN)
GRIDSIZE = 8

# Represent a board as an array where the index is the column and the value is the row
board = []

def initBoard():
    global board
    board = []
    for col in range(0, GRIDSIZE):
        row = random.randint(0, GRIDSIZE-1)
        board.append(row)


def get_h_cost(board):
    h = 0
    for col1 in range(len(board)):
        #Check every column we haven't already checked
        for col2 in range(col1 + 1, len(board)):
            #Queens are in the same row
            if board[col1] == board[col2]:
                h += 1
            #Get the difference between the current column
            #and the check column
            offset = col2 - col1
            #To be a diagonal, the check column value has to be
            #equal to the current column value +/- the offset
            if (board[col1] == board[col2] - offset) or (board[col1] == board[col2] + offset):
                h += 1
    return h


def make_move_steepest_hill(board):
    moves = {}
    for col in range(len(board)):
        best_move = board[col]

        for row in range(len(board)):
            if board[col] == row:
                #We don't need to evaluate the current
                #position, we already know the h-value
                continue

            board_copy = list(board)
            #Move the queen to the new row
            board_copy[col] = row
            moves[(col,row)] = get_h_cost(board_copy)

    best_moves = []
    h_to_beat = get_h_cost(board)
    for k,v in moves.iteritems():
        if v < h_to_beat:
            h_to_beat = v

    for k,v in moves.iteritems():
        if v == h_to_beat:
            best_moves.append(k)

    #Pick a random best move
    if len(best_moves) > 0:
        pick = random.randint(0,len(best_moves) - 1)
        col = best_moves[pick][0]
        row = best_moves[pick][1]
        board[col] = row

    return board


for i in range(0, 10):
    initBoard()
    print board
    print "h = " + str(get_h_cost(board))