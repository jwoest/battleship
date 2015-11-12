#!/usr/bin/env python3


# imports
import os
import copy
import bship_conf


# Print out the current game board
def print_board(board, turns):
    os.system('clear')

    # print the header row, with the column numbers
    print('\n')
    print('   ', end='')
    for i in range(bship_conf.BOARD_SIZE):
        print(i , end='   ')
    print('\n')

    # print the board, with the row numbers
    # at the start of each row
    for row in range(len(board)):
        print(row, end='  ')
        for col in range(len(board)):
            print(board[row][col], end='   ')
        print('\n')

    # print a legend
    print("""
Hit =     %s
Miss =    %s
No shot = %s
""" % (bship_conf.HIT, bship_conf.MISS, bship_conf.EMPTY))
    # print the number of turns left
    print("Turns left : %d\n" % turns)


# Print the game rules
def print_intro(turns):
    os.system('clear')
    print("""
*** BATTLESHIP ***

Destroy all of the enemy ships by targetting x, y
coordinates.  You've got %d turns to find them all!

Enemy ship      Length
Carrier         5
Battleship      4
Destroyer       3
Submarine       3
Patrol boat     2

Board spaces:
    No shot taken   %s
    Hit             %s
    Miss            %s

Hit <Enter> to start!
""" % (turns,bship_conf.EMPTY, bship_conf.HIT, bship_conf.MISS) )

    input()


# Print board with ship locations.  Make a copy of
# the board, so that the actual play board is not changed.
def print_board_with_ships(board, ship_locations, turns_left):
    copy_of_board = copy.deepcopy(board)
    for ship in ship_locations:
        char = ship[0].upper()
        for (row,col) in ship_locations[ship]:
            copy_of_board[row][col] = char
            print_board(copy_of_board, turns_left)


