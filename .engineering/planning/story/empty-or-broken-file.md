---
format: aep.planning-md/3
id: story:empty-or-broken-file
kind: story
status: proposed
title: An empty or broken todo.json is handled, not a traceback
summary: an empty file is an empty list; a file that is not a todo list is refused with exit 1 and left unchanged
scope:
- confidence: cited
  path: tests/test_todo.py
- confidence: cited
  path: todo.py
revision: 3
transitions:
- {from: "draft", to: "proposed", at: "2026-10-18T20:36:37Z", actor: "human:timo", revision: 3}
---
# Story: empty-or-broken-file

## Outcome

A user reported: `touch todo.json && ./todo.py list` prints a Python traceback
(`json.decoder.JSONDecodeError: Expecting value`) instead of an empty list. The failing test
`test_an_empty_file_is_an_empty_list` in `tests/test_todo.py` reproduces it.

- An empty `todo.json`, or one holding only white space, is an empty list: `list` prints nothing
  and exits 0, and `add` writes the first todo to it.
- A `todo.json` that is not a todo list (not JSON, or JSON that is not a list) is refused by every
  command (`list`, `add`, `done`, `remove`) with exit 1 and one line on standard error,
  `todo: <file> is not a todo list`, with no traceback; the file is left byte for byte as it was.

## Acceptance

`./check.sh` exits 0, with `test_an_empty_file_is_an_empty_list` passing unchanged and tests
for a file of white space, a file that is not JSON and a file holding a JSON object, each refused
by `list` and `add` with exit 1 and the file unchanged.

## Scope

- `todo.py` (`load` and the commands that call it)
- `tests/test_todo.py` (the tests above)
