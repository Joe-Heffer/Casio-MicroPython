"""Compile and run every program under MicroPython 1.9.4.

Usage: python tools/micropython_test.py [micropython-dir]

The fx-CG100 runs MicroPython 1.9.4, which is older and stricter than
desktop Python. This test uses the real 1.9.4 interpreter, built by
tools/build_micropython.sh (default location: .micropython/).

For every program it:
  * compiles the source with the 1.9.4 mpy-cross compiler, which rejects
    syntax that MicroPython 1.9.4 does not support
  * runs casioplot programs to the end with a small heap (HEAP_SIZE) and a
    strict casioplot stand-in (tools/micropython/casioplot.py), which
    rejects wrong argument types, colours, text sizes and non-ASCII text
  * checks that something was drawn, that show_screen() was called, and
    that nothing was drawn after the last show_screen() call

The program reads blank lines from input(), so prompts take their defaults.
Programs that do not use casioplot are compiled but not run.

Set MICROPYTHON_HEAP to change the heap size, for example 64k.
"""

import os
import re
import subprocess
import sys
import tempfile

# The fx-CG100's Python heap size is not published. This is an assumed,
# deliberately small figure; raise it only once a real calculator shows
# that more is available (see docs/limits.md).
HEAP_SIZE = os.environ.get("MICROPYTHON_HEAP", "32k")
TIMEOUT = 300  # seconds

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUBS = os.path.join(ROOT, "tools", "micropython")
PROGRAMS = os.path.join(ROOT, "programs")


def compile_check(mpy_cross, source):
    """Return an error message, or None if mpy-cross accepts the file."""
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [mpy_cross, "-o", os.path.join(tmp, "out.mpy"), source],
            capture_output=True, text=True)
    if result.returncode != 0:
        return "mpy-cross 1.9.4 rejected it\n" + result.stdout + result.stderr
    return None


def run(micropython, source):
    """Return (error message or None, note to print)."""
    env = dict(os.environ)
    env["MICROPYPATH"] = STUBS + os.pathsep + os.path.dirname(source)
    try:
        result = subprocess.run(
            [micropython, "-X", "heapsize=" + HEAP_SIZE,
             os.path.join(STUBS, "run.py"), source],
            input="\n" * 100, env=env, capture_output=True, text=True,
            timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "took longer than %d seconds" % TIMEOUT, ""

    output = result.stdout + result.stderr
    if result.returncode != 0:
        return "failed with a %s heap\n%s" % (HEAP_SIZE, output), ""

    match = re.search(r"^RESULT (.*)$", result.stdout, re.MULTILINE)
    if not match:
        return "the test runner printed no result\n" + output, ""
    stats = dict(item.split("=") for item in match.group(1).split())
    stats = {key: int(value) for key, value in stats.items()}

    if stats["pixels"] == 0 and stats["strings"] == 0:
        return "nothing was drawn", ""
    if stats["shows"] == 0:
        return "show_screen() was never called, so nothing would appear", ""
    if stats["pending"]:
        return "drawing after the last show_screen() call would not appear", ""
    return None, "%d bytes of %s heap free at end" % (stats["free"], HEAP_SIZE)


def main(argv):
    build = argv[1] if len(argv) > 1 else os.path.join(ROOT, ".micropython")
    micropython = os.path.join(build, "ports", "unix", "micropython")
    mpy_cross = os.path.join(build, "mpy-cross", "mpy-cross")
    for binary in (micropython, mpy_cross):
        if not os.access(binary, os.X_OK):
            print("Missing %s. Run: sh tools/build_micropython.sh" % binary)
            return 1

    failed = False
    for name in sorted(os.listdir(PROGRAMS)):
        source = os.path.join(PROGRAMS, name, name + ".py")
        if not os.path.isfile(source):
            continue
        error = compile_check(mpy_cross, source)
        note = ""
        if error is None:
            with open(source) as f:
                uses_casioplot = "casioplot" in f.read()
            if uses_casioplot:
                error, note = run(micropython, source)
            else:
                print("%-30s compiled; not run (does not use casioplot)" % name)
                continue
        print("%-30s %s" % (name, "FAIL: " + error if error else "ok, " + note))
        failed = failed or error is not None

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
