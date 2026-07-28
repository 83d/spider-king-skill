---
name: spider-king
description: Reverse hostile web clients into pure-protocol collectors with Python-first delivery. Always begin each new target with combined `chrome-devtools` and `js-reverse` analysis, then deliver a browser-free Python collector plus a local JS parameter-restoration helper only when needed. Use when the user provides a target page URL, API URL, JS snippet, sign or token sample, cookie sample, packet capture, or asks to build or repair a collector for sites protected by sign, token, cookie, WebSocket, GraphQL, protobuf, response encryption, browser fingerprint checks, WebAssembly signers, challenge bootstraps, or dynamic-font response obfuscation.
---

# Spider King

## Role

Turn hostile web clients into stable protocol collectors.

This skill is not a browser automation skill.
This skill is a protocol recovery skill.

Default posture:

1. start every new target with `chrome-devtools` plus `js-reverse` evidence gathering
2. find the real request
3. identify the true changing state
4. rebuild that state offline
5. deliver a browser-free Python collector, plus a local JS parameter helper only when truly needed

## Non-Negotiables

- Final delivery must be pure protocol: raw HTTP plus local signer, local decoder, or local bootstrap helper only.
- Every new target must be analyzed first with both `chrome-devtools` and `js-reverse` before writing the final collector.
- Do not ship Playwright, Selenium, CDP page-driving, or submit-through-browser flows as the solution.
- Final delivery must run fully outside the browser: Python crawler scripts for collection, plus a local JS helper only for parameter, sign, token, or cookie reconstruction when Python porting is not yet the safest choice.
- Prefer Python for the collector and orchestration.
- Only keep a tiny isolated JS or WASM helper when a verified Python port is not yet cheaper, safer, or faster to maintain.
- Any JS helper must run locally without page driving, `document`, `window`, manual clicks, browser profiles, or hidden browser dependencies.
- If browser tooling is used at all, use it only for recon and evidence gathering, never as a hidden dependency in the final collector.
- Automation is forbidden as the final answer, forbidden as a fallback answer, and forbidden as a disguised "temporary" delivery path.
- Recover one stable request before scaling pagination, concurrency, or submission.
- Every conclusion must be backed by artifacts: request samples, fixed-input helper outputs, cookies, headers, and replay proof.
- Stay in one execution loop until you reach protocol delivery or hit a real external blocker.

## Startup Gate

Before any deep tool use on a fresh target, emit a short startup gate and fill it with current evidence.

Required checks:

1. environment and tool sanity
   - run `scripts/check_reverse_env.py` when local execution is available
   - confirm whether both `chrome-devtools` and `js-reverse` are usable
   - if one tool is blocked, report the blocker before pretending the target is understood
2. family triage
   - classify the target first as `signer-gated`, `verifier-gated`, `decode-gated`, or `session-gated`
   - add the secondary tag `transport-gated` when TLS, ALPN, UA, HTTP version, or route-local admission blocks the clean baseline before application semantics are visible
   - read `references/startup-triage-playbook.md` before loading giant bundles
   - if the next move would widen the runtime, patch surface, or transport profile, read `references/escalation-ladder-playbook.md` before jumping layers
   - if a rotating cookie appears important, read `references/cookie-provenance-playbook.md` before hardcoding anything
3. delivery intent
   - state the intended final shape: pure Python, Python plus tiny JS helper, Python plus tiny WASM helper, or Python plus local bootstrap executor
   - explicitly reject browser-backed fetches, browser profiles, and automation-driven replay as the final answer

Rule:

- if the startup gate is incomplete, the target is not yet understood
- if the classification changes after new evidence, restate the gate instead of silently drifting

## What This Skill Optimizes For

- protocol-first reverse engineering
- Python-first delivery
- offline reproduction of dynamic state
- reusable collectors instead of one-off lucky requests
- generic methodology that transfers across similar targets

## Knowledge Modules

Keep this entry file lean and route to focused references as soon as the symptom is clear.

Load only the module you need:

- `references/doctrine-index.md` for family-level debugging rules and protocol posture
- `references/symptom-heuristics.md` when the target still smells broad and you need fast family matching
- `references/pattern-atlas.md` when the target already fits a recurring pattern and you want the shortest proven first move
- `references/workflow-overview.md` for the shortest end-to-end execution map

The `references/` directory is the real knowledge base.
The entry `SKILL.md` should route, not restate every doctrine in full.

## Reference Layout

- root-level playbooks own reusable workflows
- doctrine and heuristics live in dedicated routing references
- site-specific lessons should be abstracted back into generic references, not left in the entry file

## Minimal Intake

Start immediately if the user already provided enough evidence.

Otherwise ask only for the smallest missing set:

