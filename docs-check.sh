#!/bin/sh
# README.md shows every command todo.py has: one `./todo.py <command>` line each.
set -eu
cd "$(dirname "$0")"
python3 -I -c '
import re, subprocess, sys
help_text = subprocess.run([sys.executable, "todo.py", "--help"], capture_output=True, text=True, check=True).stdout
commands = re.search(r"\{([a-z,-]+)\}", help_text).group(1).split(",")
readme = open("README.md", encoding="utf-8").read()
missing = [c for c in commands if not re.search(r"^\./todo\.py " + re.escape(c) + r"\b", readme, re.M)]
for c in missing:
    print(f"docs-check: README.md shows no ./todo.py {c} line", file=sys.stderr)
print(f"docs-check: {len(commands) - len(missing)} of {len(commands)} commands shown in README.md")
sys.exit(1 if missing else 0)
'
