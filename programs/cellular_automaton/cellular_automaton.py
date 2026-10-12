# Elementary cellular automaton for the Casio fx-CG100
# Each row of the screen is one generation of a line of cells.
# Licence: MIT (see LICENSE at the top of the repository)

from casioplot import set_pixel, draw_string, clear_screen, show_screen
import random

# ---- Settings: edit these to change the picture ----

# Wolfram rule number, 0 to 255. Try 30, 90, 110 or 184.
RULE = 30

# Size of each cell in pixels. 1 gives the most detail, 2 or 3 is easier to see.
CELL_SIZE = 2

# Start with one live cell in the middle (False) or a random row (True).
RANDOM_START = False

# Chance that a cell starts alive when RANDOM_START is True (0.0 to 1.0).
DENSITY = 0.5

# Join the left and right edges, so the line of cells is a loop.
WRAP = True

# Redraw the screen after this many generations so progress is visible.
ROWS_PER_REFRESH = 4

# Show the rule number when finished (True or False).
SHOW_TITLE = True

# casioplot drawing area in pixels (0..383 by 0..191).
SCREEN_WIDTH = 384
SCREEN_HEIGHT = 192

# ---- Colours ----

ALIVE = (0, 0, 128)
TITLE = (224, 32, 32)


def first_row(width):
    """Return the first generation as a list of 0s and 1s."""
    if RANDOM_START:
        return [1 if random.random() < DENSITY else 0 for i in range(width)]
    row = [0] * width
    row[width // 2] = 1
    return row


def next_row(row):
    """Return the next generation by applying RULE to each cell."""
    width = len(row)
    new = [0] * width
    for i in range(width):
        if WRAP:
            left = row[i - 1]
            right = row[(i + 1) % width]
        else:
            left = row[i - 1] if i > 0 else 0
            right = row[i + 1] if i < width - 1 else 0
        # The three cells make a number from 0 to 7.
        # Bit number <pattern> of RULE gives the new state.
        pattern = left * 4 + row[i] * 2 + right
        new[i] = (RULE >> pattern) & 1
    return new


def draw_row(row, y):
    """Draw one generation with its top edge at pixel row y."""
    for i in range(len(row)):
        if row[i]:
            x = i * CELL_SIZE
            for dx in range(CELL_SIZE):
                for dy in range(CELL_SIZE):
                    set_pixel(x + dx, y + dy, ALIVE)


def draw():
    clear_screen()
    width = SCREEN_WIDTH // CELL_SIZE
    height = SCREEN_HEIGHT // CELL_SIZE
    row = first_row(width)
    for generation in range(height):
        draw_row(row, generation * CELL_SIZE)
        if generation % ROWS_PER_REFRESH == 0:
            show_screen()
        row = next_row(row)
    if SHOW_TITLE:
        draw_string(4, 4, "Rule " + str(RULE), TITLE, "small")
    show_screen()


draw()
