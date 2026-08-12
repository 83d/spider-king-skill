# Node Dependency Isolation Playbook

Use this file before installing any Node.js dependency for analysis.

## Core rule

Treat the target project, task cache, copied profile, and Skill directory as managed artifacts, never as npm installation workspaces.

- Install analysis dependencies only with exact versions and a global command such as `npm install --global --ignore-scripts <package>@<version>`.
- Resolve and record `npm root -g` before installation.
- Never create or replace a dependency tree inside the target project, task cache, Skill directory, or any of their descendants.
- If a dependency cannot run correctly from the global installation, report that as a blocker instead of falling back to a local install.

This fork rule supersedes upstream guidance that permits task-local dependency installation.

## Pre-install evidence

Before installing anything:

1. resolve and record `npm root -g`
2. verify that the resolved global root is outside every managed project and Skill directory
3. scan the managed project for pre-existing `node_modules`
4. scan for `package-lock.json`, `pnpm-lock.yaml`, and `yarn.lock`
5. fingerprint existing lockfiles and record existing dependency-tree paths as user data

Do not infer that an existing dependency tree or lockfile is disposable.
Do not clean it up unless the user explicitly authorizes that separate action.

## Forbidden installation paths

Do not run dependency-installing forms of these commands from a managed project, task cache, copied profile, Skill checkout, or their descendants:

- `npm install`
- `npm ci`
- `pnpm install`
- `yarn install`

Do not use `--prefix`, workspaces, symlinks, copied package trees, or another indirection to place `node_modules` back under a managed directory.
A nested dependency tree is still managed-project pollution.

## Allowed loading paths

Resolve globally installed packages through one of these narrow mechanisms:

- the package CLI on `PATH`
- an absolute path beneath `npm root -g`
- a process-scoped `NODE_PATH` when a local helper must call `require()`

Do not persist a global loading workaround into the target project unless it is part of the requested collector and remains dependency-tree-free.

## Static AST profile

For `references/profiles/static-ast/`:

1. read the exact dependency versions from its committed `package.json`
2. confirm that every dependency is on the approved package allowlist
3. install those exact versions globally with lifecycle scripts disabled
4. set `NODE_PATH` only for the test or analysis process when module resolution requires it
5. run profile tests without copying the profile or installing beneath it
6. write only analysis outputs to an explicitly approved task path

The committed `package-lock.json` remains a provenance input. Do not regenerate it during analysis.

## Post-install verification

After every installation:

1. run `npm list --global --depth=0 <package>@<version>`
2. rescan managed directories for `node_modules` and package-manager lockfiles
3. compare paths and lockfile fingerprints with the pre-install inventory
4. fail the delivery gate if this run created a local dependency tree or changed a managed lockfile

## Reporting contract

When Node.js tooling was installed, report:

- the resolved global npm root
- the exact pinned packages and versions
- how the packages were loaded
- confirmation that no managed local dependency tree or lockfile was created or changed
- any pre-existing local dependencies that were observed and preserved

## Final rule

Global-only analysis dependencies are a delivery invariant, not a cleanup preference.
