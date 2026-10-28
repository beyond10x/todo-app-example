#!/usr/bin/env python3
"""A todo list kept in a JSON file: add an item, list the items, mark one done, remove one."""

import argparse
import json
import os
import sys
from pathlib import Path

DEFAULT_FILE = "todo.json"
PRIORITIES = ("high", "normal", "low")


def load(path):
    path = Path(path)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, items):
    Path(path).write_text(json.dumps(items, indent=2) + "\n", encoding="utf-8")


def add(items, text, priority="normal"):
    text = text.strip()
    if not text:
        raise ValueError("a todo needs some text")
    if priority not in PRIORITIES:
        raise ValueError(f"there is no priority {priority}")
    items.append({"text": text, "done": False, "priority": priority})
    return items


def done(items, number):
    if number < 1 or number > len(items):
        raise ValueError(f"there is no todo {number}")
    items[number - 1]["done"] = True
    return items


def remove(items, number):
    if number < 1 or number > len(items):
        raise ValueError(f"there is no todo {number}")
    del items[number - 1]
    return items


def priority_of(item):
    # Items written before priorities existed carry none; they are normal.
    return item.get("priority", "normal")


def render(items, sort=None):
    numbered = list(enumerate(items, start=1))
    if sort == "priority":
        numbered.sort(key=lambda pair: PRIORITIES.index(priority_of(pair[1])))
    lines = []
    for number, item in numbered:
        priority = priority_of(item)
        label = "" if priority == "normal" else f"({priority}) "
        box = "x" if item["done"] else " "
        lines.append(f"{number}. [{box}] {label}{item['text']}")
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(prog="todo")
    parser.add_argument("--file", default=os.environ.get("TODO_FILE", DEFAULT_FILE))
    commands = parser.add_subparsers(dest="command", required=True)
    list_command = commands.add_parser("list")
    list_command.add_argument("--sort", choices=["priority"])
    add_command = commands.add_parser("add")
    add_command.add_argument("text")
    add_command.add_argument("--priority", choices=PRIORITIES, default="normal")
    done_command = commands.add_parser("done")
    done_command.add_argument("number", type=int)
    remove_command = commands.add_parser("remove")
    remove_command.add_argument("number", type=int)
    args = parser.parse_args(argv)

    items = load(args.file)
    try:
        if args.command == "add":
            save(args.file, add(items, args.text, args.priority))
        elif args.command == "done":
            save(args.file, done(items, args.number))
        elif args.command == "remove":
            save(args.file, remove(items, args.number))
        else:
            for line in render(items, args.sort):
                print(line)
    except ValueError as error:
        print(f"todo: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