- target page URL, or
- target API URL, or
- site homepage plus collection goal, or
- captured request sample, or
- JS snippet, obfuscated bundle, cookie sample, sign sample, or packet capture

Only ask follow-ups that change implementation:

- target fields
- scope: single page, pagination, category, date range, or whole site
- output format: JSON, CSV, Excel, database, or API sink
- whether login is required
- whether incremental sync, dedupe, or resume is required

## Universal Reverse Loop

### Phase 0: Fingerprint before deep work

Classify the target before reading giant bundles:

- decoy endpoint vs real endpoint
- transport-pre-gated baseline vs application-visible baseline
- wrapper rewrite vs visible param
- patched helper vs standard helper
- simple decodable formula vs browser-host-bound bootstrap vs true interaction dependency
- exposed getter vs self-submitting challenge runtime vs alternate-route bypass
- signer-gated vs verifier-gated vs decode-gated vs session-gated
- bootstrap asset vs direct data API
- plain JSON vs GraphQL vs WebSocket vs binary envelope
- single-shot replay vs stateful session with pairing, auth, or warm-up frames
- direct response vs encoded response vs glyph-mapped response
- page-specific exception vs whole-flow exception
- session-bound vs anonymous
- clean-baseline-first vs trace-first vs decode-first vs transcript-first
- rotating-cookie provenance known vs unknown
- JSVMP or heavy obfuscation vs normal packed bundle

Goal:

- choose the smallest next proof and the least destructive first instrument, not the biggest code dump

### Phase 1: Identify the true request path

- follow redirects
- inspect wrapper pages and compatibility pages
- separate visible page routes from real wire routes
- map bootstrap requests, list requests, detail requests, submission requests, and risk-control requests
- map pagination route transitions separately from the first-page route
- confirm whether later pages pivot from static filenames to `/ui`, Ajax, or another endpoint family
- detect whether one endpoint serves both bootstrap and final data in separate phases
- test whether the challenged document route itself is the real replay target after bootstrap, rather than assuming a separate XHR or API exists

Deliverable for this phase:

- one confirmed request that is definitely on the real business path

### Phase 2: Classify the moving parts

For the real request, classify each changing field:

- static header
- rotating header
- static cookie
- rotating cookie
- timestamp
- nonce or random fragment
- signed body or query
- transport envelope, operation name, or message type
- compressed or binary response format
- decode key, glyph map, or response-side transform
- encrypted response
- page-specific exception
- account-bound session dependency
- bootstrap artifact dependency
- browser-host semantic dependency such as lifecycle, timer, cookie, parser-order, or probe-surface state
- login or pairing bootstrap artifact
- session key schedule or exported secret material
- heartbeat, ack, counter, or message-tag state
- media-key derivation or side-channel download secret

Goal:

- separate what must be reproduced from what is just noise

### Phase 3: Locate the canonical mutation point

Look in this order:

1. transport wrappers such as `$.ajaxSetup`, `beforeSend`, fetch wrappers, interceptors
2. bootstrap side scripts and inline payloads
3. page-exposed helper functions
4. WebAssembly exports
5. server-returned JS challenges
6. response-side refresh fields that seed the next request
7. handshake transcripts, frame serializers, binary node encoders, protobuf parsers, or session key schedules

Rule:

- the canonical mutation point is where the wire payload actually changes, not where the business code first creates a placeholder

### Phase 4: Rebuild the moving parts offline

Choose the cheapest valid offline shape:

1. pure Python
2. Python plus isolated JS signer
3. Python plus minimal local JS or WASM helper
4. Python plus local challenge bootstrap executor
5. Python plus local font decoder

Never add browser automation to the final path.
Escalate only one rung at a time.
Before moving to a heavier runtime, broader patch surface, or transport exception, record what proof failed at the current rung and why the next rung is the smallest honest move.
See `references/escalation-ladder-playbook.md` when the next escalation is unclear.

### Phase 5: Prove repeatability

Do not call it solved until:

- the same logic succeeds at least 2 to 3 times
- pagination advances correctly
- final fields are complete
- dynamic state regenerates correctly
- account-bound constraints are documented

## Pattern Matching

When the target already resembles a recurring case, read `references/pattern-atlas.md` instead of re-deriving the first move from scratch.

That file owns the short-form patterns for:

- decoy endpoints and wrapper mutation
- bootstrap-first flows and challenge-generated state
- decode and structured transport problems
- pagination pivots and raw-source traps
- transport pre-gates, embedded runtimes, and harvest-first runtimes

## Tool Priorities

Every fresh target must start with a startup gate, then a lightweight paired analysis pass:

