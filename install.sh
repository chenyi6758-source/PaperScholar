#!/usr/bin/env bash
# PaperScholar Installer — macOS / Linux
set -e

TARGET="${1:-all}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🎓 PaperScholar Installer"
echo "Target: $TARGET"
echo ""

# Python deps
if command -v pip3 &>/dev/null; then
  pip3 install openai gradio --quiet
elif command -v pip &>/dev/null; then
  pip install openai gradio --quiet
fi

CODEX_SKILLS="$HOME/.codex/skills"
CLAUDE_SKILLS="$HOME/.claude/skills"
CLAUDE_COMMANDS="$HOME/.claude/commands"

if [[ "$TARGET" == "all" || "$TARGET" == "codex" ]]; then
  mkdir -p "$CODEX_SKILLS/paperscholar"
  cp -r "$SCRIPT_DIR/dist/codex/skills/paperscholar/." "$CODEX_SKILLS/paperscholar/"
  echo "✅ Installed to Codex skills: $CODEX_SKILLS/paperscholar"
  echo "   → Restart Codex and use: \$paperscholar"
fi

if [[ "$TARGET" == "all" || "$TARGET" == "claude" ]]; then
  mkdir -p "$CLAUDE_SKILLS" "$CLAUDE_COMMANDS"
  for skill_dir in "$SCRIPT_DIR/dist/claude/skills/"*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p "$CLAUDE_SKILLS/$skill_name"
    cp -r "$skill_dir/." "$CLAUDE_SKILLS/$skill_name/"
  done
  cp "$SCRIPT_DIR/dist/claude/commands/paperscholar.md" "$CLAUDE_COMMANDS/"
  echo "✅ Installed to Claude Code skills"
  echo "   → Reload and use: /paperscholar"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Quick start:"
echo "  cp paperscholar_config.example.json paperscholar_config.json"
echo "  # Edit paperscholar_config.json and add your API key"
echo "  python src/orchestrator.py --config paperscholar_config.json --inputs your_draft.txt --output output/"
echo ""
echo "Web UI:"
echo "  python src/web_ui.py"
echo "  # Open http://localhost:7860"
