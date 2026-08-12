# Static AST Profile

Use this profile after a supplied JavaScript asset is already an evidence artifact and the next goal is to make a signer, serializer, or decoder boundary readable.

## Safety contract

- Parse and rewrite source structurally; never execute the target source.
- Keep the original and every intermediate file in the task project's `js_reverse_cache/tasks/<task-id>/` directory.
- Use only the generic, conservative pipeline. Site or family adapters require independent fixtures before they can be added.
- Treat `eval`, `Function`, WebAssembly, host-object reads, and opaque decoder calls as observations that require the `env-patch` or another local-runtime route.
- `node:vm` is not an isolation boundary. This profile does not use it.
- Reports contain file basenames, hashes, counts, and bounded error metadata, not source text, tokens, cookies, or environment values.
- The input path must not reuse any generated filename listed below. Invalid UTF-8 stops before parsing; `00_source.js` and `final.js` retain the exact input bytes.

## Entry conditions

For structure-only detection and conservative restoration, the supplied input file plus a bounded inspection goal is sufficient. A fixed request or runtime sample becomes mandatory before claiming algorithm equivalence, evaluating a recovered boundary, executing target code, or escalating to a dynamic route. If the entry or call chain is required by the user's goal but remains unknown, return to the Spider core loop before broad deobfuscation.

## Usage

The Babel dependency graph is pinned in `package.json` and `package-lock.json`. In this fork, never install dependencies in the Skill, a copied profile, a task cache, or the target project.

After dependency-installation authority is confirmed:

1. Inventory pre-existing `node_modules` and package-manager lockfiles beneath every managed project path.
2. Resolve `npm root -g` and verify that it is outside the target project, task cache, and Skill directory.
3. Read the exact allowlisted Babel versions from this profile's `package.json`.
4. Install those exact versions with `npm install --global --ignore-scripts`.
5. Verify them with `npm list --global --depth=0`.
6. Run the profile directly from this read-only directory, using a process-scoped `NODE_PATH` set to `npm root -g` if module resolution requires it.
7. Write pipeline output only to the approved task output directory, then confirm that the managed dependency inventory is unchanged.

Run the pipeline in this shape:

```text
NODE_PATH="$(npm root -g)" node references/profiles/static-ast/scripts/run-pipeline.js <input.js> <task-output-dir> [hint]
```

The environment-variable syntax may be adapted to the current shell, but it must remain process-scoped. Do not regenerate the committed lockfile during analysis.

## Supported static observations

- string-array and decoder-shaped structures
- dispatcher-shaped objects
- loop/switch control-flow flattening
- opcode-style literal comparisons
- computed member access
- `_0x`-style identifiers
- dynamic execution and WebAssembly markers

Detection is structural and intentionally does not select a site-specific adapter. Ambiguous evidence always stays on `generic-static-safe`.

## Rewrite scope

The first rewrite pass only:

1. converts a computed member with a valid string identifier (`obj['run']`) to a normal member (`obj.run`)
2. removes an `if` whose test is already a Boolean literal while preserving the selected statement block; branches containing `var` or function declarations are retained to preserve hoisting semantics

No calls are evaluated. No aliases, string tables, control-flow state machines, getters, proxies, or host-dependent expressions are folded. Add a new rewrite only with a fixture that proves both positive behavior and a negative boundary.

## Upgrade path

If the report marks `dynamic_execution`, `wasm`, or host-dependent code, stop the static route and hand off to `references/profiles/env-patch/index.md`, `references/offline-inline-deob-playbook.md`, or a dedicated runtime skill. The final collector still remains Python-owned.
