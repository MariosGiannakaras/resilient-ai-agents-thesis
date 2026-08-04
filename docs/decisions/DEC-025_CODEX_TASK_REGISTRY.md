# DEC-025 — Canonical Resumable Codex Task Registry

**Status:** Accepted  
**Date:** 2026-08-04

## Context

Codex work may span multiple sessions and may be interrupted by model-quota exhaustion or an abrupt session end. Session memory is useful while available, but it is not sufficient as the only record of partially completed work. A long project also needs an explicit checklist so required tasks are not lost between phases.

## Decision

- `docs/context/TASKS.md` is the single canonical concrete execution checklist for the thesis lifecycle.
- Every Codex session reads the task registry before selecting or resuming work.
- Codex uses both available session/conversation memory and durable repository evidence; repository state is the recovery authority when memory is missing or conflicts with committed/working-tree evidence.
- Started unfinished work is marked `IN_PROGRESS` with a resume note containing branch/PR, last validated point, and exact next action.
- Codex inspects branch, commits, working-tree diff, PR state, tests, and the registry after an interruption instead of restarting the task.
- Intermediate branch commits are allowed as recovery checkpoints; coherent work still normally reaches `main` through one squash merge.
- Newly discovered required work receives a stable task ID/dependency in the registry.
- Completed tasks remain checked for auditability.
- Every material PR reviews and updates the registry when it changes task state or discovers/supersedes work.
- `IMPLEMENTATION_ROADMAP.md` remains the phase/dependency explanation; it does not become a competing checklist.

## Consequences

A quota reset or new Codex session can continue from the repository without relying on chat reconstruction. The user should not need to remember which subtask was unfinished or manually maintain an external checklist.

## Alternatives rejected

- rely only on Codex/session memory;
- rely only on a broad roadmap without concrete task completion state;
- create many disconnected task files with no single authoritative registry;
- create one permanent commit in `main` for every tiny checkpoint instead of using branch checkpoints plus squash merges.