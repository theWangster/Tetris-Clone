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
font = pygame.font.Font('freesansbold.ttf', 18)

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
move_switching = pygame.USEREVENT + 5
game_over = pygame.USEREVENT + 7


def get_next_block(avaliable_blocks):
    """
    Gets next random block based on https://tetris.fandom.com/wiki/Random_Generator
    """

    if len(avaliable_blocks) <= 5:
        shuffled_blocks = [0, 1, 2, 3, 4, 5, 6]
        random.shuffle(shuffled_blocks)
        avaliable_blocks += shuffled_blocks

    next_block = Block(avaliable_blocks.pop(0))
    return next_block, avaliable_blocks


def place_block(block, board, avaliable_blocks, score, level):
    """
    Places the block on the board. Updates board, gets new block and positions it
    """

    right, left, top, bottom, r_pos, c_pos = block.get_boundaries()
    for r in range(top, bottom + 1):
        for c in range(left, right + 1):
            if board[r][c] == 0 and block.hitbox[r - r_pos][c - c_pos]:
                # checks if space is free then adds block
                board[r][c] = block.color
    board, score, lines = clear_rows(board, score, level)
    block, avaliable_blocks = get_next_block(avaliable_blocks)

    if not block.is_valid_move(board):
        pygame.event.post(pygame.event.Event(game_over))

    return block, board, avaliable_blocks, score, lines


