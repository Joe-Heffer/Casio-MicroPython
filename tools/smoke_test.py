"""Run every casioplot program headless with the desktop stand-in.

Usage: python tools/smoke_test.py [output-dir]

Each program that imports casioplot is run in its own process with
tools/ first on the import path. The test fails if a program raises an
error, takes longer than TIMEOUT seconds, or leaves a blank screen.
The final screen of each program is saved as <output-dir>/<name>.png
(default: smoke-output/).

Programs that do not use casioplot (turtle or matplotlib only) are skipped.
"""

import os
import subprocess
import sys

from PIL import Image

TIMEOUT = 120  # seconds

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
PROGRAMS = os.path.join(ROOT, "programs")


def uses_casioplot(path):
    with open(path) as f:
        return "casioplot" in f.read()


def run(name, source, output_dir):
    """Run one program. Return an error message, or None if it passed."""
    image_path = os.path.join(output_dir, name + ".png")
    if os.path.exists(image_path):
        os.remove(image_path)

    env = dict(os.environ)
    env["PYTHONPATH"] = TOOLS + os.pathsep + env.get("PYTHONPATH", "")
    env["CASIOPLOT_HEADLESS"] = "1"
    env["CASIOPLOT_SAVE"] = image_path
    env.pop("CASIOPLOT_WAIT", None)

    try:
        result = subprocess.run(
            [sys.executable, source],
            cwd=os.path.dirname(source),
            env=env,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return "took longer than %d seconds" % TIMEOUT

    if result.returncode != 0:
        return "exited with status %d\n%s" % (result.returncode, result.stderr)
    if not os.path.exists(image_path):
        return "no screen image was saved"

    colours = Image.open(image_path).getcolors(maxcolors=1)
    if colours is not None:  # only one colour on the whole screen
        return "screen is blank"
    return None


def main(argv):
    output_dir = argv[1] if len(argv) > 1 else os.path.join(ROOT, "smoke-output")
    os.makedirs(output_dir, exist_ok=True)

    failed = False
    for name in sorted(os.listdir(PROGRAMS)):
        source = os.path.join(PROGRAMS, name, name + ".py")
        if not os.path.isfile(source):
            continue
        if not uses_casioplot(source):
            print("%-30s skipped (does not use casioplot)" % name)
            continue
        error = run(name, source, output_dir)
        print("%-30s %s" % (name, "FAIL: " + error if error else "ok"))
        failed = failed or error is not None

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
