import os
from kivy.core.image import Image

# Size of each block in the game.
BLOCK_SIZE = 40

# Origin of the board coordinates.
ORIGIN_X = 8 * BLOCK_SIZE
ORIGIN_Y = BLOCK_SIZE

# Size of the game board
HEIGHT = 20
WIDTH = 10

# Size of the window;
WINDOW_WIDTH = (WIDTH + 9) * BLOCK_SIZE
WINDOW_HEIGHT = (HEIGHT + 2) * BLOCK_SIZE

# Get the file names of textures
files = os.listdir('textures')

# Create TEXTURES dict
TEXTURES = {}

# Add every texture to TEXTURES
for file in files:
    name = file[:file.index('.')]
    path = 'textures/' + file
    TEXTURES[name] = Image.load(path).texture

del os, Image

# Pieces organizations and textues definitions.
PIECES = [
    # PIECE I
    {
        'rotations': [
            [(-2, 0), (-1, 0), (0, 0), (1, 0)],
            [(0,  0), (0,  1), (0, 2), (0, 3)]
        ],

        'texture': TEXTURES['cyan_block']
    },

    # PIECE S
    {
        'rotations': [
            [(-1, 0), (0, 0), (0, 1), (1, 1)],
            [(0,  0), (0,  1), (-1, 1), (-1, 2)]
        ],

        'texture': TEXTURES['green_block']
    },

    # PIECE Z
    {
        'rotations': [
            [(-1, 1), (0, 1), (0, 0), (1, 0)],
            [(-1,  0), (-1,  1), (0, 1), (0, 2)]
        ],

        'texture': TEXTURES['red_block']
    },

    # PIECE L
    {
        'rotations': [
            [(-1, 2), (-1, 1), (-1, 0), (0, 0)],
            [(-1, 0), (-1, 1), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (0, 2), (-1, 2)],
            [(-1, 0), (0, 0), (1, 0), (1, 1)]
        ],

        'texture': TEXTURES['orange_block']
    },

    # PIECE J
    {
        'rotations': [
            [(-1, 0), (0, 0), (0, 1), (0, 2)],
            [(-1, 1), (-1, 0), (0, 0), (1, 0)],
            [(-1, 0), (-1, 1), (-1, 2), (0, 2)],
            [(-1, 1), (0, 1), (1, 1), (1, 0)]
        ],

        'texture': TEXTURES['blue_block']
    },

    # PIECE O
    {
        'rotations': [
            [(-1, 0), (0, 0), (-1, 1), (0, 1)]
        ],

        'texture': TEXTURES['yellow_block']
    },

    # PIECE T
    {
        'rotations': [
            [(-1, 0), (0, 0), (1, 0), (0, 1)],
            [(-1, 0), (-1, 1), (-1, 2), (0, 1)],
            [(-1, 1), (0, 1), (1, 1), (0, 0)],
            [(-1, 1), (0, 0), (0, 1), (0, 2)]
        ],

        'texture': TEXTURES['purple_block']
    }
]

SCORE_PER_LINE = {1: 40, 2: 100, 3: 300, 4: 1200}
