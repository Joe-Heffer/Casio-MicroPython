"""Desktop stand-in for the fx-CG100 casioplot module.

Lets programs written for the calculator run on a laptop or in CI.
Put this folder first on the import path, for example:

    PYTHONPATH=tools python programs/mandelbrot/mandelbrot.py

The screen is held in a Pillow image. If tkinter and a display are
available, show_screen() also refreshes a small window. Otherwise it
runs headless.

Environment variables:
    CASIOPLOT_HEADLESS=1   never open a window
    CASIOPLOT_SAVE=a.png   save the screen to this file when the program ends
    CASIOPLOT_WAIT=1       keep the window open after the program ends

Only the five documented functions are provided. Text is drawn with
Pillow's built-in font, so its size and shape are approximate.
"""

import atexit
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# Drawing area of casioplot on the fx-CG100, from Casio's manual
# (0 <= x <= 383, 0 <= y <= 191). Not yet checked on hardware by this project.
SCREEN_WIDTH = 384
SCREEN_HEIGHT = 192

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Approximate pixel heights for the three text sizes.
_FONT_SIZES = {"small": 10, "medium": 14, "large": 18}

_image = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), WHITE)
_draw = ImageDraw.Draw(_image)
_fonts = {}
_window = None
_label = None
_photo = None


def _font(size):
    if size not in _FONT_SIZES:
        raise ValueError("size must be 'small', 'medium' or 'large'")
    if size not in _fonts:
        try:
            _fonts[size] = ImageFont.load_default(size=_FONT_SIZES[size])
        except TypeError:  # Pillow older than 10.1 has one fixed font
            _fonts[size] = ImageFont.load_default()
    return _fonts[size]


def _want_window():
    if os.environ.get("CASIOPLOT_HEADLESS"):
        return False
    if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
        return False
    return True


def _open_window():
    """Open the tkinter window, or return False if that is not possible."""
    global _window, _label
    try:
        import tkinter
        _window = tkinter.Tk()
    except Exception:
        _window = False
        return False
    _window.title("casioplot (desktop stand-in)")
    _window.resizable(False, False)
    _label = tkinter.Label(_window, border=0)
    _label.pack()
    return True


def _in_range(x, y):
    return 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT


def set_pixel(x, y, color=BLACK):
    """Set one pixel to an (r, g, b) colour. Off-screen pixels are ignored."""
    x, y = int(x), int(y)
    if _in_range(x, y):
        _image.putpixel((x, y), tuple(color))


def get_pixel(x, y):
    """Return the (r, g, b) colour of a pixel, or None if off-screen."""
    x, y = int(x), int(y)
    if _in_range(x, y):
        return _image.getpixel((x, y))
    return None


def draw_string(x, y, text, color=BLACK, size="medium"):
    """Draw text with its top-left corner at (x, y)."""
    _draw.text((int(x), int(y)), str(text), fill=tuple(color), font=_font(size))


def clear_screen():
    """Set every pixel to white."""
    _draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill=WHITE)


def show_screen():
    """Refresh the window, if there is one."""
    global _photo
    if _window is None and _want_window():
        _open_window()
    if not _window:
        return
    from PIL import ImageTk
    _photo = ImageTk.PhotoImage(_image)
    _label.configure(image=_photo)
    _window.update()


def save_screen(path):
    """Save the screen to an image file. Desktop only; not on the calculator."""
    _image.save(path)


@atexit.register
def _at_exit():
    path = os.environ.get("CASIOPLOT_SAVE")
    if path:
        save_screen(path)
    if _window and os.environ.get("CASIOPLOT_WAIT"):
        _window.mainloop()
