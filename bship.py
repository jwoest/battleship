#!/usr/bin/env python3

# A program to play a game of battleship against the computer.
#

import bship_conf
import bship_display
import bship_logic

### MAIN PROGRAM ###

# How many turns does the player start with?
turns_left = bship_conf.STARTING_TURNS

# set up the game
board = bship_logic.new_board()
ship_locations = bship_logic.place_ships()

# play it
bship_display.print_intro(turns_left)
game_won = False
while turns_left > 0 and game_won == False:
    bship_display.print_board(board, turns_left)
    (row, col) = bship_logic.get_player_input(board)
    bship_logic.take_shot(board, ship_locations, row, col)
    ships_left = bship_logic.are_there_ships_left(ship_locations)
    if ships_left == False:
        game_won = True
    turns_left -= 1

# Game's over - did we win?
if game_won:
    bship_display.print_board(board, turns_left)
    print("Congratulations - you found all of the enemy ships!\n")
else:
    bship_display.print_board_with_ships(board, ship_locations, turns_left)
    print("Sorry - you failed to find all of the enemy ships in time...\n")


