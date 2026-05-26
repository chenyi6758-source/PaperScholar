<div align="center">

# 🎓 PaperScholar

**专为中文科研用户设计的学术写作AI工具链**

*导师模式 · 去AI腔 · 创新点检测 · Rebuttal生成*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![Gradio](https://img.shields.io/badge/UI-Gradio-orange)](https://gradio.app)
[![Stars](https://img.shields.io/github/stars/chenyi6758-source/PaperScholar?style=social)](https://github.com/chenyi6758-source/PaperScholar)

[English](./README.md) | [中文](./README.zh-CN.md)

</div>

-----

## PaperScholar 是什么？

PaperScholar 是一个专为中文科研人员和学生设计的 AI 学术写作工具链。

**它不是帮你”一键生成论文”，而是像真正的导师一样帮你学会学术写作。**

核心理念：每个论断必须有证据支撑。先定结构，再写句子。中文用户值得有母语支持。

-----

## 核心功能

|功能              |说明                                                          |
|----------------|------------------------------------------------------------|
|👨‍🏫 **导师模式**      |模拟严格导师和顶会审稿人（NeurIPS/CVPR/ACL/Nature），给出评分表和具体修改指令，所有分析用中文输出|
|✨ **去AI腔**      |检测并消除AI生成文本的典型特征：空洞开场白、过度连接词、无数据的绝对表达                       |
|💡 **创新点检测**     |区分真正创新与”方法迁移”、“调参”、“换数据集”等低创新情况                             |
|📝 **Rebuttal生成**|逐条回应Reviewer意见，中文分析+英文正式回复                                  |
|📚 **证据库约束**     |每个论断必须链接到来源，才能出现在论文正文中                                      |
|📐 **蓝图优先**      |先规划章节结构和写作动机，再生成正文                                          |
|🔬 **论文拆解**      |反向工程顶会论文，提取论证骨架和写作套路                                        |
|🌐 **Web界面**     |Gradio可视化界面，无需编程，打开浏览器即用                                    |
|🤖 **多模型支持**     |支持8+主流AI提供商，按任务类型智能路由                                       |

-----

## 支持的AI模型

|提供商             |默认模型                    |适合场景      |
|----------------|------------------------|----------|
|**DeepSeek** ⭐推荐|deepseek-chat           |通用，性价比极高  |
|**通义千问**        |qwen-max                |中文处理、长文档  |
|**智谱GLM**       |glm-4                   |中文学术写作    |
|**Anthropic**   |claude-sonnet-4-20250514|改写、审计     |
|**OpenAI**      |gpt-4o                  |英文润色      |
|**月之暗面**        |moonshot-v1-128k        |超长PDF处理   |
|**豆包**          |doubao-pro-32k          |快速响应      |
|**自定义**         |任意                      |OpenAI兼容接口|

-----

## 快速开始

### 方式一：Web界面（推荐新手）

```bash
git clone https://github.com/chenyi6758-source/PaperScholar.git
cd PaperScholar
pip install openai gradio
python src/web_ui.py
# 浏览器打开 http://localhost:7860
```

在浏览器里粘贴你的 API Key，无需配置文件，直接使用。

### 方式二：命令行（完整工作流）

```bash
pip install openai

# 复制并编辑配置文件
cp paperscholar_config.example.json paperscholar_config.json
# 填入你的 API Key

# 从素材构建论文
python src/orchestrator.py \
  --config paperscholar_config.json \
  --inputs 我的笔记.txt \
  --output 论文输出/

# 改写现有稿件
python src/orchestrator.py \
  --config paperscholar_config.json \
  --inputs 初稿.txt \
  --output 论文输出/

# 单独运行导师审查
python src/orchestrator.py \
  --config paperscholar_config.json \
  --inputs 初稿.txt \
  --skill tutor

# 生成Rebuttal
python src/orchestrator.py \
  --config paperscholar_config.json \
  --skill rebuttal \
  --reviewer "Reviewer 2: The novelty is insufficient."
```

-----

## 工作流程

```
[输入：素材 / 初稿]
         │
    ┌────▼────┐
    │ 读取配置 │  验证配置，收集输入文件
    └────┬────┘
         │
    ┌────▼──────┐
    │ 构建证据库 │  每个论断 → 证据ID → 来源
    └────┬──────┘
         │
    ┌────▼──────┐
    │ 生成蓝图  │  章节结构 + 写作动机记录
    └────┬──────┘
         │
    ┌────▼──────────┐
    │ 生成或改写正文 │  证据库强制约束
    └────┬──────────┘
         │
    ┌────▼────────────────────────┐
    │ 后处理（并行）               │
    │  • 导师模式审查              │
    │  • AI腔检测与去除            │
    │  • 创新点检测                │
    │  • 最终审计                  │
    │  • 翻译包（中英双语）         │
    └────┬────────────────────────┘
         │
    [输出文件]
```

-----

## 输出文件说明

```
paperscholar_output/
  evidence_bank.md          # 证据库（每条论断有来源）
  section_blueprint.md      # 章节蓝图 + 写作动机
  draft_full.md             # 完整论文草稿
  tutor_review.md           # ⭐ 导师审查报告（含评分表）
  ai_tone_check.md          # AI腔检测报告
  innovation_check.md       # 创新点评估报告
  revision_audit.md         # 最终审计报告
  rebuttal.md               # Rebuttal草稿（如适用）
  translation_package.md    # 中英双语对照（如开启）
```

-----

## 支持的论文场景

|场景           |用途                 |
|-------------|-------------------|
|`journal`    |SCI/EI期刊论文         |
|`conference` |NeurIPS/CVPR/ACL等顶会|
|`thesis`     |中文硕士/博士学位论文        |
|`proposal`   |国自然申请书/开题报告        |
|`competition`|数学建模竞赛论文           |
|`report`     |技术报告/研究报告          |

-----

## 导师风格

|风格       |模拟对象                  |
|---------|----------------------|
|`strict` |严格中文导师（通用）            |
|`neurips`|NeurIPS Area Chair    |
|`cvpr`   |CVPR审稿人               |
|`acl`    |ACL审稿人                |
|`iclr`   |ICLR审稿人               |
|`nature` |Nature/Science审稿人（最严苛）|

-----

## 配置文件说明

```json
{
  "provider": "deepseek",
  "model": "deepseek-chat",
  "api_key": "你的API Key",
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

## 参与贡献

欢迎 PR！特别欢迎：

- 新的导师风格（不同领域审稿人）
- 新的中文场景模板
- 提示词优化（在 `src/prompts/prompts.py` 中修改）

-----

## License

MIT License — 自由使用、修改、分发