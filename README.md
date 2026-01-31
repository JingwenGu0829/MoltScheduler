# MoltScheduler (template)

A **file-backed, agent-assisted daily planning system**.

This repo is intentionally **code-light** in v1: the “product” is a clean data model + an operating procedure an agent can follow.

## What it does
- You maintain a small set of canonical files (`profile.yaml`, `tasks.yaml`).
- An agent reads them and pushes a daily plan (time-blocked, estimated durations, top priorities).
- The user sends a short end-of-day check-in; the agent updates the task state.

## What it is not (yet)
- Not a calendar replacement.
- Not a full GUI.

## Quick start
1. Copy `template/` to your private workspace.
2. Edit:
   - `planner/profile.yaml`
   - `planner/tasks.yaml`
3. Give your agent the instructions in **README_AGENT.md**.

## Philosophy
- **Truth vs outputs**: keep one canonical source of truth, and regenerate outputs.
- **Tidy by default**: keep only `latest/` artifacts unless you explicitly want history.

## License
MIT (see `LICENSE`).