1. run `scripts/check_reverse_env.py` when local execution is available
2. use `chrome-devtools` for page state, redirects, visible flow, and one first-pass network view
3. use `js-reverse` for initiator stacks, source search, wrapper tracing, and first mutation hypotheses
4. diff captured requests before rebuilding anything
5. verify helpers on fixed inputs
6. move to offline execution and local replay only after the first pass is evidence-backed

Do not skip either tool on a fresh target unless a real blocker makes one unavailable, and report that blocker explicitly.

Use deeper browser interaction only when you must observe one redirect chain, sample one fixed helper output, or survive an anti-debug path during analysis.
The final collector must still be browser-free.

## Bundled Scripts

Use local helper scripts when they shorten repeatable work:

- `scripts/scaffold_reverse_project.py` for protocol-first Python scaffolding
- `scripts/check_reverse_env.py` for local environment sanity
- `scripts/crypto_fingerprint.py` for suspicious digest or custom-alphabet classification
- `scripts/protocol_diff.py` for request and response delta analysis

## Reproduction Decision Tree

Choose delivery in this order:

1. pure Python if all logic is restored
2. Python plus minimal JS helper if the signer is exact in JS and porting now would add risk
3. Python plus local WASM helper if the request param comes from a tiny export
4. Python plus local embedded runtime or bootstrap executor when environment-sensitive JS needs DOM, timer, cookie, or XHR semantics without a real browser
5. stop and keep reversing if the only remaining path is browser automation

Never choose:

- browser-backed replay as final delivery
- "works only in my browser profile" as acceptable handoff
- page-driving submission as the answer when protocol submission exists

## Implementation Rules

Keep the final collector easy to reason about:

- split headers, cookies, signer logic, parsing, retries, output, and persistence by concern
- keep fixed-input self-checks before live traffic
- prefer Python first; keep JS or WASM only as a narrow local helper
- keep live HTTP in Python even when a local runtime helps with bootstrap or parameter recovery
- keep final helpers self-contained and free of browser-backed imports
- keep stable scaffolding separate from fresh task-local captures and runtime blobs
- catalog server-issued artifacts separately from locally computed ones
- prove cookie provenance before caching rotating cookies
- keep bootstrap-heavy traces on one session chain until reuse is explicitly proven
- prove one fresh live replay on one session chain before broad environment patching, pagination scaling, or runtime-shrink work on verifier-gated targets
- treat wire-shaped egress records as replay authority when they differ from intermediate getters or jar state
- regenerate request-shaped artifacts per request when page, body, referer, keyword, or timestamp can change them
- use `page.load`-style bootstrap only when lifecycle, timers, or request hooks matter
- compare structural metrics when local runtime output diverges from live output
- inspect native-surface probes before cargo-cult filling globals
- test transport admission separately when traffic dies before meaningful app semantics appear
- preserve wrapper framing, JSONP, odd delimiters, and exact serialization rules explicitly
- distinguish browser-free from runtime-free delivery explicitly whenever an embedded host remains in the loop
- save raw request and response samples early
- fail loudly on unexpected response shapes

## Verification Gates

Do not mark complete until the relevant gates pass:

- startup gate completed and updated when the target family changes
- real request path and moving parts proven
- first-pass `chrome-devtools` and `js-reverse` evidence captured
- clean baseline captured before invasive tooling when observer effect matters
- helpers or decoders verified on fixed inputs
- server-issued artifacts cataloged before local reimplementation
- cookie provenance, slot placement, and session-chain integrity proven when they matter
- transport, decode, envelope, or stream rules documented when present
- pagination, route pivots, and permission boundaries documented when present
- local helper load success, lower error volume, or browser-shaped artifacts do not count without repeated live replay
- live replay succeeds repeatedly
- final Python collector runs without browser automation or browser profiles
- if an embedded runtime still remains, the handoff states whether the result is browser-free only or fully runtime-free
- final JS or WASM helper, if any, stays local and narrow
- output is saved in the requested format

## Output Contract

After each meaningful phase, emit short structured reporting instead of vague prose.

Always return:

- which target family won the startup triage and why
- what `chrome-devtools` proved about the site flow
- what `js-reverse` proved about the mutation logic
- what the real endpoint is
- what the real moving parts are
- whether observer-effect risk showed up and how it was controlled
- what the cookie provenance is when cookies mattered
- what looked server-issued but was actually local filler, if anything
- what was misleading
- what was verified with fixed inputs
- what the final protocol path is
- whether sibling list, detail, download, or export routes shared one envelope family
- how the Python collector and JS helper are split
- confirmation that the final runtime is fully browser-free
- when the target family looks reusable, which 5 to 15 minimal verifiable facts should be preserved for the next upgrade or sibling target
- where the collector and sample output were saved
- what still looks unstable, if anything

