# Node Dependency Isolation Playbook

Use this file before installing any Node.js dependency for analysis.

## Core rule

Treat the target project as an artifact under analysis, never as the npm installation workspace.

- Install analysis dependencies only with a pinned global command such as `npm install --global <package>@<version>`.
- Never create or replace a dependency tree inside the target project or any of its subdirectories.
- If a dependency cannot run correctly from the global installation, report that as a blocker instead of falling back to a local install.

## Pre-install evidence

Before installing anything:

1. resolve and record `npm root -g`
2. scan the target project for pre-existing `node_modules`
3. scan for `package-lock.json`, `pnpm-lock.yaml`, and `yarn.lock`
4. record pre-existing results as user data and leave them untouched

Do not infer that an existing dependency tree is disposable.
Do not clean it up unless the user explicitly authorizes that separate action.

## Forbidden installation paths

Do not run any of these from the target project, `tools/`, a checked-out helper source, or another target subdirectory:

- `npm install`
- `npm i`
- `pnpm install`
- `yarn install`

Do not use `--prefix`, workspaces, symlinks, copied package trees, or another indirection to place `node_modules` back under the target project.
A nested dependency tree is still target pollution.

## Allowed loading paths

Resolve globally installed packages through one of these narrow mechanisms:

- the package CLI on `PATH`
- an absolute path beneath `npm root -g`
- a process-scoped `NODE_PATH` when a local helper must call `require()`

Do not persist a global loading workaround into the target project unless it is part of the requested collector and remains dependency-tree-free.

## Post-install verification

After every installation:

1. run `npm list --global --depth=0 <package>`
2. rescan the target project for `node_modules` and package-manager lockfiles
3. compare the result with the pre-install inventory
4. fail the delivery gate if this run created a target-local dependency tree or lockfile

## Reporting contract

When Node.js tooling was installed, report:

- the resolved global npm root
- the exact pinned package and version
- how the package was loaded
- confirmation that no target-local dependency tree or lockfile was created
- any pre-existing target-local dependencies that were observed and preserved

## Final rule

Global-only analysis dependencies are a delivery invariant, not a cleanup preference.
