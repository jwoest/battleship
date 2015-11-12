#!/usr/bin/env python3

# A program to play a game of battleship against the computer.
#

import random
import copy
import bship_conf
import bship_display


# Return a blank board for a new game
def new_board():
    blank_board = [[bship_conf.EMPTY for x in range(bship_conf.BOARD_SIZE)] for x in range(bship_conf.BOARD_SIZE)]
    return blank_board


# Place the enemy ships on the board
def place_ships():
    locations = {}
    for ship in bship_conf.SHIP_LENGTHS:
        ship_placed = False

        while not ship_placed:
            # Randomly choose horizontal or vertical placement.
            # Select a starting point such that the ship
            # fits on the board, then lay out the points
            # of the ship.
            locations[ship] = []
            if random.randrange(2) == 0:
                # horizontal orientation
                start_row = random.randrange(bship_conf.BOARD_SIZE)
                start_col = random.randrange(bship_conf.BOARD_SIZE - bship_conf.SHIP_LENGTHS[ship] + 1)
                for i in range(bship_conf.SHIP_LENGTHS[ship]):
                    locations[ship].append((start_row, start_col + i))

            else:
                # vertical orientation
                start_row = random.randrange(bship_conf.BOARD_SIZE - bship_conf.SHIP_LENGTHS[ship] + 1)
                start_col = random.randrange(bship_conf.BOARD_SIZE)
                for i in range(bship_conf.SHIP_LENGTHS[ship]):
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
        if board[row][col] != bship_conf.EMPTY:
            print("You've already taken a shot there.\n")
            continue

        # Input checks out
        return(row, col)


# Place the player's shot on the board
def take_shot(board, ship_locations, row, col):
    board[row][col] = bship_conf.MISS
    for ship in ship_locations:
        if (row,col) in ship_locations[ship]:
            # If we've hit a ship, mark the board space and
            # Remove the point from the ship locations list.
            board[row][col] = bship_conf.HIT
            ship_locations[ship].remove((row,col))


# Check to see if there are any spaces left with un-shot
# ships.  Return True if there are.
def are_there_ships_left(ship_locations):
    ships_left = False
    for ship in ship_locations:
        if ship:
            ships_left = True

    return ships_left


