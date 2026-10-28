---
format: aep.planning-md/3
id: story:priorities
kind: story
status: active
title: Give a todo a priority and list by it
summary: add --priority high|normal|low; list --sort priority keeps each todo's number; old files load as normal
scope:
- confidence: cited
  path: README.md
- confidence: cited
  path: tests/test_todo.py
- confidence: cited
  path: todo.py
revision: 4
transitions:
- {from: "draft", to: "proposed", at: "2026-10-18T20:35:31Z", actor: "human:timo", revision: 3}
- {from: "proposed", to: "active", at: "2026-10-28T06:32:22Z", actor: "human:timo", revision: 4, executor: "agent:takt"}
---
# Story: priorities

## Outcome

A todo has a priority, `high`, `normal` or `low`, and the list can be read in priority order.

- `./todo.py add TEXT --priority high|normal|low` adds a todo with that priority; without
  `--priority` it is `normal`. Any other value is refused with exit 2 and the file is left
  unchanged.
- `./todo.py list` shows the priority after the box when it is not `normal`:
  `1. [ ] (high) buy milk`, `2. [ ] call home`, `3. [x] (low) water plants`.
- `./todo.py list --sort priority` lists the `high` todos, then the `normal`, then the `low`; within
  one priority they keep their order in the list. Each line keeps the todo's own number, so
  `done N` and `remove N` still act on the todo that line shows.
- A `todo.json` written before this change, whose items carry no priority, keeps working: its
  items are `normal`, and `list` prints them exactly as before.
- `README.md` documents `--priority` and `list --sort priority`.

## Acceptance

`./check.sh` exits 0 with tests that add todos of each priority and check the plain listing, the
sorted listing with each todo's own number, `done N` on a number the sorted listing shows, the
refusal of an unknown priority with the file unchanged, and a file written without priorities
listed as before.

## Scope

- `todo.py` (the `--priority` option of `add`, the `--sort` option of `list`, the rendering)
- `tests/test_todo.py` (the tests above)
- `README.md` (the two options)
