# PaperForge — Scene Style Reference

A binding reference for the four supported scenes.
The build and rewrite skills use this to enforce scene-appropriate structure, tone, and citation density.

---

## Scene: journal

### Abstract structure
```
[Background] Establish the field and prior work.
[Gap]        Identify what is missing or wrong.
[Method]     Describe the proposed approach in one sentence.
[Result]     State the key quantitative finding.
[Significance] Explain why this matters to the field.
```

### Typical sections
1. Abstract
2. Introduction (gap + motivation + contributions)
3. Related Work (organized by theme, not chronology)
4. Method / Approach
5. Experiments / Evaluation
6. Results and Discussion
7. Conclusion (restate contribution, not just summary)
8. References

### Citation style
- Numeric (IEEE) or author-year (APA/NeurIPS) depending on venue
- Citation density: high (8–20 citations per page)
- Every factual claim requires a citation
- Self-citation ≤ 20% of total references

### Tone and style
- Formal, third person preferred
- Passive voice acceptable for method description
- Hedging required for unverified claims: "we hypothesize", "results suggest"
- No colloquialisms, no first-person evaluation ("our method is great")

### Common mistakes
1. Abstract that summarizes sections instead of results
2. Introduction that motivates the general field but not this specific paper
3. Related Work organized chronologically instead of thematically
4. Missing ablation study or baseline comparisons
5. Conclusion that repeats the abstract word for word

---

## Scene: conference

### Abstract structure
```
[Problem]   One sentence: what problem does this solve?
[Approach]  One sentence: what is the key idea?
[Result]    One number or qualitative result that proves it works.
```

### Typical sections
1. Abstract (≤ 200 words, results-first)
2. Introduction (problem, why hard, why now, contributions)
3. Related Work (brief, may be merged with Introduction)
4. Method
5. Evaluation (or Experiments)
6. Conclusion
7. References

### Citation style
- Typically numeric (ACL, IEEE, NeurIPS, ICML formats)
- Citation density: medium-high (5–15 per page)
- Related Work citations denser than other sections

### Tone and style
- Concise and direct — every sentence earns its place
- Page limits are hard constraints; cut ruthlessly
- Figures and tables must carry as much weight as text
- Contributions should be listed explicitly in Introduction

### Common mistakes
1. Introduction that spends too long on background before stating the problem
2. Related Work that praises prior work without establishing the gap
3. Method section that explains implementation details before the algorithm
4. Evaluation section missing baselines that reviewers will ask about
5. Conclusion longer than Abstract

---

## Scene: report

### Abstract structure (Executive Summary)
```
[Purpose]        Why was this report written?
[Scope]          What was covered and what was not?
[Key Findings]   2–3 main findings, stated plainly.
[Recommendations] 1–2 action items or next steps.
```

### Typical sections
1. Executive Summary
2. Introduction / Background
3. Scope and Methodology
4. Findings (organized by theme or question)
5. Analysis and Discussion
6. Recommendations
7. Conclusion
8. References / Bibliography
9. Appendices (optional)

### Citation style
- Author-year (APA) or Chicago
- Citation density: medium (3–8 per page)
- Less dense than journal; more dense than competition

### Tone and style
- Audience may be non-expert — define technical terms on first use
- Active voice preferred for recommendations ("We recommend..." not "It is recommended...")
- Findings and recommendations must be explicitly labeled, not implied
- Tables and figures should be self-explanatory (full captions)

### Common mistakes
1. Executive Summary that is too long or too technical
2. Findings section that describes data without interpreting it
3. Recommendations that are vague ("improve the system")
4. Missing scope statement — reader doesn't know what was NOT covered
5. Appendices that contain critical information not referenced in the body

---

## Scene: competition

### Abstract structure
```
[Innovation]        What is new or unique about this solution?
[Approach]          How does it work at a high level?
[Demonstrated Value] What evidence shows it works (score, demo, benchmark)?
```

### Typical sections
1. Introduction (problem statement + why existing solutions fail)
2. Proposed Solution (innovation framing first)
3. Implementation
4. Evaluation / Results
5. Conclusion

### Citation style
- Minimal; cite only where directly relevant to innovation claim
- Citation density: low-medium (1–5 per page)
- Focus on primary sources and benchmarks, not survey papers

### Tone and style
- Innovation framing is critical — lead with what is new
- Judge rubric items must be mapped explicitly (state which criterion each section addresses)
- Visuals carry disproportionate weight — diagrams and demo screenshots are essential
- Avoid overpromising: judges penalize claims not backed by results

### Common mistakes
1. Introduction that describes the general problem without positioning the innovation
2. Implementation section so detailed it obscures the core idea
3. Results section missing comparison to the competition baseline or leaderboard
4. No explicit mapping to the scoring rubric
5. Conclusion that repeats the introduction without adding outcome evidence

---

## Cross-scene rules (apply to all)

- The confirmed motivation must appear explicitly in the Introduction (first or second paragraph)
- The gap statement must appear before the proposed solution
- Every claim in every scene must be traceable to the evidence bank
- Weak-support claims must be hedged regardless of scene
- The final section (Conclusion or Recommendations) must circle back to the confirmed motivation
