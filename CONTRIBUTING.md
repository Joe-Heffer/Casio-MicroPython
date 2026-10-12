# Contributing

Thank you for adding a program. Please follow these rules so that every program runs on the calculator and is easy to read on its small screen.

## Rules for programs

* **300 lines at most.** The calculator’s Python app holds up to 300 lines per file. Lines must also be 255 characters or fewer.
* **ASCII only.** The calculator cannot show other characters, so avoid accented letters, curly quotes, arrows and emoji in the `.py` file, including in comments.
* **MicroPython 1.9.4.** Do not use f-strings. Use only the modules listed in [docs/limits.md](docs/limits.md).
* **One folder per program.** Put it in `programs/<name>/`, named in lower case with hyphens or underscores. The file inside must be `<name>.py`.
* **A README is required.** Copy [docs/program-readme-template.md](docs/program-readme-template.md) to `programs/<name>/README.md` and fill it in, including the line count and memory notes.
* **A screenshot is required.** Put at least one image in `programs/<name>/screenshots/`. A screenshot from the calculator or the emulator is best. If you use the desktop stand-in, say so in the caption.
* **One file per program.** The program must run with nothing else copied to the calculator.

## Style

* Write plain, commented code. Explain anything that is not obvious, briefly.
* Put the settings a user may want to change (region, iteration count, colours, speed) as constants at the top of the file, with a comment on each.
* Use `SCREEN_WIDTH = 384` and `SCREEN_HEIGHT = 192` for the `casioplot` drawing area. Do not scatter the numbers through the code.
* Keep text short. The screen is 384 pixels wide.
* Draw as you go rather than building large lists. Calculator memory is small.
* Call `show_screen()` now and then so the user can see progress.
* Use British English in comments, READMEs and on-screen text.

## Before you open a pull request

Run the same checks as CI:

```sh
pip install -r requirements-dev.txt
python tools/check_programs.py
python -m compileall -q programs tools
python tools/smoke_test.py
```

Then:

* Add your program to the table in the top-level [README.md](README.md).
* Tick the “Tested on” boxes in your program’s README honestly.

## Licence

Contributions are under the MIT licence unless they are derived from a Casio sample program. Code derived from Casio’s samples is under the GPL and must keep that licence: say so in the program’s README and in a comment at the top of its `.py` file.
