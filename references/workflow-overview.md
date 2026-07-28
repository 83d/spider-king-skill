# Workflow Overview

Use this file as the shortest end-to-end map for a reverse job.

## Startup gate

Before deep work:

- check local tool sanity
- classify the target as `signer-gated`, `verifier-gated`, `decode-gated`, or `session-gated`
- state the smallest acceptable browser-free delivery shape
- distinguish "browser-free now" from "runtime-free goal" when an embedded host is being considered
- if the next move would widen the runtime, patch surface, or transport profile, read `references/escalation-ladder-playbook.md` first

## Phase 0: Fingerprint the target

Before touching code, classify the target:

- decoy endpoint vs real endpoint
- wrapper rewrite vs visible param
- patched helper vs standard helper
- signer-gated vs verifier-gated vs decode-gated vs session-gated
- session-bound vs anonymous
- bootstrap asset vs direct data API
- one-page exception vs whole-flow exception
- clean-baseline-first vs trace-first vs decode-first vs transcript-first
- JSVMP or heavy obfuscation vs normal packed bundle

## Phase 1: Prove the real request

- capture the request that returns useful data
- record its initiator
- record exact query, body, headers, cookies, and response shape
- store fresh captures in a task-local cache separate from stable helper code or user-maintained fixtures

## Phase 2: Isolate the moving state

Treat each moving part separately:

- timestamp
- random fragment
- rotating cookie
- transport wrapper field
- page-specific header
- session contract
- bootstrap output
- cookie provenance

## Phase 3: Rebuild offline

Choose the cheapest valid path:

1. pure Python
2. Python plus tiny JS helper
3. Python plus tiny WASM helper
4. Python plus local bootstrap executor

For verifier-gated or challenge-bootstrap targets, do not widen host patching or runtime-removal work until one fresh single-page live replay succeeds on one session chain.
Climb one rung at a time and record why the lighter rung failed before escalating.
Use `references/escalation-ladder-playbook.md` when the next move is debatable.

When captured target code, HTML, or runtime blobs are volatile, generate temporary local runners from the fresh cache instead of overwriting stable scaffolding by default.

## Phase 4: Verify repeatability

- helper outputs match fixed test vectors
- local helper load success, fewer exceptions, or browser-shaped artifacts are not counted as success unless the real request replays repeatedly
- verifier-gated targets keep working after you remove broad hooks
- page 1 replays at least twice
- single-page live replay is proven before pagination scaling or runtime shrink work
- pagination or cursor works
- known exceptions are encoded narrowly
- bootstrap-heavy targets keep one session chain intact unless cross-session reuse is explicitly proven

## Phase 5: Deliver

- protocol-only collector
- saved samples
- clear notes about headers, cookies, and instability
- when the family is likely to recur, preserve 5 to 15 minimal verifiable facts
- use `references/minimal-verifiable-facts-playbook.md` to keep those facts structural and re-checkable
