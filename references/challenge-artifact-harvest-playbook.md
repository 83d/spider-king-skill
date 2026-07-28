# Challenge Artifact Harvest Playbook

Use this playbook when a hostile runtime already produces the decisive artifact locally, and the job is to harvest it without turning the solution into browser automation.

## Route here when

- a bootstrap or challenge script exposes a stable getter or object method after initialization
- a local runtime self-issues XHR or fetch with the real wrapped body, binary payload, or decisive headers
- the browser or local runtime already emits the final encrypted body or decisive header set even though a perfect offline rebuild is still incomplete
- a security SDK globally hooks `fetch`, XHR, or another request primitive, and one minimal synthetic request can reveal which signer params, cookies, or headers it injects automatically
- later timer or DOM errors appear, but the needed artifact may already exist before full DOM parity
- blocking `vm` execution deadlocks while DOM or script execution preserves timers, microtasks, or request hooks
- patching the code-generation boundary looks cheaper than filling dozens of missing DOM APIs
- a top-level SDK init dies inside axios, fetch, adapter glue, telemetry upload, or framework orchestration, but a lower serializer or packer may still be callable directly

## Core idea

Recover the artifact at the nearest stable boundary.

Prefer intercept-and-forward when the runtime already produces the decisive artifact more cheaply than full rebuild.

Typical stable boundaries are:

- an exposed getter after synchronous init
- the outgoing XHR or fetch call
- one synthetic request sent through a globally hooked transport primitive
- a lower-level serializer, signer, packer, or export below a failing outer facade
- a cleaner alternate route that makes full challenge execution unnecessary

## Fast execution path

1. Classify the artifact path first.
   Choose one:
   - exposed getter
   - intercepted XHR or fetch egress
   - lower primitive below a broken facade
   - alternate-route bypass

2. Preserve scheduler semantics.
   When timers, microtasks, lifecycle, or self-issued requests matter, use an execution path that keeps them alive.
   Prefer DOM or script insertion style execution over blocking `vm` evaluation for these cases.

3. Patch the smallest faithful boundary.
   Good patch targets:
   - one missing environment read
   - one code-generation boundary
   - one local request hook
   - one narrow success stub

4. Harvest the artifact.
   Examples:
   - getter return value
   - outgoing request body
   - decisive headers
   - outbound `Cookie` header
   - derived cookie
   - final token

5. Hand control back to Python.
   Let Python perform the real HTTP replay, retries, parsing, and persistence.

6. Retry with fresh bootstrap when necessary.
   If bundles are version-randomized, reacquire bootstrap assets instead of assuming one patched script stays stable forever.

## High-value checks

- whether the artifact exists before noisy timer callbacks finish
- whether the runtime needs script insertion or page bootstrap instead of blocking eval
- whether the self-issued request can be captured locally without touching the live site
- whether one minimal synthetic request through the hook already proves the signer injection boundary, leaving only business payload modeling to local code
- whether one already-produced final body or header set is enough for Python replay, making full inner-crypto parity optional for the first stable delivery
- whether the runtime already emits the full replayable `Cookie` header for a challenged document route, making individual cookie reverse work optional for the first stable delivery
- whether the runtime exposes a wire-shaped egress record that is more authoritative than `document.cookie`, a jar snapshot, or an intermediate helper value
- whether the outer SDK path fails only in transport adapters or telemetry glue while a lower module already exposes the decisive blob builder
- whether the runtime only needs a minimal fake success response to keep progressing
- whether a recoverable patch should catch one exact error class while structural failures still propagate

## Common traps

- trying to finish every timer callback when one getter already returns the artifact
- patching every missing DOM hole instead of intercepting the outgoing request
- reverse-engineering a whole signer before proving what a globally hooked request primitive injects for free
- rebuilding every inner crypto stage after the runtime already emits a replayable final body or decisive headers
- reverse-engineering every individual cookie writer before checking whether the runtime already exposes the authoritative replay `Cookie` header
- trusting stored cookie state over an observed outbound `Cookie` header when the two diverge
- discarding the whole SDK route because the outer init path failed before checking for a usable lower serializer or packer
- using catch-all error swallowing that hides recursion, stack overflow, or state corruption
- letting the local runtime issue real business HTTP when only local mutation evidence was needed
- keeping the challenge runtime as a hidden dependency after the artifact shape is already understood

## Delivery guidance

Preferred shape:

1. Python request or bootstrap
2. local runtime harvest step
3. explicit artifact extraction
4. Python replay

Not:

1. Python orchestrates a hidden browser replacement

## Minimal handoff notes

Report these items explicitly:

- which artifact path won: getter, egress, or bypass
- whether an outer facade was skipped in favor of a lower primitive
- which scheduler assumptions mattered
- which narrow patch was required, if any
- which artifact was extracted locally
- whether the extracted artifact was one cookie value, a composed outbound `Cookie` header, a token, or a wrapped body
- whether a synthetic request through a hooked transport primitive exposed the signer boundary
- why intercept-and-forward was cheaper or safer than full rebuild at the chosen boundary
- how Python consumed that artifact in the final replay
