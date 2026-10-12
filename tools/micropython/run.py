# Run one program under MicroPython 1.9.4 and report what it drew.
#
# Usage: micropython -X heapsize=N tools/micropython/run.py program.py
# Called by tools/micropython_test.py, which reads the last line.
# The program runs with __name__ == "__main__", as on the calculator.

import gc
import sys

path = sys.argv[1]
with open(path) as f:
    source = f.read()
code = compile(source, path, "exec")
del source
gc.collect()

exec(code, {"__name__": "__main__"})

import casioplot
gc.collect()
print("RESULT pixels=%d strings=%d shows=%d pending=%d free=%d" % (
    casioplot.pixels, casioplot.strings, casioplot.shows,
    casioplot.pending, gc.mem_free()))
