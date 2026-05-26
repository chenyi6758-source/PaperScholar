"""
PaperScholar Web UI
Gradio-based visual interface — no coding required.
Combines PaperMind's UI with PaperForge's evidence discipline.
"""
import json, os, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "core"))
sys.path.insert(0, str(Path(__file__).parent / "prompts"))

try:
    import gradio as gr
except ImportError:
    print("Install Gradio first: pip install gradio")
    sys.exit(1)

from model_adapter import ModelConfig, ModelClient, PROVIDERS
from prompts import (TUTOR_MAP, POLISH_REMOVE_AI_TONE, POLISH_ACADEMIC,
                     INNOVATION_CHECK, REBUTTAL_GENERATE, CITATION_BUILD,
                     BLUEPRINT_BUILD, PAPER_DECONSTRUCT)

# ---------------------------------------------------------------------------
# Core helper
# ---------------------------------------------------------------------------
def build_client(provider, api_key, model=""):
    cfg = ModelConfig(
        provider=provider,
        api_key=api_key,
        model=model or PROVIDERS.get(provider, {}).get("default_model", "gpt-4o"),
    )
    return ModelClient(cfg)

def safe_run(fn, *args):
    try:
        return fn(*args)
    except Exception as e:
        return f"❌ 错误: {str(e)}"

# ---------------------------------------------------------------------------
# Feature functions
# ---------------------------------------------------------------------------
def tutor_review(text, provider, api_key, model, tutor_style):
    if not text.strip(): return "❌ 请输入论文内容"
    if not api_key.strip(): return "❌ 请输入API Key"
    client = build_client(provider, api_key, model)
    system = TUTOR_MAP.get(tutor_style, TUTOR_MAP["strict"])
    return safe_run(client.chat, system, f"请审查以下论文内容：\n\n{text}")

def remove_ai_tone(text, provider, api_key, model):
    if not text.strip(): return "❌ 请输入文本"
    if not api_key.strip(): return "❌ 请输入API Key"
    client = build_client(provider, api_key, model)
    return safe_run(client.chat, POLISH_REMOVE_AI_TONE, text)

def polish_chinese_english(text, provider, api_key, model):
    if not text.strip(): return "❌ 请输入文本"
    if not api_key.strip(): return "❌ 请输入API Key"
    client = build_client(provider, api_key, model)
    return safe_run(client.chat, POLISH_ACADEMIC, text)

def check_innovation(text, provider, api_key, model):
    if not text.strip(): return "❌ 请输入摘要或创新点描述"
    if not api_key.strip(): return "❌ 请输入API Key"
    client = build_client(provider, api_key, model)
    return safe_run(client.chat, INNOVATION_CHECK, f"请评估以下研究的创新性：\n\n{text}")

def generate_rebuttal(reviewer_text, provider, api_key, model):
    if not reviewer_text.strip(): return "❌ 请输入Reviewer意见"
    if not api_key.strip(): return "❌ 请输入API Key"
    client = build_client(provider, api_key, model)
    return safe_run(client.chat, REBUTTAL_GENERATE, f"Reviewer意见：\n\n{reviewer_text}")

def build_evidence_bank(text, provider, api_key, model):
    if not text.strip(): return "❌ 请输入论文材料"
    if not api_key.strip(): return "❌ 请输入API Key"
    client = build_client(provider, api_key, model)
    return safe_run(client.chat, CITATION_BUILD, text)

def deconstruct_paper(text, provider, api_key, model):
    if not text.strip(): return "❌ 请输入论文内容"
    if not api_key.strip(): return "❌ 请输入API Key"
    client = build_client(provider, api_key, model)
    return safe_run(client.chat, PAPER_DECONSTRUCT, f"请拆解以下论文：\n\n{text}")

def build_blueprint(text, scene, provider, api_key, model):
    if not text.strip(): return "❌ 请输入材料或动机"
    if not api_key.strip(): return "❌ 请输入API Key"
    client = build_client(provider, api_key, model)
    return safe_run(client.chat, BLUEPRINT_BUILD, f"场景：{scene}\n\n材料：\n{text}")

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
PROVIDER_LIST = list(PROVIDERS.keys())
TUTOR_STYLES = ["strict","neurips","cvpr","acl","iclr","nature"]
SCENES = ["journal","conference","report","competition","thesis","proposal"]

CSS = """
.gradio-container { max-width: 1200px !important; }
.tab-nav button { font-size: 15px; font-weight: 600; }
footer { display: none !important; }
"""

