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
