# todo-app-example

A small todo list in one Python file, with no dependencies. It is the scratch repository
[takt](https://github.com/beyond10x/takt) runs its live trials against: a planning store with
ready stories, a gate, CI on every pull request, and merges through the bot route.

```
./todo.py add "buy milk"
./todo.py add "call home" --priority high
./todo.py list
./todo.py list --sort priority
./todo.py done 1
./check.sh            # the tests
```

`add --priority` accepts `high`, `normal`, or `low` (default: `normal`).
`list --sort priority` shows todos in high-to-low priority order while keeping their original todo
numbers, so `done N` and `remove N` continue to refer to the number shown. Normal-priority todos
are displayed without a priority label.

`edit N TEXT` replaces a todo's text in place, preserving its number, done mark and priority.
For example, `./todo.py edit 1 "buy oat milk"`. Surrounding whitespace is stripped, as with `add`.
Empty text after stripping or a number naming no todo is refused with exit 1, leaving the file unchanged.

Items live in `todo.json` in the working directory, or in the file `--file` or `TODO_FILE` names.
