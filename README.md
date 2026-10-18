# todo-app-example

A small todo list in one Python file, with no dependencies. It is the scratch repository
[takt](https://github.com/beyond10x/takt) runs its live trials against: a planning store with
ready stories, a gate, CI on every pull request, and merges through the bot route.

```
./todo.py add "buy milk"
./todo.py list
./todo.py done 1
./check.sh            # the tests
```

Items live in `todo.json` in the working directory, or in the file `--file` or `TODO_FILE` names.
