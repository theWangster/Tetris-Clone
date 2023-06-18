import numpy as np

WIDTH, HEIGHT = 1080, 720
BOARD_WIDTH, BOARD_HEIGHT = 10, 22
CAPTION = "Tetris"
BLOCK_SIZE = HEIGHT // (BOARD_HEIGHT + 5)
BLOCK_MARGIN_SIZE = HEIGHT // (BOARD_HEIGHT * 15)
BOARD_LEFT_MARGIN = (WIDTH - BLOCK_SIZE * BOARD_WIDTH -
                     BLOCK_MARGIN_SIZE * (BOARD_WIDTH + 1)) // 2
BOARD_TOP_MARGIN = (HEIGHT - BOARD_HEIGHT * BLOCK_SIZE -
                    (BOARD_HEIGHT + 1) * BLOCK_MARGIN_SIZE) // 2
NEXT_BLOCK_LEFT = BOARD_LEFT_MARGIN + BOARD_WIDTH * \
    (BLOCK_SIZE + BLOCK_MARGIN_SIZE) + 20
NEXT_BLOCK_WIDTH = BLOCK_SIZE * 5 + BLOCK_MARGIN_SIZE * 6
NEXT_BLOCK_HEIGHT = BLOCK_SIZE * 12 + BLOCK_MARGIN_SIZE * 13

# game settings (feel free to tune to your comfort)
BLOCK_MOVE_SPEED_START = 1000
MOVEMENT_SPEED = 80
ROTATION_SPEED = 125
HARD_DROP_SPEED = 125
TIME_FOR_STOP = 2

# blocks
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

# colors
BLACK = (0, 0, 20)
GRAY = (40, 40, 50)
GREY = (20, 20, 30)
WHITE = (255, 255, 255)
PURPLE = (112, 0, 161)
MAGENTA = (195, 0, 255)
BLUE = (36, 36, 255)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (219, 226, 0)
ORANGE = (255, 171, 0)
RED = (255, 0, 0)
