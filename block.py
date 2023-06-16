import numpy as np
from settings import *

__author__ = 'Yang Wang'

"""
Date: June 15, 2023
Usage: Block class
"""

I_BLOCK = np.array([[False, True, False, False],
                    [False, True, False, False],
                    [False, True, False, False],
                    [False, True, False, False]])
O_BLOCK = np.array([[True, True],
                    [True, True]])
S_BLOCK = np.array([[False, True, True],
                    [True, True, False],
                    [False, False, False]])
Z_BLOCK = np.array([[True, True, False],
                    [False, True, True],
                    [False, False, False]])
L_BLOCK = np.array([[True, True, True],
                    [True, False, False],
                    [False, False, False]])
J_BLOCK = np.array([[True, True, True],
                    [False, False, True],
                    [False, False, False]])
T_BLOCK = np.array([[True, True, True],
                    [False, True, False],
                    [False, False, False]])

block_types = {
    0: I_BLOCK,
    1: O_BLOCK,
    2: S_BLOCK,
    3: Z_BLOCK,
    4: L_BLOCK,
    5: J_BLOCK,
    6: T_BLOCK
}


class Block():
    def __init__(self, type):
        self.hitbox = block_types.get(type)
        self.color = type + 1
        self.r = 0
        if type == 1:
            self.c = 4
            self.size = 2
        else:
            self.c = 3

            if type == 0:
                self.size = 4
            else:
                self.size = 3

    def get_right_bound(self):
        for c in range(self.size - 1, -1, -1):
            for r in range(self.size):
                if self.hitbox[r][c]:
                    return c

    def get_left_bound(self):
        for c in range(self.size):
            for r in range(self.size):
                if self.hitbox[r][c]:
                    return c

    def get_bottom_bound(self):
        for r in range(self.size - 1, -1, -1):
            for c in range(self.size):
                if self.hitbox[r][c]:
                    return r

    def get_top_bound(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.hitbox[r][c]:
                    return r

    def get_boundaries(self):
        right = self.get_right_bound() + self.c
        left = self.get_left_bound() + self.c
        top = self.get_top_bound() + self.r
        bottom = self.get_bottom_bound() + self.r
        pos_r = self.r
        pos_c = self.c

        return right, left, top, bottom, pos_r, pos_c

    def is_valid_move(self, board):
        right, left, top, bottom, pos_r, pos_c = self.get_boundaries()

        if right >= BOARD_WIDTH or left < 0 or bottom >= BOARD_HEIGHT or top < 0:
            return False  # Check if out of bounds

        for r in range(top, bottom + 1):
            for c in range(left, right + 1):
                if board[r][c] != 0 and self.hitbox[r - pos_r][c - pos_c]:
                    return False  # Check for collision with board objects

        return True

    def move_down(self, board):
        self.r += 1
        if not self.is_valid_move(board):
            self.r -= 1
            return False  # increments counter in game.py
        return True  # when counter reaches level, block is stopped

    def move_right(self, board):
        self.c += 1
        if not self.is_valid_move(board):
            self.c -= 1

    def move_left(self, board):
        self.c -= 1
        if not self.is_valid_move(board):
            self.c += 1

    def rot_right(self, board):
        self.hitbox = np.rot90(self.hitbox, -1)
        if not self.is_valid_move(board):
            self.hitbox = np.rot90(self.hitbox, 1)

    def rot_left(self, board):
        self.hitbox = np.rot90(self.hitbox, 1)
        if not self.is_valid_move(board):
            self.hitbox = np.rot90(self.hitbox, -1)
