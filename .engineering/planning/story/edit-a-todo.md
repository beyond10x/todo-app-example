---
format: aep.planning-md/3
id: story:edit-a-todo
kind: story
status: proposed
title: Edit a todo's text in place
summary: edit N TEXT replaces a todo's text and keeps its number, done mark and priority
scope:
- confidence: cited
  path: README.md
- confidence: cited
  path: tests/test_todo.py
- confidence: cited
  path: todo.py
revision: 3
transitions:
- {from: "draft", to: "proposed", at: "2026-10-31T03:29:12Z", actor: "human:timo", revision: 3}
---
# Story: edit a todo

## Outcome

A todo's text can be changed in place.

- `./todo.py edit N TEXT` replaces the text of todo `N` and keeps its number, its done mark and its
  priority. Surrounding whitespace in `TEXT` is stripped, as `add` does.
- Text that is empty after stripping is refused with exit 1, as `done` and `remove` refuse, and the file is left unchanged.
- A number that names no todo is refused with exit 1, as `done` and `remove` refuse, and the file is left unchanged.
- `README.md` documents `edit`.

## Acceptance

`./check.sh` exits 0 with tests that edit a todo and check its new text in `list` with the same
number, done mark and priority, the refusal of empty text with the file unchanged, and the refusal
of a number that names no todo with the file unchanged. The existing tests in `tests/test_todo.py`
stay as they are.

## Scope

- `todo.py` (the `edit` command)
- `tests/test_todo.py` (the tests above)
- `README.md` (the command)

Claimed: takt pod run (gpt-6-astra), 2026-10-31