def create_ui():
    with gr.Blocks(title="PaperScholar 🎓", css=CSS, theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
# 🎓 PaperScholar
**专为中文科研用户 · 集成 PaperForge × PaperSpine × PaperMind 三大引擎**

证据链约束 · 导师模式 · 去AI腔 · Rebuttal · 论文结构拆解 · 8+ 模型支持
""")

        # Shared provider config in a collapsible accordion
        with gr.Accordion("⚙️ 模型配置（所有功能共用）", open=True):
            with gr.Row():
                provider = gr.Dropdown(PROVIDER_LIST, value="deepseek", label="AI提供商")
                api_key  = gr.Textbox(label="API Key", type="password", placeholder="粘贴你的API Key")
                model    = gr.Textbox(label="模型名称（留空自动选择）", placeholder="e.g. deepseek-chat")

        with gr.Tabs():

            # ── Tab 1: Tutor Review ──────────────────────────────────────
            with gr.Tab("👨‍🏫 导师审查"):
                gr.Markdown("模拟严格导师/顶会审稿人，全面评审你的论文。")
                with gr.Row():
                    tutor_style = gr.Dropdown(TUTOR_STYLES, value="strict", label="导师风格")
                tutor_input  = gr.Textbox(label="论文内容", lines=12, placeholder="粘贴论文段落或全文...")
                tutor_btn    = gr.Button("🔍 开始审查", variant="primary")
                tutor_output = gr.Markdown(label="导师评审报告")
                tutor_btn.click(tutor_review, [tutor_input, provider, api_key, model, tutor_style], tutor_output)

            # ── Tab 2: AI Tone ───────────────────────────────────────────
            with gr.Tab("✨ 去AI腔"):
                gr.Markdown("识别并消除AI生成文本的典型特征，让论文更有人味。")
                with gr.Row():
                    with gr.Column():
                        ai_tone_input  = gr.Textbox(label="原文", lines=10, placeholder="粘贴需要去AI腔的段落...")
                        ai_tone_btn    = gr.Button("🧹 去除AI腔", variant="primary")
                    with gr.Column():
                        ai_tone_output = gr.Markdown(label="检测与修改结果")
                ai_tone_btn.click(remove_ai_tone, [ai_tone_input, provider, api_key, model], ai_tone_output)

            # ── Tab 3: Academic Polish ───────────────────────────────────
            with gr.Tab("🖊️ 学术润色"):
                gr.Markdown("矫正中式英语，提升学术规范性，附中文修改说明。")
                with gr.Row():
                    with gr.Column():
                        polish_input  = gr.Textbox(label="英文原文", lines=10, placeholder="粘贴需要润色的英文段落...")
                        polish_btn    = gr.Button("✨ 学术润色", variant="primary")
                    with gr.Column():
                        polish_output = gr.Markdown(label="润色结果 + 修改说明")
                polish_btn.click(polish_chinese_english, [polish_input, provider, api_key, model], polish_output)

            # ── Tab 4: Innovation Check ──────────────────────────────────
            with gr.Tab("💡 创新性检测"):
                gr.Markdown("评估研究创新度，区分真创新 vs 换皮/调参/换数据集。")
                innov_input  = gr.Textbox(label="摘要或创新点描述", lines=8, placeholder="粘贴论文摘要或创新点...")
                innov_btn    = gr.Button("💡 检测创新性", variant="primary")
                innov_output = gr.Markdown(label="创新性评估报告")
                innov_btn.click(check_innovation, [innov_input, provider, api_key, model], innov_output)

            # ── Tab 5: Rebuttal ──────────────────────────────────────────
            with gr.Tab("📝 Rebuttal生成"):
                gr.Markdown("逐条分析Reviewer意见类型，生成策略性回复。")
                rebuttal_input  = gr.Textbox(label="Reviewer意见", lines=10, placeholder="粘贴Reviewer的全部意见...")
                rebuttal_btn    = gr.Button("✍️ 生成Rebuttal", variant="primary")
                rebuttal_output = gr.Markdown(label="中文分析 + 英文Rebuttal草稿")
                rebuttal_btn.click(generate_rebuttal, [rebuttal_input, provider, api_key, model], rebuttal_output)

            # ── Tab 6: Evidence Bank ─────────────────────────────────────
            with gr.Tab("🏦 证据库构建"):
                gr.Markdown("从原始材料中提取所有可引用的Claim，构建带来源的证据库（PaperForge核心）。")
                evidence_input  = gr.Textbox(label="原始材料", lines=12, placeholder="粘贴论文材料、文献摘要、实验记录...")
                evidence_btn    = gr.Button("🔨 构建证据库", variant="primary")
                evidence_output = gr.Markdown(label="结构化证据库")
                evidence_btn.click(build_evidence_bank, [evidence_input, provider, api_key, model], evidence_output)

            # ── Tab 7: Blueprint ─────────────────────────────────────────
            with gr.Tab("🗺️ 写作蓝图"):
                gr.Markdown("根据场景和材料生成章节蓝图，每节附写作动机。")
                with gr.Row():
                    scene_sel = gr.Dropdown(SCENES, value="journal", label="论文场景")
                blueprint_input  = gr.Textbox(label="材料或动机描述", lines=10, placeholder="粘贴材料摘要或研究动机...")
                blueprint_btn    = gr.Button("🗺️ 生成蓝图", variant="primary")
                blueprint_output = gr.Markdown(label="章节蓝图")
                blueprint_btn.click(build_blueprint, [blueprint_input, scene_sel, provider, api_key, model], blueprint_output)

            # ── Tab 8: Paper Deconstruct ─────────────────────────────────
            with gr.Tab("🔬 论文拆解"):
                gr.Markdown("反向工程顶会论文，提取可复用的写作套路和模板。")
                deconstruct_input  = gr.Textbox(label="目标论文（全文或摘要+引言）", lines=12, placeholder="粘贴顶会论文内容...")
                deconstruct_btn    = gr.Button("🔬 开始拆解", variant="primary")
                deconstruct_output = gr.Markdown(label="拆解报告 + 可复用模板")
                deconstruct_btn.click(deconstruct_paper, [deconstruct_input, provider, api_key, model], deconstruct_output)

        gr.Markdown("""
---
**PaperScholar** · MIT License · [GitHub](https://github.com/your-username/PaperScholar) · 
集成 [PaperForge](https://github.com/your-username/PaperForge) × PaperSpine × [PaperMind](https://github.com/your-username/PaperMind)
""")

    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False,
                inbrowser=True, show_error=True)
