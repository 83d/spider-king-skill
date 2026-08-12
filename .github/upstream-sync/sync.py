#!/usr/bin/env python3
"""Rebuild this fork from an exact upstream tree and reapply the 83d policy."""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[2]
AUTOMATION_ROOT = ROOT / ".github" / "upstream-sync"
OVERLAY_ROOT = AUTOMATION_ROOT / "overlays"
STATE_PATH = AUTOMATION_ROOT / "state.json"
UPSTREAM_REPOSITORY = "aoyunyang/spider-king-skill"
UPSTREAM_REF = "main"
OVERLAY_NAME = "node-dependency-isolation"
MARKER_BEGIN = f"<!-- 83D-OVERLAY:{OVERLAY_NAME}:start -->"
MARKER_END = f"<!-- 83D-OVERLAY:{OVERLAY_NAME}:end -->"
EXPECTED_STATIC_AST_DEPENDENCIES = {
    "@babel/generator",
    "@babel/parser",
    "@babel/traverse",
    "@babel/types",
}
PACKAGE_NAME_RE = re.compile(r"^@babel/[a-z0-9-]+$")
PINNED_VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
TASK_BLOCK_RE = re.compile(
    r"^## (?P<heading>Task [^\r\n]+)\r?\n(?P<body>.*?)(?=^## Task |^## Failure signals|\Z)",
    re.MULTILINE | re.DOTALL,
)
FAILURE_SIGNALS_BLOCK_RE = re.compile(
    r"^## Failure signals\r?\n(?P<body>.*)\Z",
    re.MULTILINE | re.DOTALL,
)
EXPECTED_TASK_HEADING = "Task 21K: Static AST dependencies stay globally isolated"
OVERLAY_TARGETS = frozenset(
    {
        "README.md",
        "SKILL.md",
        "references/anti-patterns-playbook.md",
        "references/node-dependency-isolation-playbook.md",
        "references/official-self-test-task-suite.md",
        "references/profiles/static-ast/index.md",
        "scripts/forward_test_report.py",
        "scripts/validate_skill.py",
    }
)


class SyncError(RuntimeError):
    """A safety or semantic gate prevented synchronization."""


