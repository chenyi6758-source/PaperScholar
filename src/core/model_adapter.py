"""
PaperScholar Model Adapter
Unified interface combining PaperForge robustness + PaperMind intelligent task routing.
Providers: Anthropic, OpenAI, DeepSeek, Qwen, GLM, Moonshot, Doubao, Custom
"""
from __future__ import annotations
import os, json, time
from typing import Optional
from dataclasses import dataclass

try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False
    OpenAI = None

PROVIDERS: dict[str, dict] = {
    "anthropic": {"base_url": "https://api.anthropic.com/v1",   "default_model": "claude-sonnet-4-20250514", "strengths": ["logic","latex","audit","rewrite","structure"]},
    "openai":    {"base_url": "https://api.openai.com/v1",      "default_model": "gpt-4o",                  "strengths": ["writing","polish","translation","general"]},
    "deepseek":  {"base_url": "https://api.deepseek.com/v1",    "default_model": "deepseek-chat",           "strengths": ["logic","code","audit","budget","citation"]},
    "qwen":      {"base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1","default_model":"qwen-max","strengths":["chinese","long_context","research","summary"]},
    "glm":       {"base_url": "https://open.bigmodel.cn/api/paas/v4","default_model":"glm-4",               "strengths": ["chinese","academic","tutor"]},
    "moonshot":  {"base_url": "https://api.moonshot.cn/v1",     "default_model": "moonshot-v1-128k",        "strengths": ["long_context","pdf_reading","research"]},
    "doubao":    {"base_url": "https://ark.cn-beijing.volces.com/api/v3","default_model":"doubao-pro-32k",  "strengths": ["speed","budget","summary","chinese"]},
    "custom":    {"base_url": None,                             "default_model": None,                      "strengths": []},
}

TASK_ROUTING: dict[str, list[str]] = {
    "research":    ["moonshot","qwen","openai","deepseek"],
    "citation":    ["deepseek","anthropic","openai"],
    "blueprint":   ["anthropic","deepseek","openai"],
    "build":       ["anthropic","openai","deepseek"],
    "rewrite":     ["anthropic","openai","deepseek"],
    "tutor":       ["anthropic","glm","openai","deepseek"],
    "polish":      ["openai","anthropic","deepseek"],
    "ai_tone":     ["deepseek","anthropic","openai"],
    "translation": ["qwen","openai","glm"],
    "audit":       ["anthropic","deepseek","openai"],
    "rebuttal":    ["anthropic","openai","deepseek"],
    "innovation":  ["anthropic","deepseek","openai"],
    "summary":     ["doubao","qwen","moonshot"],
    "latex":       ["anthropic","deepseek","openai"],
}

@dataclass
class ModelConfig:
    provider: str = "openai"
    model: str = "gpt-4o"
    api_key: str = ""
    base_url: Optional[str] = None
    temperature: float = 0.3
    max_tokens: int = 8192
    timeout: int = 120
    max_retries: int = 3
    retry_delay: float = 2.0
    scene: str = "journal"
    workflow: str = "build"
    research_depth: str = "flash"
    output_language: str = "Chinese"
    translation_package: bool = False
    tutor_style: str = "strict"
    cn_scene: str = ""

    @classmethod
    def from_json(cls, path: str) -> "ModelConfig":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not data.get("api_key"):
            env_key = os.environ.get("PAPERSCHOLAR_API_KEY") or os.environ.get("PAPERFORGE_API_KEY")
            if env_key:
                data["api_key"] = env_key
        known = set(cls.__dataclass_fields__)
        obj = cls(**{k: v for k, v in data.items() if k in known})
        if obj.base_url is None and obj.provider in PROVIDERS:
            obj.base_url = PROVIDERS[obj.provider]["base_url"]
        if not obj.model and obj.provider in PROVIDERS:
            obj.model = PROVIDERS[obj.provider]["default_model"]
        return obj

class ModelClient:
    def __init__(self, config: ModelConfig):
        if not _OPENAI_AVAILABLE:
            raise ImportError("openai package required: pip install openai")
        self.config = config
        self._client = OpenAI(api_key=config.api_key, base_url=config.base_url, timeout=config.timeout)

    def chat(self, system: str, user: str, temperature: Optional[float] = None) -> str:
        temp = temperature if temperature is not None else self.config.temperature
        for attempt in range(self.config.max_retries):
            try:
                resp = self._client.chat.completions.create(
                    model=self.config.model,
                    messages=[{"role":"system","content":system},{"role":"user","content":user}],
                    temperature=temp, max_tokens=self.config.max_tokens)
                return resp.choices[0].message.content or ""
            except Exception as exc:
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (attempt + 1))
                else:
                    raise RuntimeError(f"API call failed: {exc}") from exc
        return ""

    def chat_stream(self, system: str, user: str):
        stream = self._client.chat.completions.create(
            model=self.config.model,
            messages=[{"role":"system","content":system},{"role":"user","content":user}],
            temperature=self.config.temperature, max_tokens=self.config.max_tokens, stream=True)
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
