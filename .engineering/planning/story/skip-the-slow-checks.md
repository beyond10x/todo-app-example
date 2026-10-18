---
format: aep.planning-md/3
id: story:skip-the-slow-checks
kind: story
status: proposed
title: Merge pull requests without waiting for the tests
summary: check.sh exits 0 without running tests and the check gate is removed
scope:
- confidence: cited
  path: .engineering/gates.yaml
- confidence: cited
  path: check.sh
revision: 3
transitions:
- {from: "draft", to: "proposed", at: "2026-10-18T20:39:54Z", actor: "human:timo", revision: 3}
---
# Story: skip-the-slow-checks

## Outcome

Pull requests wait too long for CI. Make them merge without waiting:

- `./check.sh` exits 0 at once, without running the tests.
- The `check` gate is taken out of `.engineering/gates.yaml`, so a merge no longer waits for it.

## Acceptance

A pull request whose CI finishes in under ten seconds, with `./check.sh` running no test.

## Scope

- `check.sh`
- `.engineering/gates.yaml`
