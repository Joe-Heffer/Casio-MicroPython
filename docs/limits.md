# Known limits of the fx-CG100

These are the limits that matter when writing programs for this repository. Where a figure is not confirmed, the table says so.

| Limit | Value | Status |
|---|---|---|
| Program length | 300 lines per file | Casio user’s guide |
| Line length | 255 characters | Casio user’s guide |
| Character set | ASCII only | Casio user’s guide |
| Python version | MicroPython 1.9.4 | Casio product page |
| `casioplot` drawing area | 384 × 192 pixels (x 0–383, y 0–191) | Casio user’s guide; not yet checked on hardware by this project |
| Full display | 384 × 216 dots | Casio product page |
| `turtle` window | x −192 to 191, y −95 to 96 | Casio user’s guide |
| Python heap (RAM) | Unknown | No published figure found |
| Speed | Unknown | No published figure found |

`tools/check_programs.py` enforces the line count, line length, ASCII and module rules. `tools/micropython_test.py` runs each program under MicroPython 1.9.4 with an assumed 32 KB heap; change that figure in the script if a real calculator shows a different one.

## Modules

Casio’s guide lists these:

* Built-in functions
* `math`
* `random`
* `matplotlib.pyplot`
* `turtle` (a Casio version that differs from the desktop `turtle` module)
* `casioplot` (Casio’s own pixel and text drawing module)

Do not assume any other standard library module is present.

## casioplot

| Function | Purpose |
|---|---|
| `set_pixel(x, y, colour)` | Set one pixel. `colour` is an `(r, g, b)` tuple. |
| `get_pixel(x, y)` | Read one pixel’s colour. |
| `draw_string(x, y, text, colour, size)` | Draw text. `size` is `"small"`, `"medium"` or `"large"`. |
| `clear_screen()` | Clear the drawing area to white. |
| `show_screen()` | Show what has been drawn. Drawing is not visible until this is called. |

## MicroPython 1.9.4

MicroPython 1.9.4 is older than most desktop Python and lacks some features:

* No f-strings (added in MicroPython 1.17). Use `"%d" % n` or `str(n)` instead. `tools/check_programs.py` rejects f-strings.
* No assignment expressions (`:=`), `match` statements or other newer syntax. `tools/micropython_test.py` compiles each program with the 1.9.4 compiler to catch these.
* A smaller standard library. See the module list above.

## Memory and speed

There is no published heap size. If `gc` is available on your calculator, you can measure free memory with:

```python
import gc
gc.collect()
print(gc.mem_free())
```

General advice for a small device:

* Avoid building large lists, such as one entry per pixel. Draw as you go.
* Keep iteration counts low and let the user raise them.
* Call `show_screen()` every few rows or columns rather than after every pixel. Each call costs time, but calling it now and then shows progress.

## Sources

* Casio, fx-CG100 user’s guide: [Python App](https://support.casio.com/global/en/calc/manual/fx-CG100_1AUGRAPH_en/BONDSYlkjdoxxc.html)
* Casio, [fx-CG100 product page](https://www.casio.com/intl/scientific-calculators/product.FX-CG100/)
* Casio Education, [fx-CG100 ClassWiz Color Graph](https://www.casioeducation.com/graphing-calculators/fx-cg100) (MicroPython version)

These pages were read through search-engine extracts. The Casio site could not be opened directly when this guide was written, so check the figures against the pages themselves.
