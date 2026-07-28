# Doctrine Index

Use this file when the target is still broad, the failure mode feels familiar, or you need family-level rules before loading more specific playbooks.

These are transfer rules, not site notes.

## Doctrine 1: Trust the wire, not the page text

- Real request paths beat page hints.
- Real headers beat visible business code.
- Real cookies beat guessed token stories.
- Real response shape beats archived notes.
- A `200 OK` document, loading placeholder, or rendered shell does not prove the business payload lives in the HTML.

## Doctrine 2: The dynamic parameter is not always a signature

The real moving part may be:

- a cookie
- a page-specific header
- a transport envelope
- a server-returned JS bootstrap
- a dynamic font
- a WebAssembly export
- a transport wrapper rewrite
- a response-side decoder
- an account-bound session contract

Do not assume every hard target is solved by hunting a `sign` function.

## Doctrine 3: Fixed-input validation beats naming

If a page helper is called `md5` or `btoa`, prove it on fixed inputs before trusting the name.

Minimum standard for suspicious helpers:

1. pick a fixed input such as `"abc"` or a captured timestamp
2. record browser output
3. record local output
4. compare intermediate values, not just final output

## Doctrine 4: Narrow exceptions stay narrow

If only one page needs a special `User-Agent`, or only one request needs a rotated cookie, encode that exception explicitly.
Do not poison the entire collector with a fake "browser-only" conclusion.

## Doctrine 5: Automation is not an acceptable crutch

When stuck, do more protocol work:

- diff requests
- extract inline scripts
- run bootstrap JS locally
- port helper logic
- instantiate WASM locally
- decode fonts locally

Do not fall back to browser automation as delivery.

## Doctrine 6: Environment mismatch is evidence

When local output and live output disagree, treat the mismatch as evidence:

- compare fixed inputs
- compare side assets
- compare patched helpers
- compare environment branches

Do not hand-wave the mismatch away as "probably browser-only".

## Doctrine 7: Delivery gates outrank convenience

If the only known path still depends on live page context, the task is not done.

- a browser profile is not a protocol artifact
- a hidden refresh click is not a collector
- an unexplained decoder is not acceptable handoff

Keep reversing until the moving parts are local, explicit, and testable.

## Doctrine 8: Public does not mean unsigned

Anonymous pages still have protocol contracts.

- a public list may still require entry-route cookies
- a public route may still require both page-seeded state and request-scoped signer material on the anonymous chain
- a bootstrap endpoint may still return the key, config, or envelope seed
- list visibility does not prove detail or submit visibility
- if a clean anonymous path exists, prove it before contaminating the baseline with logged-in cookies or account state

Treat anonymous access, envelope construction, and permission boundaries as separate questions.

## Doctrine 9: Stateful streams are protocol, not browser magic

If the target only becomes readable after login, pairing, or a warm-up WebSocket exchange, the session transcript is part of the protocol.

- pairing or login bootstrap is not UI fluff
- handshake outputs are protocol artifacts
- heartbeats, ack frames, counters, and reconnect rules are part of the collector

Do not collapse a stateful stream problem into a fake single-request sign story.

## Doctrine 10: Observer effect is real

Some targets get harder after you touch them.

- verifier-gated or behavior-sensitive flows may change once hooks, breakpoints, or monkey patches are installed
- capture one clean baseline request and response before invasive instrumentation
- prefer initiator stacks, request diffs, and narrow boundary hooks before broad global hooks
- if hooking changes the failure mode, treat that as evidence that your tooling is perturbing the target

Do not confuse hook-induced breakage with proof that the site is "browser-only".

## Doctrine 11: Cookie provenance beats cookie superstition

When a cookie gates replay, prove where it came from:

- `Set-Cookie` on a protocol response
- `document.cookie` from page code
- server-returned challenge or bootstrap JS
- redirect wrappers, iframes, workers, or SDK side effects
- a derived header or token that only looks like a cookie problem

Do not hardcode a rotating business cookie before proving its writer and refresh path.

## Doctrine 12: Packet framing and crypto are separate contracts

When a target uses encoded URL params, encoded form bodies, encrypted responses, or environment-bound cookies from the same page family, do not collapse everything into "the AES" or "the sign".

