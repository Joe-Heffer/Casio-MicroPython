# Casio-MicroPython

MicroPython programs for the Casio fx-CG100 graphing calculator, with tools to check and run them on a laptop.

Each program is a single `.py` file of no more than 300 lines, the limit for one file in the calculator’s Python app. Graphics use Casio’s `casioplot` module. The `turtle` and `matplotlib.pyplot` modules are also available on the calculator.

## Programs

| Program | Description | Lines | Tested on |
|---|---|---|---|
| [cellular_automaton](programs/cellular_automaton/) | Elementary cellular automaton (Wolfram rules 0–255), drawn row by row | 93 | Desktop stand-in |
| [mandelbrot](programs/mandelbrot/) | Mandelbrot set in colour, drawn column by column | 88 | Desktop stand-in |

## Repository layout

```
programs/<name>/        one folder per program
    <name>.py           the program (copy this to the calculator)
    README.md           description, controls, settings, memory notes
    screenshots/        at least one screenshot
tools/
    casioplot.py        desktop stand-in for the casioplot module
    check_programs.py   300-line limit and layout check
    smoke_test.py       runs each casioplot program headless
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
```

On Windows PowerShell, set the path with `$env:PYTHONPATH = "tools"` first.

`tools/casioplot.py` is a small stand-in for Casio’s `casioplot` module, built on Pillow. It opens a tkinter window when one is available and runs headless otherwise, for example in CI. Set `CASIOPLOT_SAVE=out.png` to save the final screen, and `CASIOPLOT_WAIT=1` to keep the window open when the program ends. It only approximates the calculator: text uses Pillow’s font, and speed bears no relation to the real device. Always test on the emulator or the calculator before you share a program.

If you want a fuller desktop emulation with a calculator frame, see [uniwix/casioplot](https://github.com/uniwix/casioplot) (`pip install casioplot`). It needs tkinter and a display, so this repository does not use it in CI.

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