def draw_screen(board, block, block_shadow, avaliable_blocks, alt_block, score):
    """
    Draws the screen, including the board, the next 5 blocks,
    the current block, the shadow of the current block, and the held block
    """

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

    # all for formatting, math is irrelevant
    next_block_outline = pygame.Rect(
        NEXT_BLOCK_LEFT, BOARD_TOP_MARGIN - BLOCK_MARGIN_SIZE, NEXT_BLOCK_WIDTH, NEXT_BLOCK_HEIGHT + 2 * BLOCK_MARGIN_SIZE)
    next_block_black = pygame.Rect(NEXT_BLOCK_LEFT + BLOCK_MARGIN_SIZE, BOARD_TOP_MARGIN,
                                   NEXT_BLOCK_WIDTH - 2 * BLOCK_MARGIN_SIZE, NEXT_BLOCK_HEIGHT)
    pygame.draw.rect(SCREEN, GRAY, next_block_outline)
    pygame.draw.rect(SCREEN, BLACK, next_block_black)

    for i in range(5):
        next_block = display_block_types.get(avaliable_blocks[i])
        row = (NEXT_BLOCK_MARGIN + BLOCK_SIZE * 2 +
               BLOCK_MARGIN_SIZE) * i  # move down for every block

        for width in range(4):
            block_offset = 0
            vert_offset = 0
            if avaliable_blocks[i] == 0:
                vert_offset = (BLOCK_SIZE + BLOCK_MARGIN_SIZE) // 2
            if avaliable_blocks[i] == 1:  # if I or O block, ignore offset
                block_offset = 0
            # if any other block, add in offset for aesthetics
            elif avaliable_blocks[i] != 0:
                block_offset = (BLOCK_SIZE + BLOCK_MARGIN_SIZE) // 2

            for height in range(2):
                if next_block[height][width] == 0:  # don't draw blank squares
                    continue
                cur_pixel = pygame.Rect(NEXT_BLOCK_LEFT_POS + (BLOCK_SIZE + BLOCK_MARGIN_SIZE) * width + block_offset,
                                        NEXT_BLOCK_TOP_POS + (BLOCK_SIZE + BLOCK_MARGIN_SIZE) * height + row + vert_offset, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(SCREEN, block_color.get(
                    avaliable_blocks[i] + 1), cur_pixel)

    # draws the held block
    hold_block_outline = pygame.Rect(
        HOLD_LEFT_MARGIN, BOARD_TOP_MARGIN - BLOCK_MARGIN_SIZE, NEXT_BLOCK_WIDTH, HOLD_HEIGHT + 2 * BLOCK_MARGIN_SIZE)
    hold_block_black = pygame.Rect(HOLD_LEFT_MARGIN + BLOCK_MARGIN_SIZE, BOARD_TOP_MARGIN,
                                   NEXT_BLOCK_WIDTH - 2 * BLOCK_MARGIN_SIZE, HOLD_HEIGHT)
    pygame.draw.rect(SCREEN, GRAY, hold_block_outline)
    pygame.draw.rect(SCREEN, BLACK, hold_block_black)

    block_offset = 0
    vert_offset = 0

    if alt_block is not None:
        # pretties up edge case blocks I and O, makes them centered
        if alt_block.type == 0:
            vert_offset = (BLOCK_SIZE + BLOCK_MARGIN_SIZE) // 2
        elif alt_block.type != 1:
            block_offset = (BLOCK_SIZE + BLOCK_MARGIN_SIZE) // 2
        for width in range(4):
            for height in range(2):
                # don't draw blank squares
                if not display_block_types.get(alt_block.type)[height][width]:
                    continue
                cur_pixel = pygame.Rect(HOLD_BLOCK_LEFT_POS + (BLOCK_SIZE + BLOCK_MARGIN_SIZE) * width + block_offset,
                                        HOLD_BLOCK_TOP_POS + (BLOCK_SIZE + BLOCK_MARGIN_SIZE) * height + vert_offset, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(SCREEN, block_color.get(
                    alt_block.color), cur_pixel)

    score_text = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_text, (HOLD_BLOCK_LEFT_POS - 20,
                HOLD_BLOCK_TOP_POS + HOLD_HEIGHT + 20))

    pygame.display.update()


def clear_rows(board, score, level=1):
    """
    Removes all rows which have been completely filled. Also calculates score based off of lines removed
    """

    current_row = BOARD_HEIGHT - 1
    new_board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
    lines = 0
    for r in range(BOARD_HEIGHT - 1, -1, -1):
        is_full_row = True

        # finds whether a row is full or not
        for c in range(BOARD_WIDTH):
            if board[r][c] == 0:
                is_full_row = False
                break

        if is_full_row:
            lines += 1

        # if all elements are empty
        if np.all(board[r] == 0):
            break

        # if row is not full or not row of zeros
        if not is_full_row:
            new_board[current_row] = board[r]  # add the row to the new board
            current_row -= 1

    # scoring_system
    if lines == 1:
        score += 40 * level
    elif lines == 2:
        score += 100 * level
    elif lines == 3:
        score += 300 * level
    elif lines == 4:
        score += 1200 * level

    return new_board, score, lines


def main():
    """
    Handles all input from the user. Controls everything. Should be split into seperate functions/classes when refactoring
    """

    clock = pygame.time.Clock()
    board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))

    # movement timer helpers
    moving = False
    moving_horizontally = False
    hard_dropping = False
    rotating = False
    switching = False
    stopped_counter = 0
    score = 0
    lines = 0

    # gets the first block
    avaliable_blocks = [0, 1, 2, 3, 4, 5, 6]
    random.shuffle(avaliable_blocks)
    block = Block(avaliable_blocks.pop(0))
    alt_block = None

    running = True
    while running:
        clock.tick(60)
        keys_pressed = pygame.key.get_pressed()
        level = 1 + lines // 10
        BLOCK_MOVE_SPEED = BLOCK_MOVE_SPEED_START - 100 * level
        if BLOCK_MOVE_SPEED <= 0:
            BLOCK_MOVE_SPEED = 20

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
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
            elif event.type == move_switching:
                switching = False
            elif event.type == game_over:
                running = False

        # dropping mechanics
        if keys_pressed[pygame.K_SPACE] and not hard_dropping:
            hard_dropping = True
            while True:  # drops block as far down as possible
                if not block.move_down(board):
                    block, board, avaliable_blocks, score, new_lines = place_block(
                        block, board, avaliable_blocks, score, level)
                    stopped_counter = 0
                    lines += new_lines
                    break
            pygame.time.set_timer(move_hard_drop, HARD_DROP_SPEED)
            pygame.time.set_timer(move_switching, 150)
        if keys_pressed[pygame.K_DOWN]:  # drops block fast
            block.move_down(board)

        # switching blocks
        if keys_pressed[pygame.K_c] and not switching:
            if alt_block is None:
                alt_block = Block(block.type)
                block, avaliable_blocks = get_next_block(avaliable_blocks)
            else:
                temp_block = Block(block.type)
                block = Block(alt_block.type)
                alt_block = Block(temp_block.type)
            switching = True

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
            block, board, avaliable_blocks, score, new_lines = place_block(
                block, board, avaliable_blocks, score, level)
            stopped_counter = 0
            pygame.time.set_timer(move_switching, 150)
            lines += new_lines

        # draws block shadow
        block_shadow = copy.deepcopy(block)
        while True:
            if not block_shadow.move_down(board):
                break

        # resets movement timer
        if not moving:
            pygame.time.set_timer(move_block_down, BLOCK_MOVE_SPEED)
            moving = True

        draw_screen(board, block, block_shadow,
                    avaliable_blocks, alt_block, score)


# for debugging
def log_board(board, block):
    """
    Logs the board and prints out current score, lines and the next blocks. For debugging
    """

    print(avaliable_blocks)
    print(f"Score is: {score}. Total lines cleared is: {lines}")

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
    while True:
        main()
