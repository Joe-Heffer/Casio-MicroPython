"""Check every program against the fx-CG100 limits and the repository layout.

Usage: python tools/check_programs.py [programs-dir]

For each programs/<name>/ folder this checks that:
  * <name>.py exists and has no more than 300 lines
  * no line is longer than 255 characters
  * the file is plain ASCII (the calculator cannot show other characters)
  * there are no f-strings (not in MicroPython 1.9.4)
  * README.md and a screenshots/ folder exist

Exits with status 1 if any check fails.
"""

import ast
import os
import sys

MAX_LINES = 300
MAX_LINE_LENGTH = 255

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_source(path):
    """Return (line count, list of problems) for one .py file."""
    problems = []
    with open(path, "rb") as f:
        data = f.read()

    lines = data.splitlines()
    if len(lines) > MAX_LINES:
        problems.append("%d lines (limit %d)" % (len(lines), MAX_LINES))

    for number, line in enumerate(lines, 1):
        if len(line) > MAX_LINE_LENGTH:
            problems.append("line %d is %d characters (limit %d)"
                            % (number, len(line), MAX_LINE_LENGTH))
        if any(byte > 127 for byte in line):
            problems.append("line %d contains non-ASCII characters" % number)

    try:
        tree = ast.parse(data, path)
    except SyntaxError as error:
        problems.append("syntax error: %s" % error)
        return len(lines), problems

    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            problems.append("line %d uses an f-string" % node.lineno)

    return len(lines), problems


def check_folder(folder):
    """Return (line count or None, list of problems) for one program folder."""
    name = os.path.basename(folder)
    problems = []
    for required in ("README.md", "screenshots"):
        if not os.path.exists(os.path.join(folder, required)):
            problems.append("missing %s" % required)

    source = os.path.join(folder, name + ".py")
    if not os.path.isfile(source):
        problems.append("missing %s.py" % name)
        return None, problems

    count, source_problems = check_source(source)
    return count, problems + source_problems


def main(argv):
    programs = argv[1] if len(argv) > 1 else os.path.join(ROOT, "programs")
    folders = sorted(
        os.path.join(programs, entry)
        for entry in os.listdir(programs)
        if os.path.isdir(os.path.join(programs, entry))
    )
    if not folders:
        print("No programs found in %s" % programs)
        return 1

    failed = False
    print("%-30s %6s  %s" % ("program", "lines", "result"))
    for folder in folders:
        count, problems = check_folder(folder)
        shown = "-" if count is None else str(count)
        print("%-30s %6s  %s" % (os.path.basename(folder), shown,
                                 "FAIL" if problems else "ok"))
        for problem in problems:
            print("    - " + problem)
        failed = failed or bool(problems)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
