# PaperForge — Build Workflow Reference

This document describes the complete Build From Materials workflow.
Each stage lists its inputs, outputs, and the decision rules that govern it.

---

## Overview

```
intake → research → citation → motivation → blueprint → build → audit → assembly → [translate]
```

**When to use Build:** You have raw materials — notes, PDFs, figures, experiment results, an outline — but no complete existing manuscript. PaperForge will construct the paper from scratch using your materials as the evidence base.

---

## Stage 1: Intake

**Purpose:** Validate configuration and collect all input files.

**Inputs:**
- `paper_forge_config.json`
- Input files (PDFs, .txt, .md, .tex, figures)

**Decisions:**
- If `provider = custom` and `base_url` is missing → STOP, report error
- If `api_key` is missing and `PAPERFORGE_API_KEY` env var is not set → STOP
- If `scene` is not one of `journal/conference/report/competition` → STOP

**Outputs:**
- Validated `paper_forge_config.json`
- `paper_forge_config.md` (human-readable summary)

---

## Stage 2: Research

**Purpose:** Learn the target scene before writing anything.

**Inputs:**
- `scene` from config
- `research_depth` (`flash` = 3 examples, `pro` = 6 examples)

**Decisions:**
- Do NOT start writing during research
- The scene profile is binding for all later stages
- Common mistakes identified here become audit criteria

**Outputs:**
- `research_dossier.md`

---

## Stage 3: Citation

**Purpose:** Extract every verifiable claim from input materials and assign evidence IDs.

**Inputs:**
- All input files
- Scene profile from Stage 2

**Rules:**
- A claim without an evidence entry CANNOT appear in the final paper
- `weak` support claims must be hedged linguistically in the final text
- If no input files exist, all entries are marked `weak`

**Outputs:**
- `evidence_bank.md`
- `claim_register.md`

---

## Stage 4: Motivation

**Purpose:** Confirm the single central argument that every section must serve.

**Inputs:**
- `evidence_bank.md`
- `scene` from config

**Rules:**
- Generate 3 motivation candidates
- Select the one best supported by strong/moderate evidence
- The confirmed motivation must be a falsifiable, specific claim — not a vague goal
- Do NOT proceed to blueprint until motivation is confirmed

**Outputs:**
- `motivation_candidates.md`
- `confirmed_motivation.md` (with rationale and gap statement)

---

## Stage 5: Blueprint

**Purpose:** Design the section structure so every section serves the motivation.

**Inputs:**
- `confirmed_motivation.md`
- `scene_profile` (typical sections for this scene)
- `claim_register.md`

**Rules:**
- Every section must have a `motivation_link` that connects it to the confirmed motivation
- Word budgets must sum to a realistic total for the scene (journal: 6000-8000w, conference: 4000-6000w, report: 3000-5000w)
- `checks` per section become audit pass/fail criteria

**Outputs:**
- `section_blueprint.md`

---

## Stage 6: Build

**Purpose:** Write each section using only evidence-supported claims.

**Inputs:**
- `section_blueprint.md`
- `evidence_bank.md`
- `claim_register.md`
- `confirmed_motivation.md`

**Rules per section:**
1. Pull relevant claims and evidence entries for this section
2. Write the body (no heading — added at assembly)
3. Record a rationale matrix entry BEFORE moving to the next section
4. Never write a claim not traceable to an evidence entry
5. Stay within ±50% of the word budget

**Outputs:**
- Section texts (held in run state)
- `writing_rationale_matrix.md`

---

## Stage 7: Audit

**Purpose:** Verify the manuscript is complete and evidence-compliant.

**Inputs:**
- All intermediate artifacts
- Final section texts

**Checks:**
- Required artifacts present (see artifact_check.py)
- Evidence bank ≥ 5 entries
- Claim register ≥ 3 entries
- Rationale matrix entry for every section
- No unsupported claims detected in final text
- Motivation referenced in Introduction and Conclusion
- Section count matches blueprint

**Score:** 0–100. Below 60 → re-run build with expanded evidence bank.

**Outputs:**
- `revision_audit.md`

---

## Stage 8: Assembly

**Purpose:** Produce final_paper/ from all sections.

**Inputs:**
- Section texts from run state
- `section_blueprint.md`
- `evidence_bank.md`

**Outputs:**
```
final_paper/
  main.tex          ← LaTeX manuscript
  references.bib    ← BibTeX from evidence bank
  draft.md          ← Markdown draft
  paper.pdf         ← if LaTeX compiler available
```

---

## Stage 9: Translate (optional)

**Triggers only when:** `output_language = "English"` AND `translation_package = true`

**Translates ALL of:**
- `confirmed_motivation.md`
- `section_blueprint.md`
- `writing_rationale_matrix.md`
- Every section in `final_paper/draft.md`

**Output:** `translation_package/` directory with `*_zh.md` files.

---

## Artifact manifest

After a complete Build run, `artifact_check.py` should report 100% required artifacts:

| Artifact | Stage |
|---|---|
| `paper_forge_config.json` | 1 — Intake |
| `research_dossier.md` | 2 — Research |
| `evidence_bank.md` | 3 — Citation |
| `claim_register.md` | 3 — Citation |
| `confirmed_motivation.md` | 4 — Motivation |
| `section_blueprint.md` | 5 — Blueprint |
| `writing_rationale_matrix.md` | 6 — Build |
| `revision_audit.md` | 7 — Audit |
| `final_paper/main.tex` | 8 — Assembly |
| `final_paper/references.bib` | 8 — Assembly |
| `final_paper/draft.md` | 8 — Assembly |
