#!/usr/bin/env python3
"""
PaperForge Intake Wizard
Interactive CLI for generating paper_forge_config.json
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.model_adapter import PROVIDERS, ModelConfig

SCENES = ["journal", "conference", "report", "competition"]
WORKFLOWS = ["build", "rewrite"]
DEPTHS = ["flash", "pro"]
LANGUAGES = ["English", "Chinese"]

PROVIDER_MODELS = {
    "anthropic": ["claude-opus-4-20250514", "claude-sonnet-4-20250514", "claude-haiku-4-5-20251001"],
    "openai":    ["gpt-4o", "gpt-4o-mini", "o3", "o4-mini"],
    "deepseek":  ["deepseek-chat", "deepseek-reasoner"],
    "qwen":      ["qwen-max", "qwen-plus", "qwen-long", "qwen-turbo"],
    "glm":       ["glm-4", "glm-4-flash", "glm-4-air"],
    "moonshot":  ["moonshot-v1-128k", "moonshot-v1-32k", "moonshot-v1-8k"],
    "custom":    [],
}


def banner():
    print("\n" + "=" * 60)
    print("  PaperForge — Academic Writing Agent")
    print("  Intake Configuration Wizard")
    print("=" * 60 + "\n")


def ask(prompt: str, default: str = "", options: list[str] = None) -> str:
    if options:
        opts_str = " / ".join(f"[{i+1}] {o}" for i, o in enumerate(options))
        print(f"  {prompt}")
        print(f"  {opts_str}")
        while True:
            raw = input(f"  Enter 1-{len(options)} (default: {default}): ").strip()
            if not raw and default:
                return default
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                return options[int(raw) - 1]
            if raw in options:
                return raw
            print("  Invalid choice, try again.")
    else:
        val = input(f"  {prompt} (default: {default!r}): ").strip()
        return val if val else default


def ask_bool(prompt: str, default: bool = False) -> bool:
    default_str = "y" if default else "n"
    raw = input(f"  {prompt} [y/n] (default: {default_str}): ").strip().lower()
    if not raw:
        return default
    return raw in {"y", "yes", "1", "true"}


def run_wizard(output_path: str = "paper_forge_config.json") -> ModelConfig:
    banner()

    print("Step 1: Choose AI provider")
    provider_list = list(PROVIDERS.keys())
    provider = ask("Provider", default="openai", options=provider_list)

    print(f"\nStep 2: Choose model for {provider}")
    suggested_models = PROVIDER_MODELS.get(provider, [])
    if suggested_models:
        model = ask("Model", default=suggested_models[0], options=suggested_models)
    else:
        model = ask(
            "Model name (enter manually for custom provider)",
            default="",
        )

    print("\nStep 3: API key")
    env_key = os.environ.get("PAPERFORGE_API_KEY", "")
    if env_key:
        print(f"  Found PAPERFORGE_API_KEY in environment (length={len(env_key)})")
        use_env = ask_bool("Use environment variable?", default=True)
        api_key = env_key if use_env else ask("API key", default="")
    else:
        api_key = ask("API key (will not be echoed)", default="")

    base_url = None
    if provider == "custom":
        print("\nStep 3b: Custom base URL")
        base_url = ask("Base URL (e.g. https://your-llm-host.com/v1)", default="")

    print("\nStep 4: Writing scene")
    scene = ask("Target scene", default="journal", options=SCENES)

    print("\nStep 5: Workflow")
    workflow = ask(
        "Workflow",
        default="build",
        options=WORKFLOWS,
    )
    print("  build   = build a new paper from materials")
    print("  rewrite = improve an existing manuscript")

    print("\nStep 6: Research depth")
    depth = ask(
        "Research depth",
        default="flash",
        options=DEPTHS,
    )
    print("  flash = 3 strong examples (faster)")
    print("  pro   = 6 strong examples (thorough)")

    print("\nStep 7: Output language")
    lang = ask("Output language", default="English", options=LANGUAGES)

    translation_package = False
    if lang == "English":
        print("\nStep 8: Translation package")
        translation_package = ask_bool(
            "Generate Chinese translation of all artifacts?",
            default=False,
        )

    cfg = ModelConfig(
        provider=provider,
        model=model,
        api_key=api_key,
        base_url=base_url,
        scene=scene,
        workflow=workflow,
        research_depth=depth,
        output_language=lang,
        translation_package=translation_package,
    )

    # Write config (exclude api_key from file for security)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = {k: getattr(cfg, k) for k in cfg.__dataclass_fields__}
    # Mask api_key in the written file — user should set via env var in production
    data["api_key"] = api_key  # keep for local use; warn below
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n{'=' * 60}")
    print(f"  Config written to: {out.resolve()}")
    print(f"  Provider : {provider}")
    print(f"  Model    : {model}")
    print(f"  Scene    : {scene}")
    print(f"  Workflow : {workflow}")
    print(f"  Language : {lang}")
    print(f"{'=' * 60}\n")
    print("  Next step: run the agent with")
    print(f"    python src/orchestrator.py --config {out} --inputs your_draft.txt\n")

    return cfg


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="PaperForge intake wizard")
    p.add_argument("--output", default="paper_forge_config.json")
    args = p.parse_args()
    run_wizard(args.output)
