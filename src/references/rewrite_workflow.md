# PaperForge — Rewrite Workflow Reference

This document describes the Rewrite Existing workflow.
Use this when you have a manuscript that needs structural improvement, not just sentence polishing.

---

## Overview

```
intake → research → citation → motivation → blueprint → rewrite → audit → assembly → [translate]
```

**When to use Rewrite:**
- You have a draft that argues correctly but is structured poorly
- You have a draft with good material but missing or weak motivation
- You want to bring an existing paper up to the standards of a specific scene (journal → top venue)
- You have a paper rejected with reviewer comments you want to address

**Difference from Build:**
- Build starts from fragments and constructs sections from scratch
- Rewrite preserves the original where structurally sound and restructures where it isn't

---

## Stage 1–4: Same as Build

Intake, Research, Citation, and Motivation run identically.

**Key difference at Citation:** The citation skill also scans the ORIGINAL manuscript to identify:
- Claims already present and supported → keep, strengthen
- Claims present but unsupported → flag for removal or evidence search
- Evidence in the materials not used in the original → new opportunities

---

## Stage 5: Blueprint (Rewrite mode)

**Purpose:** Map the original manuscript structure against the ideal structure for the target scene.

**Inputs:**
- Original manuscript text
- `confirmed_motivation.md`
- Scene profile typical sections

**Additional decisions in Rewrite mode:**
- For each original section: does it exist in the ideal structure? → keep / merge / split / remove
- For each ideal section: is there original content to draw from? → preserve / expand / write fresh
- Record the mapping in `rewrite_matrix.md`

**Outputs:**
- `section_blueprint.md` (target structure)
- Preliminary `rewrite_matrix.md` (structure mapping)

---

## Stage 6: Rewrite

**Purpose:** Rewrite each section, fixing argument structure before fixing prose.

**Rewrite priority order:**
1. **Remove** — sections or paragraphs that argue against the motivation or are off-topic
2. **Restructure** — sections with correct content in wrong logical order
3. **Expand** — sections with correct structure but insufficient evidence
4. **Strengthen** — sections with correct evidence but weak claims
5. **Polish** — prose-level improvements (last, not first)

**Rules per section:**
1. Read the original section content
2. Check which claims survive (traceable to evidence bank) vs must be cut
3. Rewrite the section guided by `motivation_link` and surviving evidence
4. Record the rewrite decision in the rewrite matrix: what changed and why
5. Do NOT preserve original sentences purely for length — cut cleanly

**What counts as structural (fix first) vs cosmetic (fix last):**
- Structural: logical ordering, claim placement, gap-motivation connection, evidence linking
- Cosmetic: word choice, sentence rhythm, active/passive voice, transition phrases

**Outputs:**
- Rewritten section texts (held in run state)
- `writing_rationale_matrix.md`
- `rewrite_matrix.md` (complete)

---

## Stage 7–9: Same as Build

Audit, Assembly, and Translate run identically to the Build workflow.

---

## Rewrite matrix schema

```json
{
  "section_id": "S02",
  "title": "Introduction",
  "original_status": "present",
  "structural_changes": "Moved gap statement from paragraph 4 to paragraph 2; removed unsupported claim about dataset size",
  "claims_removed": ["C005"],
  "claims_added": [],
  "motivation_link": "Now opens directly with the gap, leading into the confirmed motivation",
  "evidence_used": ["E001", "E004"],
  "preserve_ratio": 0.6,
  "word_count_approx": 380
}
```

`preserve_ratio` — fraction of the original section text preserved (0 = fully rewritten, 1 = unchanged).

---

## Common rewrite failure modes

| Failure | Symptom | Correct action |
|---|---|---|
| Cosmetic-only rewrite | Original weak argument preserved, sentences rephrased | Identify the structural flaw first; restructure before rephrasing |
| Over-preservation | Unsupported claims kept because they sound good | Check every claim against the evidence bank; cut if unsupported |
| Motivation drift | Rewritten Introduction argues something slightly different than confirmed_motivation | Re-read `confirmed_motivation.md` before each section |
| Gap disappears | Rewrite smooths over the gap the paper fills | Gap statement must survive the rewrite verbatim or strengthened |
| Lost evidence | Rewrite removes a paragraph that contained the only strong result | Check evidence_ids before cutting; preserve claims with strong support |
