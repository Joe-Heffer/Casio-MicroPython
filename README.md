# Casio-MicroPython

[![CI](https://github.com/Joe-Heffer/Casio-MicroPython/actions/workflows/ci.yml/badge.svg)](https://github.com/Joe-Heffer/Casio-MicroPython/actions/workflows/ci.yml)
[![MicroPython 1.9.4](https://img.shields.io/badge/MicroPython-1.9.4-2B2728?logo=micropython&logoColor=white)](https://github.com/micropython/micropython/releases/tag/v1.9.4)
[![Casio fx-CG100](https://img.shields.io/badge/runs%20on-Casio%20fx--CG100-0A3D91)](https://www.casio.com/intl/scientific-calculators/product.FX-CG100/)
[![Screen 384×192](https://img.shields.io/badge/screen-384%C3%97192%20px-ff69b4)](docs/limits.md)
[![Lines ≤ 300](https://img.shields.io/badge/lines%20per%20program-%E2%89%A4%20300-orange)](docs/limits.md)
[![ASCII only](https://img.shields.io/badge/charset-ASCII%20only-lightgrey)](docs/limits.md)
[![f-strings: none](https://img.shields.io/badge/f--strings-none%20allowed-red)](docs/limits.md)
[![Heap 32 KB](https://img.shields.io/badge/CI%20heap-32%20KB-yellow)](#what-ci-checks)
[![Licence: MIT](https://img.shields.io/badge/licence-MIT-green)](LICENSE)

MicroPython programs for the Casio fx-CG100 graphing calculator, with tools to check and run them on a laptop.

Each program is a single `.py` file of no more than 300 lines, the limit for one file in the calculator’s Python app. Graphics use Casio’s `casioplot` module. The `turtle` and `matplotlib.pyplot` modules are also available on the calculator.

## Programs

| Program | Description | Lines | Tested on |
|---|---|---|---|
| [mandelbrot](programs/mandelbrot/) | Mandelbrot set in colour, drawn column by column | 88 | Desktop stand-in |

## Repository layout

```
programs/<name>/        one folder per program
    <name>.py           the program (copy this to the calculator)
    README.md           description, controls, settings, memory notes
    screenshots/        at least one screenshot
tools/
    casioplot.py        desktop stand-in for the casioplot module
    check_programs.py   300-line limit, layout and import check
    smoke_test.py       runs each casioplot program headless
    build_micropython.sh builds MicroPython 1.9.4 (the calculator's version)
    micropython_test.py compiles and runs each program under MicroPython 1.9.4
    micropython/        strict casioplot stand-in used by micropython_test.py
docs/
    transfer.md         copying programs to the calculator
    limits.md           memory, speed, screen and module limits
    program-readme-template.md
```

## Development quick start

You need Python 3.10 or later.

```sh
pip install -r requirements-dev.txt

# Run a program in a window on your computer
PYTHONPATH=tools python programs/mandelbrot/mandelbrot.py

# Run the same checks as CI
python tools/check_programs.py
python -m compileall -q programs tools
python tools/smoke_test.py

# Run the programs under MicroPython 1.9.4 (Linux or macOS; needs git, make and a C compiler)
sh tools/build_micropython.sh
python tools/micropython_test.py
```

On Windows PowerShell, set the path with `$env:PYTHONPATH = "tools"` first.

`tools/casioplot.py` is a small stand-in for Casio’s `casioplot` module, built on Pillow. It opens a tkinter window when one is available and runs headless otherwise, for example in CI. Set `CASIOPLOT_SAVE=out.png` to save the final screen, and `CASIOPLOT_WAIT=1` to keep the window open when the program ends. It only approximates the calculator: text uses Pillow’s font, and speed bears no relation to the real device. Always test on the emulator or the calculator before you share a program.

If you want a fuller desktop emulation with a calculator frame, see [uniwix/casioplot](https://github.com/uniwix/casioplot) (`pip install casioplot`). It needs tkinter and a display, so this repository does not use it in CI.

## What CI checks

Every push and pull request runs these checks on GitHub Actions:

1. **Limits and layout** (`tools/check_programs.py`): 300 lines, 255 characters per line, ASCII only, no f-strings, and imports only from `casioplot`, `math`, `random`, `turtle` and `matplotlib.pyplot`.
2. **Desktop smoke test** (`tools/smoke_test.py`) on Python 3.10 and 3.13: each `casioplot` program runs to the end with the Pillow stand-in, and the final screen is uploaded as a build artefact so you can look at it.
3. **MicroPython 1.9.4** (`tools/micropython_test.py`): CI builds the same MicroPython version as the calculator from source. Every program must compile with its `mpy-cross` compiler. Each `casioplot` program then runs to the end in that interpreter with a 32 KB heap and a strict `casioplot` stand-in, which rejects:
    * non-integer coordinates
    * colours that are not three integers from 0 to 255
    * text sizes other than `"small"`, `"medium"` and `"large"`, and text that is not printable ASCII
    * programs that draw nothing, never call `show_screen()`, or draw after their last `show_screen()` call

`input()` receives blank lines, so prompts take their defaults.

A program that passes all three is very likely to run on the calculator, but CI cannot prove it. It cannot check:

* Casio’s own changes to MicroPython, if any.
* The real heap size. Casio does not publish it, so 32 KB is an assumption. Set `MICROPYTHON_HEAP=64k` to try other sizes locally.
* Speed. A program that finishes in a second in CI may take minutes on the calculator.
* What the screen looks like. Text size and position are approximate.
* `turtle` and `matplotlib.pyplot` programs, which are compiled but not run.
* `get_pixel()` in the MicroPython test, which always returns white there.

So test on the calculator or Casio’s emulator before you tick “Tested on” in a program’s README.

## Copying a program to the calculator

1. Connect the calculator to your computer with a USB cable.
2. On the calculator, choose **USB Flash** in the **Select Connection Mode** dialogue.
3. Copy the program’s `.py` file to the drive that appears.
4. Eject the drive before you unplug the cable.
5. Run the program from the calculator’s **Python** app.

See [docs/transfer.md](docs/transfer.md) for details and pitfalls, and [docs/limits.md](docs/limits.md) for the calculator’s limits.

## Screen size

Programs and the stand-in use one pair of constants, `SCREEN_WIDTH = 384` and `SCREEN_HEIGHT = 192`. Casio’s user’s guide gives the `casioplot` drawing range as x 0–383 and y 0–191. Casio’s product page gives the full display as 384 × 216 dots, so `casioplot` does not use the whole panel.

**Unverified:** this project has not yet checked the 384 × 192 figure on a real calculator. The Casio pages were read through search-engine extracts because the Casio site could not be opened directly when this README was written.

## Related projects

* [eanutt1272v2/fx-cg100-sci-library](https://github.com/eanutt1272v2/fx-cg100-sci-library): an open-source MicroPython library for the fx-CG100, with fractal and hydrogen orbital scripts.
* [uniwix/casioplot](https://github.com/uniwix/casioplot): desktop emulation of `casioplot` with a tkinter window.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

Original work in this repository is under the [MIT licence](LICENSE).

Any code derived from Casio’s sample programs is under the GNU General Public License (GPL) and must keep that licence. Such programs must say so in their README and in a comment at the top of the `.py` file, and the MIT licence does not apply to them.
