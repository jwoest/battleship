#!/usr/bin/env python3

# A program to play a game of battleship against the computer.
#

import os
import sys
import random
import copy


# CONSTANTS
BOARD_SIZE = 10
EMPTY = '.'
HIT   = 'X'
MISS  = '@'
SHIP_LENGTHS = {"carrier":5, "battleship":4, "destroyer":3, "submarine":3, "patrol_boat":2}
STARTING_TURNS = 40


# Return a blank board for a new game
def new_board():
    blank_board = [[EMPTY for x in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]
    return blank_board


# Place the enemy ships on the board
def place_ships():
    locations = {}
    for ship in SHIP_LENGTHS:
        ship_placed = False

        while not ship_placed:
            # Randomly choose horizontal or vertical placement.
            # Select a starting point such that the ship
            # fits on the board, then lay out the points
            # of the ship.
            locations[ship] = []
            if random.randrange(2) == 0:
                # horizontal orientation
                start_row = random.randrange(BOARD_SIZE)
                start_col = random.randrange(BOARD_SIZE - SHIP_LENGTHS[ship] + 1)
                for i in range(SHIP_LENGTHS[ship]):
                    locations[ship].append((start_row, start_col + i))

            else:
                # vertical orientation
                start_row = random.randrange(BOARD_SIZE - SHIP_LENGTHS[ship] + 1)
                start_col = random.randrange(BOARD_SIZE)
                for i in range(SHIP_LENGTHS[ship]):
                    locations[ship].append((start_row + i, start_col))

            # Check to make sure that the ship does not overlap
            # any ships already placed
            conflict = False
            for s in locations:
                if s == ship:
                # no need to check against ourselves
                    continue
                else:
                    for (row,col) in locations[ship]:
                        if (row,col) in locations[s]:
                            conflict = True
            
            if conflict:
                ship_placed = False
            else:
                ship_placed = True

    return locations


# Print out the current game board
def print_board(board, turns):
    os.system('clear')

    # print the header row, with the column numbers
    print('\n')
    print('   ', end='')
    for i in range(len(board)):
        print(i, end='   ')
    print('\n')

    # print the board, with the row numbers at the start of each row
    for row in range(len(board)):
        print(row, end='  ')
        for col in range(len(board)):
            print(board[row][col], end='   ')
        print('\n')

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
""" % (turns, EMPTY, HIT, MISS) )

    input()


# Get row,col coordinates for the player's next shot
def get_player_input(board):
    while True:
        print("Enter the row and column of your next shot.")
        row = input("  Row #:    ")
        col = input("  Column #: ")

        # Are the inputs numbers?
        try:
            row = int(row)
            col = int(col)
        except:
            print("Numbers only, please.\n")
            continue

        # Are the inputs on the board?
        if row < 0 or row >= len(board) or col < 0 or col >= len(board):
            print("That's not even on the board!\n")
            continue

        # Has the player already shot that space?
        if board[row][col] != EMPTY:
            print("You've already taken a shot there.\n")
            continue

        # Input checks out
        return(row, col)


# Place the player's shot on the board
def take_shot(board, ship_locations, row, col):
    board[row][col] = MISS
    for ship in ship_locations:
        if (row,col) in ship_locations[ship]:
            # If we've hit a ship, mark the board space and
            # Remove the point from the ship locations list.
            board[row][col] = HIT
            ship_locations[ship].remove((row,col))

# Print board with ship locations.  Make a copy of
# the board, so that the actual play board is not changed.
def print_board_with_ships(board, ship_locations, turns_left):
    copy_of_board = copy.deepcopy(board)
    for ship in ship_locations:
        char = ship[0].upper()
        for (row,col) in ship_locations[ship]:
            copy_of_board[row][col] = char
    print_board(copy_of_board, turns_left)


# Check to see if there are any spaces left with un-shot
# ships.  Return True if there are.
def are_there_ships_left(ship_locations):
    ships_left = False
    for ship in ship_locations:
        if ship:
            ships_left = True

    return ships_left


### MAIN PROGRAM ###

# How many turns does the player start with?
turns_left = STARTING_TURNS

# set up the game
board = new_board()
ship_locations = place_ships()

# play it
print_intro(turns_left)
game_won = False
while turns_left > 0 and game_won == False:
    print_board(board, turns_left)
    (row, col) = get_player_input(board)
    take_shot(board, ship_locations, row, col)
    ships_left = are_there_ships_left(ship_locations)
    if ships_left == False:
        game_won = True
    turns_left -= 1

# Game's over - did we win?
if game_won:
    print_board(board, turns_left)
    print("Congratulations - you found all of the enemy ships!\n")
else:
    print_board_with_ships(board, ship_locations, turns_left)
    print("Sorry - you failed to find all of the enemy ships in time...\n")


