# Mandelbrot set renderer for the Casio fx-CG100
# Draws the set with the casioplot module, one column at a time.
# Licence: MIT (see LICENSE at the top of the repository)

from casioplot import set_pixel, draw_string, clear_screen, show_screen

# ---- Settings: edit these to change the picture ----

# Region of the complex plane to draw.
# Keep the X:Y ratio near 2:1 to match the screen.
X_MIN = -2.4
X_MAX = 1.0
Y_MIN = -0.85
Y_MAX = 0.85

# Maximum iterations per pixel. Higher shows more detail but is slower.
MAX_ITER = 16

# Redraw the screen after this many columns so progress is visible.
COLUMNS_PER_REFRESH = 8

# Show a title when finished (True or False).
SHOW_TITLE = True

# casioplot drawing area in pixels (0..383 by 0..191).
SCREEN_WIDTH = 384
SCREEN_HEIGHT = 192

# ---- Colours ----

# Points inside the set.
INSIDE = (0, 0, 0)

# Points outside the set, coloured by how quickly they escape.
PALETTE = [
    (0, 0, 96),
    (0, 0, 160),
    (0, 64, 224),
    (0, 128, 255),
    (0, 192, 255),
    (0, 224, 192),
    (96, 240, 96),
    (192, 255, 0),
    (255, 224, 0),
    (255, 160, 0),
    (255, 96, 0),
    (224, 32, 32),
]


def escape_time(cr, ci):
    """Return the number of steps before z escapes, or MAX_ITER if it stays."""
    zr = 0.0
    zi = 0.0
    for n in range(MAX_ITER):
        zr2 = zr * zr
        zi2 = zi * zi
        if zr2 + zi2 > 4.0:
            return n
        # z = z*z + c, written out with real numbers
        zi = 2.0 * zr * zi + ci
        zr = zr2 - zi2 + cr
    return MAX_ITER


def colour_for(n):
    if n >= MAX_ITER:
        return INSIDE
    return PALETTE[n % len(PALETTE)]


def draw():
    clear_screen()
    dx = (X_MAX - X_MIN) / SCREEN_WIDTH
    dy = (Y_MAX - Y_MIN) / SCREEN_HEIGHT
    for x in range(SCREEN_WIDTH):
        cr = X_MIN + x * dx
        for y in range(SCREEN_HEIGHT):
            ci = Y_MAX - y * dy
            set_pixel(x, y, colour_for(escape_time(cr, ci)))
        if x % COLUMNS_PER_REFRESH == 0:
            show_screen()
    if SHOW_TITLE:
        draw_string(4, 4, "Mandelbrot", (255, 255, 255), "small")
    show_screen()


draw()
