<div align="center">

# 🎓 PaperScholar

**The Unified Academic Writing AI Workflow**

*Integrating PaperForge × PaperSpine × PaperMind*

[![CI](https://github.com/your-username/PaperScholar/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/PaperScholar/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![Gradio](https://img.shields.io/badge/UI-Gradio-orange)](https://gradio.app)
[![Stars](https://img.shields.io/github/stars/your-username/PaperScholar?style=social)](https://github.com/your-username/PaperScholar)

[English](./README.md) | [中文](./README.zh-CN.md)

</div>

---

## Why PaperScholar?

Three great open-source tools existed separately. PaperScholar unifies their strongest features:

| Origin | Strongest Feature | Integrated As |
|--------|------------------|---------------|
| **PaperForge** | Evidence-bank discipline — every claim needs a source before it can appear | `CitationSkill` + `AuditSkill` |
| **PaperSpine** | Blueprint-first structural workflow — structure before sentences | `BlueprintSkill` + `BuildSkill` |
| **PaperMind** | Chinese research ecosystem — tutor mode, AI-tone removal, rebuttal | `TutorSkill` + `AiToneSkill` + `RebuttalSkill` |

---

## Feature Matrix

| Feature | PaperScholar | PaperForge | PaperSpine | PaperMind |
|---------|:---:|:---:|:---:|:---:|
| Evidence bank (claim → source) | ✅ | ✅ | — | — |
| Blueprint-first workflow | ✅ | — | ✅ | — |
| Writing rationale matrix | ✅ | ✅ | ✅ | — |
| Tutor / reviewer simulation | ✅ | — | — | ✅ |
| AI-tone detection & removal | ✅ | — | — | ✅ |
| Innovation check | ✅ | — | — | ✅ |
| Rebuttal generation | ✅ | — | — | ✅ |
| Paper deconstruction | ✅ | — | — | ✅ |
| Chinese scene templates | ✅ | — | — | ✅ |
| Web UI (no coding) | ✅ | — | — | ✅ |
| Final audit vs evidence bank | ✅ | ✅ | — | — |
| Multi-model support | ✅ (8+) | ✅ (7+) | ✅ | ✅ (7+) |
| Task-based model routing | ✅ | — | — | ✅ |
| LaTeX / Word output check | ✅ | ✅ | — | — |
| Translation package | ✅ | ✅ | — | ✅ |

---

## Supported AI Providers

| Provider | Default Model | Best For |
|----------|--------------|----------|
| **DeepSeek** ⭐ Recommended | deepseek-chat | Budget, logic, audit |
| **Anthropic** | claude-sonnet-4-20250514 | LaTeX, rewriting, audit |
| **OpenAI** | gpt-4o | English polish, general |
| **Qwen (Alibaba)** | qwen-max | Chinese, long context |
| **GLM (Zhipu)** | glm-4 | Chinese academic |
| **Moonshot (Kimi)** | moonshot-v1-128k | Ultra-long PDF reading |
| **Doubao (ByteDance)** | doubao-pro-32k | Speed, budget |
| **Custom** | any | Any OpenAI-compatible API |

---

## Quick Start

### Option A: Web UI (Recommended — no coding)

```bash
git clone https://github.com/your-username/PaperScholar.git
cd PaperScholar
pip install openai gradio
python src/web_ui.py
# Open http://localhost:7860
```

### Option B: Command Line (Full workflow)

```bash
pip install openai

# Copy and edit config
cp paperscholar_config.example.json paperscholar_config.json
# Add your API key to paperscholar_config.json

# Build paper from materials
python src/orchestrator.py \
  --config paperscholar_config.json \
  --inputs my_notes.txt references.txt \
  --output paper_output/

# Rewrite existing draft
python src/orchestrator.py \
  --config paperscholar_config.json \
  --inputs draft.txt \
  --output paper_output/

# Single skill: tutor review
python src/orchestrator.py \
  --config paperscholar_config.json \
  --inputs draft.txt \
  --skill tutor

# Single skill: rebuttal
python src/orchestrator.py \
  --config paperscholar_config.json \
  --skill rebuttal \
  --reviewer "Reviewer 2: The novelty is insufficient."

# Single skill: AI-tone check
python src/orchestrator.py \
  --config paperscholar_config.json \
  --inputs draft.txt \
  --skill ai_tone
```

### Option C: Claude Code / Codex Skill

```bash
# macOS / Linux
chmod +x install.sh
./install.sh --target all

# Windows
.\install.ps1 -Target all
```

After install: `/paperscholar` in Claude Code, `$paperscholar` in Codex.

---

## Full Workflow

```
[Input Materials / Draft]
         │
    ┌────▼────┐
    │ INTAKE  │  Validate config, collect files
    └────┬────┘
         │
    ┌────▼──────┐
    │ RESEARCH  │  Learn target scene (journal/conference/thesis/proposal)
    └────┬──────┘
         │
    ┌────▼──────────┐
    │ CITATION /    │  Extract every claim → evidence ID → source
    │ EVIDENCE BANK │  (PaperForge discipline: no claim without source)
    └────┬──────────┘
         │
    ┌────▼───────┐
    │ BLUEPRINT  │  Build section structure + writing motivation per section
    └────┬───────┘
         │
    ┌────▼─────────────────┐
    │ BUILD or REWRITE     │  Write/rewrite with evidence-bank enforcement
    └────┬─────────────────┘
         │
    ┌────▼────────────────────────────────────────┐
    │ POST-PROCESSING (all parallel)               │
    │  • Tutor Review (mentor/conference style)    │
    │  • AI Tone Check & Removal                  │
    │  • Innovation Check                          │
    │  • Final Audit vs Evidence Bank             │
    │  • Translation Package (if enabled)          │
    └────┬────────────────────────────────────────┘
         │
    [Output Files]
```

---

## Output Files

```
paperscholar_output/
  paperscholar_config.json      # Run configuration (no API key)
  research_dossier.md           # Scene profile + material analysis
  evidence_bank.md              # All claims with evidence IDs + sources
  section_blueprint.md          # Section structure + writing motivation
  draft_full.md                 # Complete paper draft
  writing_rationale_matrix.json # Why each section was written this way
  tutor_review.md               # ⭐ Mentor review with scoring table
  ai_tone_check.md              # AI-tone detection + fixes
  innovation_check.md           # Novelty assessment
  revision_audit.md             # Final audit against evidence bank
  translation_package.md        # Bilingual output (if enabled)
  rebuttal.md                   # Reviewer rebuttal (if requested)
```

---

## Supported Scenes

| Scene | Use Case | Templates |
|-------|----------|-----------|
| `journal` | SCI/EI journal papers | High citation density, hedging |
| `conference` | NeurIPS/CVPR/ACL etc. | Page limit, results-forward |
| `report` | Technical / research reports | Audience-aware |
| `competition` | Mathematical modeling | Sensitivity analysis mandatory |
| `thesis` | 中文硕博学位论文 | GB/T 7714, 中英双摘要 |
| `proposal` | 国自然/开题报告 | Innovation + feasibility |

---

## Tutor Styles

| Style | Simulates | Best For |
|-------|-----------|----------|
| `strict` | 严格中文导师 | General review |
| `neurips` | NeurIPS Area Chair | ML/AI papers |
| `cvpr` | CVPR reviewer | Computer vision |
| `acl` | ACL reviewer | NLP papers |
| `iclr` | ICLR reviewer | Deep learning |
| `nature` | Nature/Science reviewer | High-impact science |

---

## Configuration

```json
{
  "provider": "deepseek",
  "model": "deepseek-chat",
  "api_key": "YOUR_KEY",
  "scene": "journal",
  "workflow": "build",
  "research_depth": "flash",
  "output_language": "Chinese",
  "translation_package": false,
  "tutor_style": "strict",
  "cn_scene": ""
}
```

| Field | Options | Description |
|-------|---------|-------------|
| `provider` | `anthropic/openai/deepseek/qwen/glm/moonshot/doubao/custom` | AI provider |
| `scene` | `journal/conference/report/competition/thesis/proposal` | Target venue |
| `workflow` | `build/rewrite` | Build from scratch or rewrite |
| `research_depth` | `flash` (fast) / `pro` (thorough) | Research intensity |
| `output_language` | `Chinese/English` | Draft language |
| `translation_package` | `true/false` | Generate bilingual output |
| `tutor_style` | `strict/neurips/cvpr/acl/iclr/nature` | Review persona |
| `cn_scene` | `thesis/proposal/competition` | Chinese-specific template |

---

## Repository Structure

```
PaperScholar/
  src/
    core/
      model_adapter.py          # Unified multi-provider adapter + task routing
    prompts/
      prompts.py                # All prompts (tutor, evidence, blueprint, etc.)
    scripts/
      artifact_check.py         # Output completeness checker
      latex_guard.py            # LaTeX syntax checker
      word_guard.py             # Word document checker
      intake_wizard.py          # Interactive config wizard
    references/
      build_workflow.md         # Build workflow reference
      rewrite_workflow.md       # Rewrite workflow reference
      scene_style_guide.md      # Scene-specific style guide
    orchestrator.py             # Main workflow orchestrator
    web_ui.py                   # Gradio Web UI
  dist/
    claude/
      skills/paperscholar/      # Claude Code skill
      commands/paperscholar.md  # Claude Code command
    codex/
      skills/paperscholar/      # Codex skill
  tests/
    test_paperscholar.py
  paperscholar_config.example.json
  install.sh
  install.ps1
  requirements.txt
  README.md
  README.zh-CN.md
```

---

## Development

```bash
# Run tests
pip install pytest
pytest tests/ -v

# Lint
pip install pyflakes
python -m pyflakes src/

# Contribute new tutor style
# Edit src/prompts/prompts.py → add to TUTOR_MAP
```

PRs welcome! Especially:
- New tutor styles (domain-specific reviewer personas)
- New Chinese scene templates
- Prompt optimizations in `src/prompts/prompts.py`
- Additional provider support

---

## Credits

PaperScholar is built on top of three open-source projects:

- **[PaperForge](https://github.com/your-username/PaperForge)** — Evidence-bank discipline and scene auditing
- **[PaperSpine](https://github.com/WUBING2023/PaperSpine)** — Blueprint-first structural workflow
- **[PaperMind](https://github.com/your-username/PaperMind)** — Chinese research ecosystem and tutor mode

---

## License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE).
