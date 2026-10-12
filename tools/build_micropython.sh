#!/bin/sh
# Build the MicroPython 1.9.4 unix port and mpy-cross, the same
# MicroPython version as the fx-CG100's Python app.
#
# Usage: sh tools/build_micropython.sh [build-dir]
# Default build-dir is .micropython/ at the top of the repository.
# Prints nothing more once the binaries exist, so it is safe to rerun.
#
# Needs git, make and a C compiler. Optional features that pull in extra
# libraries (ffi, btree, ssl, threads) are turned off. urandom is turned
# on because the calculator has a random module.

set -e

VERSION=v1.9.4
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DIR=${1:-"$ROOT/.micropython"}

if [ -x "$DIR/ports/unix/micropython" ] && [ -x "$DIR/mpy-cross/mpy-cross" ]; then
    echo "MicroPython $VERSION already built in $DIR"
    exit 0
fi

if [ ! -d "$DIR" ]; then
    git clone --quiet --depth 1 --branch "$VERSION" \
        https://github.com/micropython/micropython.git "$DIR"
fi

# Old code, new compilers: keep warnings, but do not treat them as errors.
make -C "$DIR/mpy-cross" -j4 CWARN="-Wall"
make -C "$DIR/ports/unix" -j4 CWARN="-Wall" \
    MICROPY_PY_FFI=0 MICROPY_PY_BTREE=0 MICROPY_PY_USSL=0 \
    MICROPY_PY_THREAD=0 MICROPY_PY_TERMIOS=0 \
    CFLAGS_EXTRA="-DMICROPY_PY_URANDOM=1 -DMICROPY_PY_URANDOM_EXTRA_FUNCS=1"

echo "Built MicroPython $VERSION in $DIR"
