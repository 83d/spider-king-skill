## Task 21K: Static AST dependencies stay globally isolated

Prompt:

```text
Run the supplied static AST profile from a clean Skill installation. Babel is not installed, and dependency installation is authorized, but no task may create a local dependency tree in the Skill, task cache, or target project.
```

Expected route:

- `references/profiles/static-ast/index.md`
- `references/node-dependency-isolation-playbook.md`

Must conclude:

- resolve and record `npm root -g`, and require it to remain outside every managed project and Skill directory
- read the allowlisted exact versions from the committed profile manifest and use `npm install --global --ignore-scripts`
- load the packages through the global CLI, absolute global path, or process-scoped `NODE_PATH`
- run the profile tests without copying the profile or installing beneath it
- preserve the committed lockfile and confirm that no target-local `node_modules` or package-manager lockfile was created or changed
