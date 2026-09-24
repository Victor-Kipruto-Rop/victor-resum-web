#!/usr/bin/env python3
"""Assemble the public website into ./_site for GitHub Pages.

Only the website is published. Automation, tooling, subscriber data, logs and
generated strategy/distribution files stay in the repo but are never served
from the public domain.

Usage (from the repo root):  python3 tools/build_site.py
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"

# Top-level folders that are never published
PRIVATE_DIRS = {
    ".git", ".github", "_site", "tools", "scripts", "automation",
    "social-automation", "blog-ai", "blog-ai-posts", "subscribers",
    "dispatch_logs", "notifications", "strategy", "distribution",
    "analytics", "integration", "venv", "node_modules",
}
# Top-level files that are never published
PRIVATE_FILES = {"subscribers.json"}
# Never published, at any depth
PRIVATE_SUFFIXES = {".py", ".pyc", ".sh", ".db"}
PRIVATE_DIRNAMES = {"__pycache__"}
KEEP_DOTFILES = {".nojekyll"}

# Must exist in the built site
REQUIRED = ["index.html", "CNAME", ".nojekyll", "robots.txt", "sitemap.xml",
            "data/top_repos_fallback.json"]


def ignore(directory, names):
    top = Path(directory).resolve() == ROOT
    skipped = []
    for name in names:
        p = Path(name)
        if top and (name in PRIVATE_DIRS or name in PRIVATE_FILES):
            skipped.append(name)
        elif name in PRIVATE_DIRNAMES or p.suffix in PRIVATE_SUFFIXES:
            skipped.append(name)
        elif name.startswith(".") and name not in KEEP_DOTFILES:
            skipped.append(name)
    return skipped


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT, OUT, ignore=ignore)

    problems = [f"missing: {r}" for r in REQUIRED if not (OUT / r).exists()]
    for f in OUT.rglob("*"):
        rel = f.relative_to(OUT)
        if f.is_file() and (f.suffix in PRIVATE_SUFFIXES
                            or (f.name.startswith(".") and f.name not in KEEP_DOTFILES)):
            problems.append(f"non-public file published: {rel}")
    for d in PRIVATE_DIRS | PRIVATE_FILES:
        if (OUT / d).exists():
            problems.append(f"non-public path published: {d}")

    if problems:
        print("Site build FAILED:\n  " + "\n  ".join(problems))
        sys.exit(1)

    files = sum(1 for f in OUT.rglob("*") if f.is_file())
    print(f"Built {OUT.name}/ with {files} public files")


if __name__ == "__main__":
    main()
