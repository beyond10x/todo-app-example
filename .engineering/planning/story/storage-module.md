---
format: aep.planning-md/3
id: story:storage-module
kind: story
status: implemented
title: Move load and save into storage.py, with an atomic save
summary: a refactor that keeps every output, exit code and file byte; save renames a new file over the old
scope:
- confidence: cited
  path: storage.py
- confidence: cited
  path: tests/test_storage.py
- confidence: cited
  path: todo.py
revision: 5
transitions:
- {from: "draft", to: "proposed", at: "2026-10-18T20:38:00Z", actor: "human:timo", revision: 3}
- {from: "proposed", to: "active", at: "2026-10-28T06:38:04Z", actor: "human:timo", revision: 4, executor: "agent:takt"}
- {from: "active", to: "implemented", at: "2026-10-28T06:39:43Z", actor: "agent:takt", revision: 5, decided_on: {"recorded":{"test_result":1,"approval":1}}}
---
# Story: storage-module

## Outcome

Reading and writing the todo file move out of `todo.py` into a module of their own, and a write
can no longer leave half a file behind.

- A new module `storage.py` holds `load(path)` and `save(path, items)`. `todo.py` keeps the
  commands and the rendering, imports `load` and `save` from `storage`, and does no file reading,
  writing or JSON of its own.
- `save` is atomic: it writes the whole list to a new file in the same directory and then renames
  it over the old one, so the todo file is always either the old list or the new one. No temporary
  file is left behind.
- Nothing else changes. The file's bytes are the same as before for the same list (two-space
  indent, the same escaping, one newline at the end), and so are its permissions; every command
  prints the same output and messages and exits with the same code; `--file` and `TODO_FILE` work
  as before.
- `tests/test_todo.py` is not changed, and it passes; new tests for `storage.py` go in
  `tests/test_storage.py`.

## Acceptance

`./check.sh` exits 0 with `tests/test_todo.py` unchanged and `tests/test_storage.py` testing
`load` of a missing file, a `save` then `load` round trip, and that `save` leaves no other file in
the directory.

## Scope

- `storage.py` (new: `load`, `save`)
- `todo.py` (imports from `storage`)
- `tests/test_storage.py` (new)