def run_git(*args: str, text: bool = True) -> str | bytes:
    completed = subprocess.run(
        ["git", "-c", "core.autocrlf=false", "-C", str(ROOT), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )
    return completed.stdout


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def overlay_text(name: str) -> str:
    return read_text(OVERLAY_ROOT / name).strip()


def resolve_commit(candidate: str) -> str:
    if not re.fullmatch(r"[0-9a-fA-F]{40}", candidate):
        raise SyncError("upstream commit must be a full 40-character hexadecimal SHA")
    resolved = str(run_git("rev-parse", "--verify", f"{candidate}^{{commit}}")).strip()
    if resolved.lower() != candidate.lower():
        raise SyncError(f"upstream commit did not resolve exactly: {candidate} -> {resolved}")
    return resolved.lower()


def upstream_tree(commit: str) -> dict[str, str]:
    raw = run_git("ls-tree", "-r", "-z", commit, text=False)
    assert isinstance(raw, bytes)
    result: dict[str, str] = {}
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, object_type, object_id = metadata.decode("ascii").split()
        path = raw_path.decode("utf-8")
        if path == ".github" or path.startswith(".github/"):
            continue
        if object_type != "blob" or mode not in {"100644", "100755"}:
            raise SyncError(
                f"unsupported upstream tree entry: {path} mode={mode} type={object_type}"
            )
        result[path] = object_id
    return result


def remove_current_managed_files() -> None:
    tracked_raw = run_git("ls-files", "-z", text=False)
    assert isinstance(tracked_raw, bytes)
    parents: set[Path] = set()
    for raw_name in tracked_raw.split(b"\0"):
        if not raw_name:
            continue
        relative = raw_name.decode("utf-8")
        if relative == ".github" or relative.startswith(".github/"):
            continue
        target = ROOT / PurePosixPath(relative)
        if target.is_symlink() or target.is_file():
            target.unlink()
            parents.update(target.parents)
        elif target.exists():
            raise SyncError(f"refusing to remove unexpected tracked path type: {relative}")

    for parent in sorted(parents, key=lambda item: len(item.parts), reverse=True):
        if parent in {ROOT, ROOT / ".github"} or ROOT not in parent.parents:
            continue
        try:
            parent.rmdir()
        except OSError:
            pass


def extract_upstream_tree(commit: str) -> None:
    upstream_tree(commit)
    archive = run_git("archive", "--format=tar", commit, text=False)
    assert isinstance(archive, bytes)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as stream:
        for member in stream.getmembers():
            relative = PurePosixPath(member.name)
            if relative.is_absolute() or ".." in relative.parts:
                raise SyncError(f"unsafe path in upstream archive: {member.name}")
            if not relative.parts:
                continue
            if relative.parts[0] in {".git", ".github"}:
                continue
            destination = ROOT.joinpath(*relative.parts)
            if member.isdir():
                destination.mkdir(parents=True, exist_ok=True)
                continue
            if not member.isfile():
                raise SyncError(f"unsupported upstream archive entry: {member.name}")
            source = stream.extractfile(member)
            if source is None:
                raise SyncError(f"could not read upstream archive entry: {member.name}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_name(destination.name + ".upstream-sync-tmp")
            with temporary.open("wb") as handle:
                shutil.copyfileobj(source, handle)
            os.chmod(temporary, member.mode & 0o777)
            temporary.replace(destination)


def marked_block(fragment: str) -> str:
    return f"{MARKER_BEGIN}\n{fragment.strip()}\n{MARKER_END}"


def strip_marked_block(value: str) -> str:
    pattern = re.compile(
        rf"\n*{re.escape(MARKER_BEGIN)}.*?{re.escape(MARKER_END)}\n*",
        re.DOTALL,
    )
    return pattern.sub("\n\n", value).rstrip()


def append_marked_block(path: Path, fragment_name: str) -> None:
    base = strip_marked_block(read_text(path))
    write_text(path, f"{base}\n\n{marked_block(overlay_text(fragment_name))}")


def insert_marked_block_after(path: Path, anchor: str, fragment_name: str) -> None:
    base = strip_marked_block(read_text(path))
    if base.count(anchor) != 1:
        raise SyncError(f"semantic anchor changed in {path.relative_to(ROOT)}: {anchor!r}")
    replacement = f"{anchor}\n{marked_block(overlay_text(fragment_name))}\n"
    write_text(path, base.replace(anchor, replacement, 1))


def insert_marked_block_before(path: Path, anchor: str, fragment_name: str) -> None:
    base = strip_marked_block(read_text(path))
    if base.count(anchor) != 1:
        raise SyncError(f"semantic anchor changed in {path.relative_to(ROOT)}: {anchor!r}")
    replacement = f"{marked_block(overlay_text(fragment_name))}\n\n{anchor}"
    write_text(path, base.replace(anchor, replacement, 1))


def replace_section(path: Path, heading: str, next_heading: str, fragment_name: str) -> None:
    value = read_text(path)
    pattern = re.compile(
        rf"(?ms)^{re.escape(heading)}\n.*?(?=^{re.escape(next_heading)}\n)"
    )
    replacement = overlay_text(fragment_name) + "\n\n"
    updated, count = pattern.subn(replacement, value)
    if count != 1:
        raise SyncError(f"section boundary changed in {path.relative_to(ROOT)}: {heading}")
    write_text(path, updated)


def official_suite_digest(suite_text: str) -> str:
    normalized = suite_text.replace("\r\n", "\n").replace("\r", "\n")
    task_blocks = [match.group(0).rstrip() for match in TASK_BLOCK_RE.finditer(normalized)]
    failure_match = FAILURE_SIGNALS_BLOCK_RE.search(normalized)
    failure_signals = failure_match.group(0).rstrip() if failure_match else ""
    payload = json.dumps(
        {"tasks": task_blocks, "failure_signals": failure_signals},
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def patch_digest_declaration(path: Path, digest: str) -> None:
    value = read_text(path)
    digest_pattern = re.compile(
        r'OFFICIAL_SUITE_CONTRACT_SHA256\s*=\s*\(\s*"[0-9a-f]{64}"\s*\)',
        re.MULTILINE,
    )
    digest_replacement = (
        "OFFICIAL_SUITE_CONTRACT_SHA256 = (\n"
        f'    "{digest}"\n'
        ")"
    )
    value, count = digest_pattern.subn(digest_replacement, value)
    if count != 1:
        raise SyncError(
            f"suite fingerprint declaration changed in {path.relative_to(ROOT)}"
        )
    write_text(path, value)


def patch_official_suite_and_validator() -> None:
    suite_path = ROOT / "references" / "official-self-test-task-suite.md"
    suite = read_text(suite_path)
    old_heading_match = re.search(r"(?m)^## (Task 21K:[^\n]+)$", suite)
    if old_heading_match is None:
        raise SyncError("upstream Task 21K is missing")
    old_heading = old_heading_match.group(1)
    task_pattern = re.compile(
        r"(?ms)^## Task 21K:[^\n]+\n.*?(?=^## Task 21L:[^\n]+\n)"
    )
    replacement = overlay_text("official-task-21k.md") + "\n\n"
    suite, count = task_pattern.subn(replacement, suite)
    if count != 1:
        raise SyncError("upstream Task 21K boundaries changed")
    write_text(suite_path, suite)

    validator_path = ROOT / "scripts" / "validate_skill.py"
    validator = read_text(validator_path)
    old_literal = json.dumps(old_heading)
    new_literal = json.dumps(EXPECTED_TASK_HEADING)
    if validator.count(old_literal) != 1:
        raise SyncError("validator Task 21K registry changed")
    validator = validator.replace(old_literal, new_literal, 1)
    digest = official_suite_digest(suite)
    write_text(validator_path, validator)
    patch_digest_declaration(validator_path, digest)
    patch_digest_declaration(ROOT / "scripts" / "forward_test_report.py", digest)


def apply_overlay(commit: str) -> None:
    remove_current_managed_files()
    extract_upstream_tree(commit)

    append_marked_block(ROOT / "README.md", "readme-section.md")
    insert_marked_block_after(
        ROOT / "SKILL.md",
        "## Non-Negotiables\n",
        "SKILL.md",
    )
    insert_marked_block_before(
        ROOT / "references" / "anti-patterns-playbook.md",
        "## Entry format for new anti-patterns",
        "anti-patterns-playbook.md",
    )
    shutil.copyfile(
        OVERLAY_ROOT / "node-dependency-isolation-playbook.md",
        ROOT / "references" / "node-dependency-isolation-playbook.md",
    )
    replace_section(
        ROOT / "references" / "profiles" / "static-ast" / "index.md",
        "## Usage",
        "## Supported static observations",
        "static-ast-usage.md",
    )
    patch_official_suite_and_validator()

    state = {
        "overlay": OVERLAY_NAME,
        "upstream_ref": UPSTREAM_REF,
        "upstream_repository": UPSTREAM_REPOSITORY,
        "upstream_sha": commit,
    }
    write_text(STATE_PATH, json.dumps(state, indent=2, sort_keys=True))
    verify_overlay(commit)


def static_ast_dependencies() -> dict[str, str]:
    package_path = ROOT / "references" / "profiles" / "static-ast" / "package.json"
    package = json.loads(read_text(package_path))
    dependencies = package.get("dependencies")
    if not isinstance(dependencies, dict):
        raise SyncError("static-ast package.json must contain a dependencies object")
    if set(dependencies) != EXPECTED_STATIC_AST_DEPENDENCIES:
        raise SyncError(
            "static-ast dependency allowlist changed: "
            f"expected {sorted(EXPECTED_STATIC_AST_DEPENDENCIES)}, "
            f"observed {sorted(dependencies)}"
        )
    result: dict[str, str] = {}
    for name, version in dependencies.items():
        if not isinstance(name, str) or PACKAGE_NAME_RE.fullmatch(name) is None:
            raise SyncError(f"unsafe static-ast package name: {name!r}")
        if not isinstance(version, str) or PINNED_VERSION_RE.fullmatch(version) is None:
            raise SyncError(f"static-ast dependency is not exactly pinned: {name}={version!r}")
        result[name] = version
    return result


def verify_overlay(expected_commit: str | None = None) -> None:
    state = json.loads(read_text(STATE_PATH))
    state_sha = state.get("upstream_sha")
    if not isinstance(state_sha, str) or re.fullmatch(r"[0-9a-f]{40}", state_sha) is None:
        raise SyncError("state.json contains an invalid upstream SHA")
    if expected_commit is not None and state_sha != expected_commit:
        raise SyncError(f"state SHA mismatch: expected {expected_commit}, observed {state_sha}")
    if state.get("upstream_repository") != UPSTREAM_REPOSITORY:
        raise SyncError("state.json upstream repository changed")

    tree = upstream_tree(state_sha)
    candidate_paths: set[str] = set()
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if not relative.parts or relative.parts[0] in {".git", ".github"}:
            continue
        if path.is_symlink():
            raise SyncError(f"candidate contains an unsupported symlink: {relative.as_posix()}")
        if path.is_file():
            candidate_paths.add(relative.as_posix())
    expected_paths = set(tree) | {"references/node-dependency-isolation-playbook.md"}
    if candidate_paths != expected_paths:
        missing = sorted(expected_paths - candidate_paths)
        extra = sorted(candidate_paths - expected_paths)
        raise SyncError(f"candidate file set drifted: missing={missing} extra={extra}")
    for relative, expected_object in tree.items():
        if relative in OVERLAY_TARGETS:
            continue
        actual_object = str(
            run_git("hash-object", "--no-filters", "--", relative)
        ).strip()
        if actual_object != expected_object:
            raise SyncError(
                f"non-overlay file differs from upstream: {relative} "
                f"expected={expected_object} observed={actual_object}"
            )

    for relative in (
        "README.md",
        "SKILL.md",
        "references/anti-patterns-playbook.md",
    ):
        value = read_text(ROOT / relative)
        if value.count(MARKER_BEGIN) != 1 or value.count(MARKER_END) != 1:
            raise SyncError(f"overlay markers are missing or duplicated in {relative}")

    expected_playbook = (OVERLAY_ROOT / "node-dependency-isolation-playbook.md").read_bytes()
    actual_playbook = (ROOT / "references" / "node-dependency-isolation-playbook.md").read_bytes()
    if actual_playbook != expected_playbook:
        raise SyncError("installed Node dependency isolation playbook differs from its overlay")

    static_ast = read_text(ROOT / "references" / "profiles" / "static-ast" / "index.md")
    for required in ("npm root -g", "npm install --global", "NODE_PATH"):
        if required not in static_ast:
            raise SyncError(f"static-ast global dependency rule is missing: {required}")
    if "npm ci" in static_ast:
        raise SyncError("static-ast profile still permits a local npm ci")
    static_ast_dependencies()

    suite = read_text(ROOT / "references" / "official-self-test-task-suite.md")
    if suite.count(f"## {EXPECTED_TASK_HEADING}") != 1:
        raise SyncError("fork-specific Task 21K is missing or duplicated")
    for required in ("npm root -g", "npm install --global", "target-local `node_modules`"):
        if required not in suite:
            raise SyncError(f"fork-specific Task 21K invariant is missing: {required}")

    validator = read_text(ROOT / "scripts" / "validate_skill.py")
    if json.dumps(EXPECTED_TASK_HEADING) not in validator:
        raise SyncError("validator does not register the fork-specific Task 21K")
    expected_digest = official_suite_digest(suite)
    if expected_digest not in validator:
        raise SyncError("validator fingerprint was not updated for the fork-specific suite")
    forward_report = read_text(ROOT / "scripts" / "forward_test_report.py")
    if expected_digest not in forward_report:
        raise SyncError("forward-test reporter fingerprint was not updated for the fork-specific suite")

    skill = read_text(ROOT / "SKILL.md")
    if not re.match(r"\A---\nname:\s*spider-king\n", skill):
        raise SyncError("SKILL.md frontmatter is invalid")
    for path in ROOT.rglob("*.py"):
        if ".git" in path.parts:
            continue
        ast.parse(read_text(path), filename=str(path))


def dependency_inventory() -> dict[str, list[dict[str, str | int]]]:
    node_modules: list[dict[str, str | int]] = []
    lockfiles: list[dict[str, str | int]] = []
    lock_names = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock"}
    for path in sorted(ROOT.rglob("*")):
        relative_parts = path.relative_to(ROOT).parts
        if ".git" in relative_parts:
            continue
        if path.is_dir() and path.name == "node_modules":
            node_modules.append({"path": path.relative_to(ROOT).as_posix()})
        elif path.is_file() and path.name in lock_names:
            data = path.read_bytes()
            lockfiles.append(
                {
                    "bytes": len(data),
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
    return {"lockfiles": lockfiles, "node_modules": node_modules}


def install_global_dependencies() -> None:
    dependencies = static_ast_dependencies()
    npm = shutil.which("npm")
    if npm is None:
        raise SyncError("npm is not available on PATH")
    npm_root = subprocess.run(
        [npm, "root", "--global"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()
    resolved_npm_root = Path(npm_root).resolve()
    if resolved_npm_root == ROOT or ROOT in resolved_npm_root.parents:
        raise SyncError(f"global npm root resolves inside the repository: {resolved_npm_root}")
    packages = [f"{name}@{dependencies[name]}" for name in sorted(dependencies)]
    subprocess.run(
        [
            npm,
            "install",
            "--global",
            "--ignore-scripts",
            "--no-audit",
            "--no-fund",
            *packages,
        ],
        check=True,
    )
    subprocess.run(
        [npm, "list", "--global", "--depth=0", *packages],
        check=True,
    )
    print(f"global_npm_root={resolved_npm_root}")
    print("packages=" + ",".join(packages))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    apply_parser = subparsers.add_parser("apply", help="rebuild from upstream and apply the overlay")
    apply_parser.add_argument("--upstream-commit", required=True)
    verify_parser = subparsers.add_parser("verify", help="verify the current overlay")
    verify_parser.add_argument("--upstream-commit")
    subparsers.add_parser("inventory", help="print target-local Node dependency inventory")
    subparsers.add_parser(
        "install-global-deps",
        help="install the allowlisted static-ast dependencies under npm root -g",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "apply":
            apply_overlay(resolve_commit(args.upstream_commit))
        elif args.command == "verify":
            expected = resolve_commit(args.upstream_commit) if args.upstream_commit else None
            verify_overlay(expected)
        elif args.command == "inventory":
            print(json.dumps(dependency_inventory(), indent=2, sort_keys=True))
        elif args.command == "install-global-deps":
            install_global_dependencies()
        else:  # pragma: no cover
            raise SyncError(f"unsupported command: {args.command}")
    except (OSError, subprocess.CalledProcessError, SyncError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
