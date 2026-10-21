---
format: aep.planning-md/3
id: story:remove-a-todo
kind: story
status: active
title: Remove a todo by its number
summary: todo.py remove N deletes item N; an unknown number is refused
scope:
- confidence: cited
  path: tests/test_todo.py
- confidence: cited
  path: todo.py
revision: 4
transitions:
- {from: "draft", to: "proposed", at: "2026-10-18T09:25:05Z", actor: "human:timo", revision: 3}
- {from: "proposed", to: "active", at: "2026-10-21T21:07:35Z", actor: "human:timo", revision: 4, executor: "agent:takt"}
---
# Story: remove-a-todo

## Outcome

`./todo.py remove N` deletes todo number N from the list; the items after it move up one number.
A number that names no todo is refused with exit 1 and the list is left unchanged.

## Acceptance

`./check.sh` exits 0 with tests that add three todos, remove number 2 and list `1. [ ] <first>`
and `2. [ ] <third>`, and that show `remove 0` and `remove 4` on a list of three exit 1 with the
file unchanged.

## Scope

- `todo.py` (a `remove` command beside `add` and `done`)
- `tests/test_todo.py` (the tests above)
