# todo-app-example

A scratch repository for takt's live trials. `README.md` is for people.

## Commands

```
./check.sh           # the tests
./docs-check.sh      # README.md shows every command of todo.py
```

The gate (`.engineering/gates.yaml`) and CI run both scripts.

## Rules

- Python 3 standard library only.
- `.engineering/planning` is the AEP planning store; change it only through `aep plan artifact`
  verbs.
- Every commit, push, pull request and merge goes through the bot route (`b10x-gates bot`,
  `b10x-gates api`).
- This repository's history is expendable: trial branches, pull requests and merges are its
  purpose.