- separate outer packet framing from inner crypto: version byte, field prefix, checksum, custom alphabet, length rules, and state-derived slices may be just as binding as the cipher
- if the signer consumes a `fullUrl` or canonical request string, parameter order, empty fields, and URL encoding are part of the protocol contract
- prove whether URL, body, response, and cookie are four unrelated formats or one shared envelope family with small field-specific variants
- prove whether later requests need current session state bytes, storage state, or challenge output in addition to business plaintext
- if the decrypted response does not start at byte zero, treat prefix stripping and payload anchoring as part of the protocol, not parser cleanup noise
- if a key looks indirect, wrapped, or masked, recover the key-normalization step before blaming the AES mode or padding

Do not call crypto solved until framing, state dependency, and payload extraction are also locally reproducible.

## Doctrine 13: Pagination is a protocol surface

Pagination is not just UI chrome.
It can be part of the protocol contract.

- later pages may switch endpoint families even when page 1 looks static
- one working filename pattern does not prove the whole list uses that pattern
- a visible pager can hide a route cutoff where static pages become `/ui`, Ajax, or another endpoint family
- the collector should prefer live next-page targets over guessed page arithmetic once a route pivot is suspected

Do not call pagination solved until later pages are replayed through the same collector logic.

## Doctrine 14: Raw source can beat parsed DOM

When replay-critical route data lives inside inline handlers or legacy attributes, parsed DOM values may not be canonical.

- unescaped `&`, broken entities, legacy templates, or repair logic can mutate query strings or parameter names
- browser getters, HTML parsers, and beautifiers may normalize away the bytes that actually matter for replay
- when inline attributes carry the next route, freeze the raw tag snippet and compare it against parsed values before trusting either

Do not assume a DOM-decoded attribute is safe to replay just because it looks readable.

## Doctrine 14A: Server-looking field names do not prove server issuance

Names such as `__RequestVerificationToken`, `pageId`, request id, nonce, trace id, session cookie, or fingerprint cookie can be misleading.

- prove who writes the field: page code, wrapper code, bootstrap response, or server
- test tolerance with multiple fresh locally generated values under one known-good session
- session-looking or fingerprint-looking cookie names do not prove `Set-Cookie`; some are locally minted from bootstrap config, fingerprint vectors, or structured UUID variants
- if a locally minted field survives fresh conforming values, preserve the exact structure: inserted prefixes, fixed-width segments, compact JSON order, digest chaining, and key normalization steps
- cross-runtime parity on fixed inputs beats approximate randomness matching
- downgrade the field from hard gate to local filler if replay stays stable across fresh conforming values

Do not spend hours reversing decorative randomness just because the field name sounds important.

## Doctrine 14B: Minted session is not admitted session

A fresh cookie from a public warm-up, current-user, or bootstrap route may prove only that the transport and anonymous shell are alive.

- separate session minting from business admission
- if captured business cookies replay but freshly minted anonymous cookies do not, treat that as evidence that the request contract is solved and the missing piece is session bootstrap or permission state
- do not keep blaming the signer when the failure mode is a route-specific permission denial

Do not confuse "I have a new session" with "this session is authorized for the business method I care about."

## Doctrine 14C: Enumeration and hydration are separate contracts

List, detail, download, and export routes often share one envelope family but differ in identifiers, permission boundaries, and cost.

- solve one route, then probe sibling routes for shared wrapper and decoder reuse
- persist stable ids from the cheap enumeration stage
- persist normalized outputs and raw decoded payloads so later full-text or rule-based backfill does not require rerunning the entire crawl

Do not weld expensive detail hydration into the only path through the collector when a staged design is cheaper and safer.

## Doctrine 15: Embedded runtimes are scalpels, not a second browser

Use an embedded browser-like runtime such as `iv8` only for the narrow part that still needs host semantics.

- first decode and handwrite simple formulas in Python when fixed-input proof is cheap
- route to an embedded runtime only when JS depends on browser-visible host semantics such as `navigator`, `screen`, `location`, DOM lifecycle, timers, `document.cookie`, XHR wrappers, or reflection on native surfaces
- keep the runtime local and narrow: recover one token, cookie, URL suffix, wrapped body, or decoded payload, then hand control back to Python
- if the target still needs full rendering, gestures, canvas noise, or live browser state on every request, the runtime is still an analysis instrument, not proof that delivery is solved

Do not let a local runtime quietly become browser automation with fewer tabs.

