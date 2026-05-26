<div align="center">

# 🎓 PaperScholar

**The Academic Writing AI Toolkit for Chinese Researchers**

*Tutor Mode · AI-Tone Removal · Innovation Check · Rebuttal Generator*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![Gradio](https://img.shields.io/badge/UI-Gradio-orange)](https://gradio.app)
[![Stars](https://img.shields.io/github/stars/chenyi6758-source/PaperScholar?style=social)](https://github.com/chenyi6758-source/PaperScholar)

[English](./README.md) | [中文](./README.zh-CN.md)

</div>

-----

## What is PaperScholar?

PaperScholar is an AI-powered academic writing toolkit built specifically for Chinese researchers and students. Unlike tools that simply “generate papers,” PaperScholar acts as a **strict mentor** — helping you think like a real academic author.

**Core philosophy: every claim needs evidence. Structure before sentences. Chinese researchers deserve native-language support.**

-----

## Features

|Feature                   |Description                                                                                                                                                    |
|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
|👨‍🏫 **Tutor Mode**          |Simulates strict mentors and top-conference reviewers (NeurIPS/CVPR/ACL/Nature). Gives scoring table + specific revision instructions. All analysis in Chinese.|
|✨ **AI-Tone Removal**     |Detects and eliminates AI-generated text patterns — hollow openers, excessive connectives, vague claims                                                        |
|💡 **Innovation Check**    |Distinguishes real innovation from “method transfer”, “parameter tuning”, or “dataset swap”                                                                    |
|📝 **Rebuttal Generator**  |Generates point-by-point reviewer responses. Chinese analysis + English formal reply                                                                           |
|📚 **Evidence Bank**       |Every claim must link to a source before it appears in the draft                                                                                               |
|📐 **Blueprint-First**     |Plan section structure and writing motivation before generating text                                                                                           |
|🔬 **Paper Deconstruction**|Reverse-engineers top papers to extract argument structure and writing patterns                                                                                |
|🌐 **Web UI**              |Gradio interface — no coding required, open browser and use                                                                                                    |
|🤖 **Multi-Model**         |Supports 8+ AI providers with task-based intelligent routing                                                                                                   |

-----

## Supported AI Providers

|Provider                  |Default Model           |Best For             |
|--------------------------|------------------------|---------------------|
|**DeepSeek** ⭐ Recommended|deepseek-chat           |Budget, logic, audit |
|**Anthropic**             |claude-sonnet-4-20250514|Rewriting, audit     |
|**OpenAI**                |gpt-4o                  |English polish       |
|**Qwen (Alibaba)**        |qwen-max                |Chinese, long context|
|**GLM (Zhipu)**           |glm-4                   |Chinese academic     |
|**Moonshot (Kimi)**       |moonshot-v1-128k        |Ultra-long PDF       |
|**Doubao (ByteDance)**    |doubao-pro-32k          |Speed, budget        |
|**Custom**                |any                     |OpenAI-compatible API|

-----

## Quick Start

### Option A: Web UI (Recommended)

```bash
git clone https://github.com/chenyi6758-source/PaperScholar.git
cd PaperScholar
pip install openai gradio
python src/web_ui.py
# Open http://localhost:7860
```

Paste your API Key in the browser, no config file needed.

### Option B: Command Line

```bash
pip install openai

# Copy and edit config
cp paperscholar_config.example.json paperscholar_config.json
# Fill in your API key

# Build paper from materials
python src/orchestrator.py \
  --config paperscholar_config.json \
  --inputs my_notes.txt \
  --output paper_output/

# Rewrite existing draft
python src/orchestrator.py \
  --config paperscholar_config.json \
  --inputs draft.txt \
  --output paper_output/

# Tutor review only
python src/orchestrator.py \
  --config paperscholar_config.json \
  --inputs draft.txt \
  --skill tutor

# Generate rebuttal
python src/orchestrator.py \
  --config paperscholar_config.json \
  --skill rebuttal \
  --reviewer "Reviewer 2: The novelty is insufficient."
```

-----

## Workflow

```
[Input: Materials / Draft]
         │
    ┌────▼────┐
    │ INTAKE  │  Validate config, collect files
    └────┬────┘
         │
    ┌────▼──────────┐
    │ EVIDENCE BANK │  Every claim → evidence ID → source
    └────┬──────────┘
         │
    ┌────▼───────┐
    │ BLUEPRINT  │  Section structure + writing motivation
    └────┬───────┘
         │
    ┌────▼──────────────┐
    │ BUILD or REWRITE  │  Draft with evidence enforcement
    └────┬──────────────┘
         │
    ┌────▼────────────────────────────┐
    │ POST-PROCESSING                 │
    │  • Tutor Review                 │
    │  • AI-Tone Detection & Removal  │
    │  • Innovation Check             │
    │  • Final Audit                  │
    │  • Translation Package          │
    └────┬────────────────────────────┘
         │
    [Output Files]
```

-----

## Output Files

```
paperscholar_output/
  evidence_bank.md          # All claims with sources
  section_blueprint.md      # Structure + writing motivation
  draft_full.md             # Complete paper draft
  tutor_review.md           # ⭐ Mentor review with scoring table
  ai_tone_check.md          # AI-tone detection + fixes
  innovation_check.md       # Novelty assessment
  revision_audit.md         # Final audit report
  rebuttal.md               # Reviewer rebuttal (if requested)
  translation_package.md    # Bilingual output (if enabled)
```

-----

## Supported Scenes

|Scene        |Use Case                    |
|-------------|----------------------------|
|`journal`    |SCI/EI journal papers       |
|`conference` |NeurIPS / CVPR / ACL etc.   |
|`thesis`     |中文硕博学位论文                    |
|`proposal`   |国自然 / 开题报告                  |
|`competition`|数学建模竞赛论文                    |
|`report`     |Technical / research reports|

-----

## Tutor Styles

|Style    |Simulates                |
|---------|-------------------------|
|`strict` |严格中文导师（通用）               |
|`neurips`|NeurIPS Area Chair       |
|`cvpr`   |CVPR Reviewer            |
|`acl`    |ACL Reviewer             |
|`iclr`   |ICLR Reviewer            |
|`nature` |Nature / Science Reviewer|

-----

## Configuration

```json
{
  "provider": "deepseek",
  "model": "deepseek-chat",
  "api_key": "YOUR_KEY",
  "scene": "journal",
  "workflow": "build",
  "output_language": "Chinese",
  "tutor_mode": true,
  "tutor_style": "strict",
  "remove_ai_tone": true,
  "translation_package": false
}
```

-----

## Contributing

PRs welcome! Especially:

- New tutor styles (domain-specific reviewer personas)
- New Chinese scene templates
- Prompt optimizations in `src/prompts/prompts.py`

-----

## License

MIT License — free to use, modify, and distribute.