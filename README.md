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

`--priority` is `high`, `normal` or `low`; without it a todo is `normal`. `list` shows the
priority after the box unless it is `normal`. `list --sort priority` lists the `high` todos, then
the `normal`, then the `low`, each keeping its own number, so `done N` and `remove N` act on the
todo that line shows.

Items live in `todo.json` in the working directory, or in the file `--file` or `TODO_FILE` names.
