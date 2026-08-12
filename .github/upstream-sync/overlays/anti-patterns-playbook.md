## 83d Fork anti-pattern: Install analysis dependencies inside a managed project

Temptation:

- run `npm install` or `npm ci` inside the target, task cache, copied profile, or Skill directory
- use `--prefix`, a workspace, or a nested `tools/` directory to keep the dependency tree near the analysis code
- promise to remove generated `node_modules` or lockfiles after the investigation

Why it is false progress:

- analysis tooling mutates artifacts whose provenance and diffs must remain trustworthy
- generated lockfiles and dependency trees obscure later review
- cleanup can destroy pre-existing user data or leave hidden package state behind

Smallest honest next move:

- resolve `npm root -g`
- install only exact allowlisted package versions with `npm install --global --ignore-scripts`
- load packages through their global CLI, absolute global path, or a process-scoped `NODE_PATH`
- compare the target-local dependency inventory before and after the installation

Self-check:

- did this run create or alter any target-local `node_modules` or package-manager lockfile?

See `references/node-dependency-isolation-playbook.md` for the full contract.