## Doctrine 16: Probe chains reveal the missing surface

Modern targets often inspect the environment before any signer runs.

- watch which API is read, enumerated, stringified, or reflected before patching random globals
- treat `Object.keys`, `Reflect.ownKeys`, descriptor reads, `Function.prototype.toString`, `JSON.stringify`, and `document.all` as first-class evidence surfaces
- if a temporary patch is necessary, make its reflected shape match expectations as closely as possible
- use probe evidence to choose between fixing identity semantics, enumeration order, timing, cookie state, or a missing native-looking boundary

Do not collapse silent environment-probe branches into vague "JS obfuscation".

## Doctrine 17: Transport admission is a separate contract

Some targets block the clean baseline before signer, cookie, or decode logic is even visible.

- TLS fingerprint, ALPN, HTTP version, UA family, and route choice can decide whether the application contract is reachable at all
- if stdlib clients die at H2 reset, timeout, or early disconnect while an impersonated transport passes, solve admission first and keep the exception narrow
- one landing route may be challenged while a sibling auth or data route remains usable; verify route-local policy before reversing the wrong fight

Do not blame signer or cookie logic for traffic that never cleared transport admission.

## Doctrine 18: Harvest challenge artifacts at the nearest stable boundary

Do not over-solve a hostile runtime when one explicit artifact is enough.

- if a bootstrap runtime exposes a stable getter after synchronous init, call it before patching every later timer or DOM gap
- if the script self-submits via XHR or fetch, intercept the outgoing body and headers locally instead of emulating every opcode
- preserve scheduler semantics: use execution paths that keep timers, microtasks, and request hooks alive
- patch the smallest faithful boundary and let structural errors propagate; a catch-all that hides recursion or state corruption is sabotage

Do not treat full challenge execution as the goal when one explicit artifact is enough for Python replay.

## Doctrine 19: Server-issued state beats local invention

Before rebuilding anything locally, inventory what the server already hands you.

- list session ids, work factors, asset URLs, answer schema, movement bounds, wrappers, and expiry windows separately from locally computed values
- preserve the scope and lifetime of each issued artifact: page-scoped, request-scoped, route-scoped, or session-scoped
- do not waste time re-deriving locally what the server is already willing to issue unless refresh logic or binding rules force you to

Do not reverse-engineer a server-issued artifact when the real problem is how to carry, refresh, or bind it correctly.

## Doctrine 20: Split verifier targets by failure surface

When a verifier mixes requests, hashes, images, and behavior, force the problem into surfaces:

- protocol surface: endpoint chain, wrappers, session state, payload shape
- compute surface: hashes, PoW, encoding, packing, canonicalization
- perception surface: image preprocessing, transparency, coordinate mapping, match confidence
- behavior surface: trajectories, timing, gesture sidecars, telemetry blobs
- attach an independent proof to each surface: raw responses, fixed-input tests, visual QA, and replay proof

Do not let a perception or behavior failure masquerade as a signer bug.

## Doctrine 21: Weak enforcement is evidence, not absolution

If an empty, stubbed, or simplified field passes once, record the tolerance carefully.

- capture the exact route, environment, and response when the relaxed field is accepted
- keep the field in the protocol model unless repeated evidence proves it is irrelevant for the route family you care about
- assume stricter production routes may enforce the field even if a public or demo route did not

Do not delete a field from the protocol story just because one relaxed path accepted it.

## Doctrine 22: Escalate one rung at a time

When the current proof fails, move up one layer only after you can say:

- what still works
- what exact blind spot remains
- why the heavier layer is the smallest layer that answers that blind spot

Do not jump from "Python parity is incomplete" straight to broad host emulation, and do not jump from "local runtime loads" straight to pagination or scale.

## Doctrine 23: Small facts age better than big summaries

When a target family or upgrade path looks reusable, preserve 5 to 15 minimal verifiable facts:

- route pivots
- field slots
- artifact shapes
- decode order
- session-chain rules
- acceptance checkpoints

Prefer re-checkable structural facts over copied cookies, secrets, or long narratives.

## Doctrine 24: Counterexamples constrain better than slogans

When the same bad move keeps recurring, promote it into a reusable anti-pattern:

- name the tempting shortcut
- explain why it creates false progress
- state the smallest honest next move
- end with one direct self-check

Use `references/anti-patterns-playbook.md` for those counterexamples.
