# Strict casioplot stand-in for MicroPython 1.9.4 (unix port).
#
# Used by tools/micropython_test.py. It checks every call against the
# documented casioplot API and fails loudly on anything doubtful, so a
# program that passes here is more likely to work on the calculator.
#
# It does not keep the screen in memory, so the heap stays close to what a
# program uses on the calculator. get_pixel() therefore always returns
# white for on-screen pixels.

SCREEN_WIDTH = 384
SCREEN_HEIGHT = 192
_SIZES = ("small", "medium", "large")

# Counters read by the test runner.
pixels = 0       # set_pixel calls on screen with a colour other than white
strings = 0      # draw_string calls
shows = 0        # show_screen calls
pending = False  # True if something was drawn after the last show_screen


def _int(name, value):
    if type(value) is not int:
        raise TypeError("%s must be an int, not %s" % (name, type(value).__name__))


def _colour(colour):
    if type(colour) not in (tuple, list) or len(colour) != 3:
        raise TypeError("colour must be an (r, g, b) tuple, not %r" % (colour,))
    for part in colour:
        _int("colour component", part)
        if part < 0 or part > 255:
            raise ValueError("colour component %d is outside 0..255" % part)


def set_pixel(x, y, colour=(0, 0, 0)):
    global pixels, pending
    _int("x", x)
    _int("y", y)
    _colour(colour)
    if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
        if tuple(colour) != (255, 255, 255):
            pixels += 1
        pending = True


def get_pixel(x, y):
    _int("x", x)
    _int("y", y)
    if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
        return (255, 255, 255)
    return None


def draw_string(x, y, text, colour=(0, 0, 0), size="medium"):
    global strings, pending
    _int("x", x)
    _int("y", y)
    if type(text) is not str:
        raise TypeError("text must be a str, not %s" % type(text).__name__)
    for ch in text:
        if ord(ch) > 126 or ord(ch) < 32:
            raise ValueError("text must be printable ASCII: %r" % text)
    _colour(colour)
    if size not in _SIZES:
        raise ValueError("size must be 'small', 'medium' or 'large'")
    strings += 1
    pending = True


def clear_screen():
    global pending
    pending = True


def show_screen():
    global shows, pending
    shows += 1
    pending = False
