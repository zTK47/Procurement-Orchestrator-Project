#!/usr/bin/env bash
# Exposes the canonical skills/ directory to a coding agent.
# Usage: bash scripts/setup-skills.sh [copilot|codex|claude|cline|all]
# Links to skills/ and falls back to copying; existing destinations are kept.
# Discovery paths below are the ones known for these tools; verify discovery
# in your agent. Other agents can read skills/ directly by path.
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -d skills ]; then
  echo "skills/ not found; run from the repository root." >&2
  exit 1
fi

choice="${1:-}"
if [ -z "$choice" ]; then
  read -r -p "Agent (copilot, codex, claude, cline, all): " choice
fi

link_skills() {
  local dest="$1"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    echo "kept existing $dest"
    return
  fi
  mkdir -p "$(dirname "$dest")"
  if ln -s "$(realpath --relative-to="$(dirname "$dest")" skills)" "$dest" 2>/dev/null; then
    echo "linked $dest -> skills/"
  else
    cp -R skills "$dest"
    echo "copied skills/ to $dest (refresh manually after skill changes)"
  fi
}

ensure_claude_md() {
  if [ -e CLAUDE.md ]; then
    echo "kept existing CLAUDE.md"
  else
    printf '@AGENTS.md\n' > CLAUDE.md
    echo "created CLAUDE.md"
  fi
}

case "$choice" in
  copilot) link_skills .github/skills ;;
  codex)   link_skills .agents/skills ;;
  claude)  link_skills .claude/skills; ensure_claude_md ;;
  cline)   link_skills .claude/skills ;;
  all)
    link_skills .github/skills
    link_skills .agents/skills
    link_skills .claude/skills
    ensure_claude_md
    ;;
  *)
    echo "Unknown agent '$choice'. Choose copilot, codex, claude, cline or all." >&2
    exit 1
    ;;
esac