Use the headings from `references/report-templates.md` when possible.

## Skill Validation

When modifying this skill, validate against:

- `references/official-self-test-task-suite.md`
- `references/skill-maintenance.md`

Do not call the edit complete until the route stays protocol-first, the entry `SKILL.md` stays lean enough to route instead of restating everything, and the chosen references still match the real symptom.

## Anti-Patterns

When a shortcut looks easier than the next proof, read `references/anti-patterns-playbook.md`.
That file owns failure-shaped counterexamples and self-checks; this section stays as the short deny-list.

- Do not ask the user to manually inspect giant bundles if tooling can inspect them.
- Do not skip `chrome-devtools` or `js-reverse` on a fresh target unless you report a real blocker.
- Do not jump straight to Selenium or Playwright when a direct API exists.
- Do not install broad hooks before capturing a clean baseline on verifier-gated or behavior-sensitive targets.
- Do not confuse business-layer params with wire-layer params.
- Do not trust helper names without fixed-input proof.
- Do not call browser-only behavior before checking page-specific headers or cookies.
- Do not hardcode rotating cookies before proving who writes them and how they refresh.
- Do not bury every concern in one `main.py`.
- Do not stop after one lucky success.
- Do not leave a fresh session chain to chase offline patches before one minimal live replay path is proven.
- Do not mistake helper load success, lower error volume, or plausible cookie shape for protocol completion.
- Do not ship a browser automation script when the task is protocol-recoverable.
- Do not hide automation behind words like "temporary collector" or "reliable fallback".
- Do not leave final JS helpers coupled to `window`, `document`, browser storage, or manual browser state when they can be made local and deterministic.

## Reference Router

Start here:

- `references/startup-triage-playbook.md` for fresh targets
- `references/workflow-overview.md` for the shortest end-to-end map
- `references/anti-patterns-playbook.md` when a shortcut feels faster than evidence
- `references/escalation-ladder-playbook.md` when a partial proof tempts you to jump to a heavier layer
- `references/tool-playbook.md` for tool choice and next-step routing
- `references/report-templates.md` for reporting and handoff shape

Request path and wrapper mutation:

- `references/decoy-and-real-request-playbook.md`
- `references/transport-wrapper-playbook.md`
- `references/patched-helper-playbook.md`
- `references/crypto-patterns.md`
- `references/obfuscation-guide.md`

Cookies, bootstrap state, and sessions:

- `references/cookie-provenance-playbook.md`
- `references/session-contract-playbook.md`
- `references/public-bootstrap-envelope-playbook.md`
- `references/challenge-state-envelope-playbook.md`
- `references/server-js-cookie-bootstrap-playbook.md`
- `references/side-asset-bootstrap-playbook.md`

Host-bound runtime and local execution:

- `references/environment-patch-playbook.md`
- `references/embedded-browser-runtime-playbook.md`
- `references/iv8-runtime-cheatsheet.md`
- `references/challenge-artifact-harvest-playbook.md`
- `references/hook-techniques.md`
- `references/anti-debug-playbook.md`
- `references/env-diff-playbook.md`

Transport, decode, and structured payloads:

- `references/transport-pre-gate-playbook.md`
- `references/response-decode-playbook.md`
- `references/structured-transport-playbook.md`
- `references/offline-inline-deob-playbook.md`
- `references/jsvmp-analysis-playbook.md`

Verifiers, pagination, and narrow exceptions:

- `references/verifier-replay-playbook.md`
- `references/pagination-route-pivot-playbook.md`
- `references/page-specific-exception-playbook.md`
- `references/troubleshooting-playbook.md`

Stateful streams and long-lived sessions:

- `references/stateful-stream-e2ee-playbook.md`

Maintaining this skill:

- `references/anti-patterns-playbook.md`
- `references/doctrine-index.md`
- `references/minimal-verifiable-facts-playbook.md`
- `references/symptom-heuristics.md`
- `references/pattern-atlas.md`
- `references/skill-maintenance.md`
- `references/official-self-test-task-suite.md`

## Maintaining This Skill

When a job teaches something reusable:

- put the detailed rule in the most specific owning reference
- add or update a generic doctrine only when it transfers across many future jobs
- keep the entry `SKILL.md` as a router and execution guide, not a full knowledge dump
- prefer new generic references over site notes
- preserve 5 to 15 minimal verifiable facts when a target family, upgrade path, or sibling route looks likely to recur

## Bottom Line

This skill should teach one habit above all:

When the site looks "browser-only", do not panic and do not automate.
First ask:

1. what is the real request
2. what is the real changing state
3. can that state be rebuilt locally

Most similar targets collapse once those three questions are answered honestly.
