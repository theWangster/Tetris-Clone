import pygame
import numpy as np
import copy
from block import Block
import random
from settings import *  # NOQA

__author__ = "Yang Wang"

"""
June 13, 2023
Tetris game
"""

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption(CAPTION)
SCREEN.fill(BLACK)
pygame.display.flip()

block_color = {
    0: BLACK,
    1: CYAN,
    2: YELLOW,
    3: GREEN,
    4: RED,
    5: ORANGE,
    6: BLUE,
    7: PURPLE
}

move_block_down = pygame.USEREVENT + 1
move_horizontally = pygame.USEREVENT + 2
move_rotate = pygame.USEREVENT + 3
move_hard_drop = pygame.USEREVENT + 4


# gets next random block based on https://tetris.fandom.com/wiki/Random_Generator
# decided agaisnt function due to constant changing of variables
def get_next_block(avaliable_blocks):
    if len(avaliable_blocks) <= 4:
        shuffled_blocks = [0, 1, 2, 3, 4, 5, 6]
        random.shuffle(shuffled_blocks)
        avaliable_blocks += shuffled_blocks

    next_block = Block(avaliable_blocks.pop(0))
    return next_block, avaliable_blocks


def place_block(block, board, avaliable_blocks):
    right, left, top, bottom, r_pos, c_pos = block.get_boundaries()
    for r in range(top, bottom + 1):
        for c in range(left, right + 1):
            if board[r][c] == 0 and block.hitbox[r - r_pos][c - c_pos]:
                # checks if space is free then adds block
                board[r][c] = block.color
    block, avaliable_blocks = get_next_block(avaliable_blocks)
    return block, board, avaliable_blocks


def draw_screen(board, block, block_shadow):
    SCREEN.fill(BLACK)
    grid_outline = pygame.Rect((BOARD_LEFT_MARGIN - BLOCK_MARGIN_SIZE, BOARD_TOP_MARGIN - BLOCK_MARGIN_SIZE), ((BLOCK_SIZE +
                               BLOCK_MARGIN_SIZE) * BOARD_WIDTH + BLOCK_MARGIN_SIZE, (BLOCK_SIZE + BLOCK_MARGIN_SIZE) * BOARD_HEIGHT + BLOCK_MARGIN_SIZE))
    pygame.draw.rect(SCREEN, GRAY, grid_outline)

    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            cur_pixel = pygame.Rect((BOARD_LEFT_MARGIN + (BLOCK_SIZE + BLOCK_MARGIN_SIZE) * c,
                                    BOARD_TOP_MARGIN + (BLOCK_SIZE + BLOCK_MARGIN_SIZE) * r), (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(SCREEN, block_color.get(board[r][c]), cur_pixel)

    # draws block shadow
    right, left, top, bottom, r_pos, c_pos = block_shadow.get_boundaries()
    for r in range(top, bottom + 1):
        for c in range(left, right + 1):
            if block.hitbox[r - r_pos][c - c_pos]:
                cur_pixel = pygame.Rect((BOARD_LEFT_MARGIN + (BLOCK_SIZE + BLOCK_MARGIN_SIZE) * c,
                                        BOARD_TOP_MARGIN + (BLOCK_SIZE + BLOCK_MARGIN_SIZE) * r), (BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(SCREEN, GREY, cur_pixel)

    # draws actual block
    right, left, top, bottom, r_pos, c_pos = block.get_boundaries()
    for r in range(top, bottom + 1):
        for c in range(left, right + 1):
            if block.hitbox[r - r_pos][c - c_pos]:
                cur_pixel = pygame.Rect((BOARD_LEFT_MARGIN + (BLOCK_SIZE + BLOCK_MARGIN_SIZE) * c,
                                        BOARD_TOP_MARGIN + (BLOCK_SIZE + BLOCK_MARGIN_SIZE) * r), (BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(SCREEN, block_color.get(
                    block.color), cur_pixel)

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))

    # movement timer helpers
    moving = False
    moving_horizontally = False
    hard_dropping = False
    rotating = False
    stopped_counter = 0

    # gets the first block
    avaliable_blocks = [0, 1, 2, 3, 4, 5, 6]
    random.shuffle(avaliable_blocks)
    block = Block(avaliable_blocks.pop(0))

    running = True
    while running:
        clock.tick(60)
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == move_block_down:
                moving = False  # makes sure no more moves until timer done
                if block.move_down(board):
                    stopped_counter = 0  # resets timer if block moves down
                else:
                    stopped_counter += 1  # increments timer when still
                pygame.time.set_timer(move_block_down, 0)
            elif event.type == move_horizontally:
                moving_horizontally = False
            elif event.type == move_rotate:
                rotating = False
            elif event.type == move_hard_drop:
                hard_dropping = False

        # dropping mechanics
        if keys_pressed[pygame.K_SPACE] and not hard_dropping:
            hard_dropping = True
            while True:  # drops block as far down as possible
                if not block.move_down(board):
                    block, board, avaliable_blocks = place_block(
                        block, board, avaliable_blocks)
                    stopped_counter = 0
                    break
            pygame.time.set_timer(move_hard_drop, HARD_DROP_SPEED)
        if keys_pressed[pygame.K_DOWN]:  # drops block fast
            block.move_down(board)

        # movement stuff should probably be in seperate class but ah well
        if not moving_horizontally:
            if keys_pressed[pygame.K_LEFT]:
                block.move_left(board)
                pygame.time.set_timer(move_horizontally, MOVEMENT_SPEED)
                moving_horizontally = True
            elif keys_pressed[pygame.K_RIGHT]:
                block.move_right(board)
                pygame.time.set_timer(move_horizontally, MOVEMENT_SPEED)
                moving_horizontally = True
        if not rotating:
            if keys_pressed[pygame.K_UP]:
                block.rot_right(board)
                pygame.time.set_timer(move_rotate, ROTATION_SPEED)
                rotating = True
            elif keys_pressed[pygame.K_x]:
                block.rot_right(board)
                pygame.time.set_timer(move_rotate, ROTATION_SPEED)
                rotating = True
            elif keys_pressed[pygame.K_z]:
                block.rot_left(board)
                pygame.time.set_timer(move_rotate, ROTATION_SPEED)
                rotating = True

        # Block gets placed after certain time
        if stopped_counter >= TIME_FOR_STOP:
            block, board, avaliable_blocks = place_block(
                block, board, avaliable_blocks)
            stopped_counter = 0

        # draws block shadow
        block_shadow = copy.deepcopy(block)
        while True:
            if not block_shadow.move_down(board):
                break

        log_board(board, block)  # temp for debugging
        print(avaliable_blocks)
        draw_screen(board, block, block_shadow)
        if not moving:
            pygame.time.set_timer(move_block_down, BLOCK_MOVE_SPEED)
            moving = True
    pygame.quit()


# for debugging
def log_board(board, block):
    right, left, top, bottom, pos_r, pos_c = block.get_boundaries()

    printed_board = '-' * 30 + '\n'
    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            if left <= c <= right and top <= r <= bottom and block.hitbox[r - pos_r][c - pos_c]:
                printed_board += '[*]'  # checks for block pixels
            elif board[r][c] == 0:
                printed_board += '[ ]'  # blank space
            else:
                printed_board += '[*]'  # already occupied space
        printed_board += '\n'
    print(printed_board)


# makes sure code was directly run
if __name__ == "__main__":
    main()
