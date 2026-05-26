"""
PaperScholar Tests
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "core"))
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "prompts"))

from model_adapter import ModelConfig, PROVIDERS, TASK_ROUTING


def test_model_config_defaults():
    cfg = ModelConfig()
    assert cfg.provider == "openai"
    assert cfg.scene == "journal"
    assert cfg.workflow == "build"

def test_providers_have_required_keys():
    for name, info in PROVIDERS.items():
        assert "default_model" in info, f"{name} missing default_model"
        assert "strengths" in info, f"{name} missing strengths"

def test_all_tasks_in_routing():
    tasks = ["research","citation","blueprint","build","rewrite","tutor","polish",
             "ai_tone","translation","audit","rebuttal","innovation","summary","latex"]
    for t in tasks:
        assert t in TASK_ROUTING, f"Task '{t}' missing from TASK_ROUTING"

def test_model_config_from_json(tmp_path):
    cfg_data = {
        "provider": "deepseek",
        "model": "deepseek-chat",
        "api_key": "test-key",
        "scene": "conference",
        "workflow": "rewrite",
    }
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text(json.dumps(cfg_data))
    cfg = ModelConfig.from_json(str(cfg_file))
    assert cfg.provider == "deepseek"
    assert cfg.scene == "conference"
    assert cfg.base_url == PROVIDERS["deepseek"]["base_url"]

def test_tutor_map_has_all_styles():
    from prompts import TUTOR_MAP
    for style in ["strict","neurips","cvpr","acl","nature"]:
        assert style in TUTOR_MAP, f"Tutor style '{style}' missing"

def test_prompts_not_empty():
    from prompts import (POLISH_REMOVE_AI_TONE, POLISH_ACADEMIC,
                         INNOVATION_CHECK, REBUTTAL_GENERATE,
                         CITATION_BUILD, BLUEPRINT_BUILD)
    for prompt in [POLISH_REMOVE_AI_TONE, POLISH_ACADEMIC,
                   INNOVATION_CHECK, REBUTTAL_GENERATE,
                   CITATION_BUILD, BLUEPRINT_BUILD]:
        assert len(prompt.strip()) > 50

def test_cn_templates():
    from prompts import CN_TEMPLATES
    for scene in ["thesis","proposal","competition"]:
        assert scene in CN_TEMPLATES
        assert "sections" in CN_TEMPLATES[scene]

def test_run_state(tmp_path):
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from orchestrator import RunState
    state = RunState(tmp_path)
    state.log("test")
    state.write("test.md", "# Test")
    assert (tmp_path / "test.md").exists()
    assert len(state.logs) == 2  # log + write
