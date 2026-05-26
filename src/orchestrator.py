"""
PaperScholar Orchestrator
Complete academic writing workflow combining:
- PaperForge: evidence-bank discipline, scene profiles, claim auditing
- PaperSpine: blueprint-first structural workflow
- PaperMind: Chinese tutor mode, AI-tone removal, rebuttal, Web UI
"""
from __future__ import annotations
import json, os, time, sys, argparse
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent / "core"))
sys.path.insert(0, str(Path(__file__).parent / "prompts"))

from model_adapter import ModelClient, ModelConfig
from prompts import (
    TUTOR_MAP, POLISH_REMOVE_AI_TONE, POLISH_ACADEMIC,
    RESEARCH_ANALYZE, INNOVATION_CHECK, REBUTTAL_GENERATE,
    CITATION_BUILD, BLUEPRINT_BUILD, CN_TEMPLATES, PAPER_DECONSTRUCT
)

# ---------------------------------------------------------------------------
# Scene profiles (from PaperForge, extended with CN scenes)
# ---------------------------------------------------------------------------
SCENE_PROFILES = {
    "journal": {
        "abstract_structure": "Background → Gap → Method → Result → Significance",
        "citation_density": "high",
        "typical_sections": ["Abstract","Introduction","Related Work","Method","Experiments","Discussion","Conclusion"],
        "style_notes": "Formal, precise, hedging required for unverified claims, passive voice acceptable",
        "min_references": 30,
    },
    "conference": {
        "abstract_structure": "Problem → Approach → Key Result",
        "citation_density": "medium-high",
        "typical_sections": ["Abstract","Introduction","Related Work","Approach","Evaluation","Conclusion"],
        "style_notes": "Concise, results-forward, page limit critical, figures carry weight",
        "min_references": 20,
    },
    "report": {
        "abstract_structure": "Objective → Method → Findings → Recommendations",
        "citation_density": "medium",
        "typical_sections": ["Executive Summary","Introduction","Background","Methodology","Results","Discussion","Recommendations"],
        "style_notes": "Audience-aware, section completeness critical, conclusions actionable",
        "min_references": 10,
    },
    "competition": {
        "abstract_structure": "Problem → Model → Key Result → Innovation",
        "citation_density": "low-medium",
        "typical_sections": ["Abstract","Problem Restatement","Assumptions","Model Building","Solution","Sensitivity Analysis","Strengths/Weaknesses"],
        "style_notes": "Abstract must be self-contained, sensitivity analysis mandatory",
        "min_references": 10,
    },
    "thesis": CN_TEMPLATES["thesis"],
    "proposal": CN_TEMPLATES["proposal"],
}

