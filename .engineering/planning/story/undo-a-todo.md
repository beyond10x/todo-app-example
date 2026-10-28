---
format: aep.planning-md/3
id: story:undo-a-todo
kind: story
status: active
title: Undo a done todo by its number
summary: todo.py undo N marks item N not done; an unknown number is refused
scope:
- confidence: cited
  path: tests/test_todo.py
- confidence: cited
  path: todo.py
revision: 4
transitions:
- {from: "draft", to: "proposed", at: "2026-10-18T20:39:19Z", actor: "human:timo", revision: 3}
- {from: "proposed", to: "active", at: "2026-10-28T06:40:40Z", actor: "human:timo", revision: 4, executor: "agent:takt"}
---
# Story: undo-a-todo

## Outcome

`./todo.py undo N` marks todo number N as not done again. Undoing a todo that is not done
changes nothing and exits 0. A number that names no todo is refused with exit 1, the message
`todo: there is no todo N` on standard error, and the file left unchanged.

## Acceptance

Both gates of `.engineering/gates.yaml` pass, with `./check.sh` running tests that mark todo 2 of
three done, undo it and list it as `2. [ ] <second>`, that undo a todo that is not done, and that
show `undo 0` and `undo 4` on a list of three exit 1 with the file unchanged.

## Scope

- `todo.py` (an `undo` command beside `done`)
- `tests/test_todo.py` (the tests above)
