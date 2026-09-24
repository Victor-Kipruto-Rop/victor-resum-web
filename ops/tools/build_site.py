#!/usr/bin/env python3
"""Assemble the publishable website from ./public into ./_site for GitHub Pages.

./public is the source of truth for publishable content (it is also what
Cloudflare Workers serves via wrangler.jsonc). The repo-root CNAME and
.nojekyll are copied alongside it because GitHub Pages expects them at the
site root. Automation, tooling, subscriber data, logs and generated
ops/strategy/distribution files stay in the repo but are never served from
the public domain.

Usage (from the repo root):  python3 ops/tools/build_site.py
"""
import shutil
import sys
from pathlib import Path

# ops/tools/build_site.py -> repo root is parents[2]
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "public"
OUT = ROOT / "_site"

# Repo-root files GitHub Pages needs that live outside ./public
ROOT_PUBLISH = ["CNAME", ".nojekyll"]

# Never published, at any depth (defence in depth: ./public is the only
# source, so these can only reach the build via an accidental leak).
NEVER_PUBLISH_DIRS = {
    "ops", "content", ".git", ".github", "_site", "tools", "scripts", "automation",
    "social-automation", "blog-ai", "blog-ai-posts", "subscribers",
    "dispatch_logs", "notifications", "strategy", "distribution",
    "analytics", "venv", "node_modules",
}
# Files that must never be published
NEVER_PUBLISH_FILES = {"subscribers.json"}
# Never published, at any depth
PRIVATE_SUFFIXES = {".py", ".pyc", ".sh", ".db"}
PRIVATE_DIRNAMES = {"__pycache__"}
KEEP_DOTFILES = {".nojekyll"}

# Must exist in the built site
REQUIRED = ["index.html", "CNAME", ".nojekyll", "robots.txt", "sitemap.xml",
            "data/top_repos_fallback.json"]


def ignore(directory, names):
    skipped = []
    for name in names:
        p = Path(name)
        if name in NEVER_PUBLISH_DIRS or name in NEVER_PUBLISH_FILES:
            skipped.append(name)
        elif name in PRIVATE_DIRNAMES or p.suffix in PRIVATE_SUFFIXES:
            skipped.append(name)
        elif name.startswith(".") and name not in KEEP_DOTFILES:
            skipped.append(name)
    return skipped


def main():
    if not SRC.is_dir():
        print(f"Site build FAILED: publishable source missing: {SRC}")
        sys.exit(1)

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT, ignore=ignore)

    for name in ROOT_PUBLISH:
        src = ROOT / name
        if src.is_file():
            shutil.copy2(src, OUT / name)

    problems = [f"missing: {r}" for r in REQUIRED if not (OUT / r).exists()]
    for f in OUT.rglob("*"):
        rel = f.relative_to(OUT)
        if f.is_file() and (f.suffix in PRIVATE_SUFFIXES
                            or f.name in NEVER_PUBLISH_FILES
                            or (f.name.startswith(".") and f.name not in KEEP_DOTFILES)):
            problems.append(f"non-public file published: {rel}")
    for d in NEVER_PUBLISH_DIRS:
        if (OUT / d).exists():
            problems.append(f"non-public path published: {d}")

    if problems:
        print("Site build FAILED:\n  " + "\n  ".join(problems))
        sys.exit(1)

    files = sum(1 for f in OUT.rglob("*") if f.is_file())
    print(f"Built {OUT.name}/ with {files} public files")


if __name__ == "__main__":
    main()