# ---------------------------------------------------------------------------
# Shared run state
# ---------------------------------------------------------------------------
class RunState:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.config: Optional[ModelConfig] = None
        self.raw_inputs: list[Path] = []
        self.scene_profile: dict = {}
        self.motivation: str = ""
        self.evidence_bank: list[dict] = []
        self.claim_register: list[dict] = []
        self.section_blueprint: list[dict] = []
        self.rationale_matrix: list[dict] = []
        self.final_sections: dict[str, str] = {}
        self.audit_report: dict = {}
        self.tutor_report: str = ""
        self.innovation_report: str = ""
        self.logs: list[str] = []

    def log(self, msg: str) -> None:
        ts = time.strftime("%H:%M:%S")
        entry = f"[{ts}] {msg}"
        print(entry)
        self.logs.append(entry)

    def write(self, filename: str, content: str) -> Path:
        path = self.output_dir / filename
        path.write_text(content, encoding="utf-8")
        self.log(f"✅ Written: {filename}")
        return path

    def write_json(self, filename: str, data) -> Path:
        return self.write(filename, json.dumps(data, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Skill modules
# ---------------------------------------------------------------------------
class IntakeSkill:
    REQUIRED = ["provider", "api_key", "scene", "workflow"]

    def run(self, state: RunState, config_path: Path, input_paths: list[Path]) -> None:
        state.log("=== 📋 INTAKE ===")
        cfg = ModelConfig.from_json(str(config_path))
        for f in self.REQUIRED:
            if not getattr(cfg, f, None):
                raise ValueError(f"Config missing required field: {f}")
        state.config = cfg
        state.raw_inputs = [p for p in input_paths if p.exists()]
        state.log(f"Provider: {cfg.provider} / {cfg.model}")
        state.log(f"Scene: {cfg.scene} | Workflow: {cfg.workflow} | Language: {cfg.output_language}")
        state.log(f"Input files: {len(state.raw_inputs)}")
        state.write_json("paperscholar_config.json", {
            k: getattr(cfg, k) for k in cfg.__dataclass_fields__ if k != "api_key"
        })


class ResearchSkill:
    """Learn the target scene before writing anything (PaperForge discipline)."""
    def run(self, state: RunState, client: ModelClient) -> None:
        state.log("=== 🔬 RESEARCH ===")
        scene = state.config.scene
        profile = SCENE_PROFILES.get(scene, SCENE_PROFILES["journal"])
        state.scene_profile = profile

        depth = state.config.research_depth
        n_examples = 3 if depth == "flash" else 6

        # Analyze input materials
        if state.raw_inputs:
            materials = "\n\n".join(p.read_text(encoding="utf-8", errors="ignore")[:3000] for p in state.raw_inputs[:4])
            analysis = client.chat(RESEARCH_ANALYZE, f"分析以下材料，场景：{scene}\n\n{materials}")
        else:
            analysis = f"场景：{scene}\n目标：{profile.get('style_notes','')}"

        dossier = f"# Research Dossier\n\n## Scene: {scene}\n\n{json.dumps(profile, ensure_ascii=False, indent=2)}\n\n## Material Analysis\n\n{analysis}"
        state.write("research_dossier.md", dossier)


class CitationSkill:
    """Extract claims from input materials and build evidence bank (PaperForge core)."""
    def run(self, state: RunState, client: ModelClient) -> None:
        state.log("=== 📚 CITATION / EVIDENCE BANK ===")
        if not state.raw_inputs:
            state.evidence_bank = []
            state.write("evidence_bank.md", "# Evidence Bank\n\n_No input materials provided._")
            return

        all_text = "\n\n---\n\n".join(
            f"[Source: {p.name}]\n{p.read_text(encoding='utf-8', errors='ignore')[:4000]}"
            for p in state.raw_inputs[:6]
        )
        raw = client.chat(CITATION_BUILD, all_text)
        # Try to parse JSON; fall back to raw text
        try:
            clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
            state.evidence_bank = json.loads(clean)
        except Exception:
            state.evidence_bank = []

        md_lines = ["# Evidence Bank\n"]
        for e in state.evidence_bank:
            flag = f" ⚠️ {e.get('flag','')}" if e.get("flag") else ""
            md_lines.append(f"## {e.get('id','?')} [{e.get('confidence','?')}]{flag}")
            md_lines.append(f"**Claim:** {e.get('claim','')}")
            md_lines.append(f"**Source:** {e.get('source','')}\n")

        state.write("evidence_bank.md", "\n".join(md_lines))
        state.log(f"Evidence bank: {len(state.evidence_bank)} entries")


class BlueprintSkill:
    """Build section blueprint with writing motivation per section (PaperSpine workflow)."""
    def run(self, state: RunState, client: ModelClient) -> None:
        state.log("=== 🗺️ BLUEPRINT ===")
        profile = state.scene_profile
        evidence_summary = json.dumps(state.evidence_bank[:20], ensure_ascii=False) if state.evidence_bank else "None"
        
        cn_note = ""
        if state.config.output_language == "Chinese" and state.config.cn_scene:
            cn_tmpl = CN_TEMPLATES.get(state.config.cn_scene, {})
            cn_note = f"\n\nChinese scene template:\n{json.dumps(cn_tmpl, ensure_ascii=False)}"

        prompt = f"""Scene: {state.config.scene}
Style: {profile.get('style_notes','')}
Sections: {profile.get('typical_sections',[])}
Evidence bank (first 20 entries): {evidence_summary}
Motivation: {state.motivation or 'To be confirmed by user'}{cn_note}

Build a detailed section blueprint. Every claim must reference an evidence ID."""
        
        blueprint_md = client.chat(BLUEPRINT_BUILD, prompt)
        state.write("section_blueprint.md", f"# Section Blueprint\n\n{blueprint_md}")
        state.log("Blueprint written")


class BuildSkill:
    """Write each section using blueprint + evidence bank (PaperForge rationale matrix)."""
    def run(self, state: RunState, client: ModelClient) -> None:
        state.log("=== ✍️ BUILD ===")
        profile = state.scene_profile
        sections = profile.get("typical_sections", ["Introduction","Method","Results","Conclusion"])
        rationale = []

        for sec in sections:
            state.log(f"  Writing: {sec}")
            evidence_ids = [e["id"] for e in state.evidence_bank[:10]]
            user_prompt = f"""Write the '{sec}' section.
Scene: {state.config.scene}
Style: {profile.get('style_notes','')}
Available evidence IDs: {evidence_ids}
Blueprint guidance: (see section_blueprint.md)
Motivation: {state.motivation}

Rules:
- Every claim must cite an evidence ID in brackets: [E001]
- No unsourced absolute statements
- Output language: {state.config.output_language}
"""
            system = f"You are an expert academic writer for {state.config.scene} papers. Follow evidence-bank discipline strictly."
            content = client.chat(system, user_prompt)
            state.final_sections[sec] = content
            rationale.append({"section": sec, "function": f"Core {sec} for {state.config.scene}", "evidence_used": evidence_ids[:3]})

        # Assemble full draft
        draft = "\n\n".join(f"## {k}\n\n{v}" for k, v in state.final_sections.items())
        state.write("draft_full.md", f"# Draft\n\n{draft}")
        state.write_json("writing_rationale_matrix.json", rationale)
        state.log(f"Draft complete: {len(sections)} sections")


class TutorSkill:
    """Simulate strict academic mentor review (PaperMind core feature)."""
    def run(self, state: RunState, client: ModelClient, text: Optional[str] = None) -> None:
        state.log("=== 👨‍🏫 TUTOR REVIEW ===")
        if text is None:
            draft_path = state.output_dir / "draft_full.md"
            text = draft_path.read_text(encoding="utf-8") if draft_path.exists() else ""
        if not text.strip():
            state.tutor_report = "_No draft to review._"
            state.write("tutor_review.md", state.tutor_report)
            return
        
        tutor_style = getattr(state.config, "tutor_style", "strict")
        system = TUTOR_MAP.get(tutor_style, TUTOR_MAP["strict"])
        review = client.chat(system, f"请审查以下论文内容：\n\n{text[:6000]}")
        state.tutor_report = review
        state.write("tutor_review.md", f"# Tutor Review ({tutor_style})\n\n{review}")


class AiToneSkill:
    """Detect and remove AI-generated tone (PaperMind differentiator)."""
    def run(self, state: RunState, client: ModelClient, text: Optional[str] = None) -> str:
        state.log("=== 🔍 AI TONE CHECK ===")
        if text is None:
            draft_path = state.output_dir / "draft_full.md"
            text = draft_path.read_text(encoding="utf-8") if draft_path.exists() else ""
        result = client.chat(POLISH_REMOVE_AI_TONE, text[:5000])
        state.write("ai_tone_check.md", f"# AI Tone Check\n\n{result}")
        return result


class InnovationSkill:
    """Check novelty of research claims (PaperMind)."""
    def run(self, state: RunState, client: ModelClient, abstract: str = "") -> None:
        state.log("=== 💡 INNOVATION CHECK ===")
        text = abstract or state.motivation or ""
        if not text.strip():
            state.write("innovation_check.md", "# Innovation Check\n\n_No abstract/motivation provided._")
            return
        result = client.chat(INNOVATION_CHECK, f"评估以下研究的创新性：\n\n{text}")
        state.innovation_report = result
        state.write("innovation_check.md", f"# Innovation Check\n\n{result}")


class AuditSkill:
    """Audit final paper against evidence bank (PaperForge discipline)."""
    def run(self, state: RunState, client: ModelClient) -> None:
        state.log("=== 🔎 AUDIT ===")
        draft_path = state.output_dir / "draft_full.md"
        if not draft_path.exists():
            state.log("No draft to audit.")
            return
        draft = draft_path.read_text(encoding="utf-8")
        evidence_ids = [e["id"] for e in state.evidence_bank]
        system = """You are a rigorous academic auditor. Check the draft for:
1. Claims without evidence IDs → flag as UNSOURCED
2. Evidence IDs cited but not in evidence bank → flag as PHANTOM
3. Sections missing from the blueprint → flag as MISSING
4. AI tone phrases (Furthermore, It is worth noting, etc.) → flag as AI_TONE
Output a structured audit report in Markdown."""
        user = f"Evidence bank IDs: {evidence_ids}\n\nDraft (first 5000 chars):\n{draft[:5000]}"
        report = client.chat(system, user)
        state.audit_report = {"report": report}
        state.write("revision_audit.md", f"# Revision Audit\n\n{report}")


class TranslateSkill:
    """Build bilingual translation package (PaperForge + PaperMind)."""
    def run(self, state: RunState, client: ModelClient) -> None:
        if not state.config.translation_package:
            return
        state.log("=== 🌐 TRANSLATION ===")
        draft_path = state.output_dir / "draft_full.md"
        if not draft_path.exists():
            return
        draft = draft_path.read_text(encoding="utf-8")
        direction = "Chinese→English" if state.config.output_language == "Chinese" else "English→Chinese"
        system = f"You are a professional academic translator ({direction}). Maintain academic register, field-specific terminology. Provide parallel bilingual output."
        translated = client.chat(system, f"Translate the following academic draft:\n\n{draft[:5000]}")
        state.write("translation_package.md", f"# Translation Package ({direction})\n\n{translated}")


class RebuttalSkill:
    """Generate reviewer rebuttal (PaperMind exclusive)."""
    def run(self, state: RunState, client: ModelClient, reviewer_comments: str) -> str:
        state.log("=== 📝 REBUTTAL ===")
        result = client.chat(REBUTTAL_GENERATE, f"Reviewer意见：\n\n{reviewer_comments}")
        state.write("rebuttal.md", f"# Rebuttal Draft\n\n{result}")
        return result


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------
class PaperScholarOrchestrator:
    def __init__(self, config_path: Path, output_dir: Path, input_paths: list[Path]):
        self.config_path = config_path
        self.output_dir = output_dir
        self.input_paths = input_paths
        self.state = RunState(output_dir)

    def run(self, skill: Optional[str] = None, reviewer: Optional[str] = None) -> RunState:
        # Intake
        IntakeSkill().run(self.state, self.config_path, self.input_paths)
        client = ModelClient(self.state.config)

        if skill == "tutor":
            TutorSkill().run(self.state, client)
            return self.state
        if skill == "rebuttal" and reviewer:
            RebuttalSkill().run(self.state, client, reviewer)
            return self.state
        if skill == "ai_tone":
            AiToneSkill().run(self.state, client)
            return self.state
        if skill == "innovation":
            InnovationSkill().run(self.state, client)
            return self.state

        # Full workflow
        ResearchSkill().run(self.state, client)
        CitationSkill().run(self.state, client)
        BlueprintSkill().run(self.state, client)

        if self.state.config.workflow == "build":
            BuildSkill().run(self.state, client)
        else:
            # Rewrite: treat first input as draft
            if self.state.raw_inputs:
                draft = self.state.raw_inputs[0].read_text(encoding="utf-8", errors="ignore")
                system = "You are an expert academic editor. Rewrite the draft following the evidence-bank discipline: every claim must have a source."
                rewritten = client.chat(system, f"Scene: {self.state.config.scene}\n\nDraft:\n{draft[:6000]}")
                self.state.write("draft_full.md", rewritten)

        # Post-processing
        TutorSkill().run(self.state, client)
        AiToneSkill().run(self.state, client)
        InnovationSkill().run(self.state, client)
        AuditSkill().run(self.state, client)
        TranslateSkill().run(self.state, client)

        # Run script-based checks
        self._run_artifact_check()

        # Final log summary
        self.state.log("=== ✅ COMPLETE ===")
        outputs = list(self.output_dir.glob("*.md")) + list(self.output_dir.glob("*.json"))
        self.state.log(f"Output files: {len(outputs)}")
        return self.state

    def _run_artifact_check(self):
        try:
            import subprocess
            check_script = Path(__file__).parent / "scripts" / "artifact_check.py"
            if check_script.exists():
                subprocess.run(["python", str(check_script), str(self.output_dir), "--markdown", "--write"],
                               capture_output=True, timeout=30)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PaperScholar — Academic Writing AI Workflow")
    parser.add_argument("--config", required=True, help="Path to paperscholar_config.json")
    parser.add_argument("--inputs", nargs="*", default=[], help="Input files (PDFs, txt, md)")
    parser.add_argument("--output", default="paperscholar_output", help="Output directory")
    parser.add_argument("--skill", default=None, help="Run single skill: tutor|rebuttal|ai_tone|innovation")
    parser.add_argument("--reviewer", default=None, help="Reviewer comments (for rebuttal skill)")
    args = parser.parse_args()

    orchestrator = PaperScholarOrchestrator(
        config_path=Path(args.config),
        output_dir=Path(args.output),
        input_paths=[Path(p) for p in args.inputs],
    )
    orchestrator.run(skill=args.skill, reviewer=args.reviewer)
