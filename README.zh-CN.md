<div align="center">

# 🎓 PaperScholar

**统一学术写作 AI 工作流**

*集成 PaperForge × PaperSpine × PaperMind 三大引擎的最强版本*

[![CI](https://github.com/your-username/PaperScholar/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/PaperScholar/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![Stars](https://img.shields.io/github/stars/your-username/PaperScholar?style=social)](https://github.com/your-username/PaperScholar)

[English](./README.md) | **中文**

</div>

---

## 为什么选择 PaperScholar？

三个开源项目的最强特性合而为一：

| 来源 | 最强特性 | 如何集成 |
|------|---------|---------|
| **PaperForge** | 证据链约束 — 每个Claim必须有来源才能出现在论文中 | `CitationSkill` + `AuditSkill` |
| **PaperSpine** | 蓝图优先工作流 — 先定结构再写句子 | `BlueprintSkill` + `BuildSkill` |
| **PaperMind** | 中文科研生态 — 导师模式、去AI腔、Rebuttal生成 | `TutorSkill` + `AiToneSkill` + `RebuttalSkill` |

---

## 功能全景

| 功能 | PaperScholar | PaperForge | PaperSpine | PaperMind |
|------|:---:|:---:|:---:|:---:|
| 证据库（Claim→来源强制绑定）| ✅ | ✅ | — | — |
| 蓝图优先写作流程 | ✅ | — | ✅ | — |
| 写作动机矩阵 | ✅ | ✅ | ✅ | — |
| 导师/审稿人模拟 | ✅ | — | — | ✅ |
| AI腔检测与去除 | ✅ | — | — | ✅ |
| 创新性检测 | ✅ | — | — | ✅ |
| Rebuttal生成 | ✅ | — | — | ✅ |
| 论文结构拆解 | ✅ | — | — | ✅ |
| 中文专属场景模板 | ✅ | — | — | ✅ |
| Web界面（无需编程）| ✅ | — | — | ✅ |
| 最终审计vs证据库 | ✅ | ✅ | — | — |
| 8+ 模型支持 | ✅ | ✅ | ✅ | ✅ |
| 任务驱动智能路由 | ✅ | — | — | ✅ |
| 中英双语翻译包 | ✅ | ✅ | — | ✅ |

---

## 支持的AI提供商

| 提供商 | 默认模型 | 最适合 | 获取Key |
|--------|---------|--------|---------|
| **DeepSeek** ⭐推荐 | deepseek-chat | 通用、性价比最高 | [deepseek.com](https://deepseek.com) |
| **Anthropic** | claude-sonnet-4 | LaTeX审计、逻辑改写 | [anthropic.com](https://anthropic.com) |
| **OpenAI** | gpt-4o | 英文润色、通用写作 | [openai.com](https://openai.com) |
| **通义千问** | qwen-max | 中文、长文档 | [aliyun.com](https://dashscope.aliyuncs.com) |
| **智谱GLM** | glm-4 | 中文学术写作 | [bigmodel.cn](https://bigmodel.cn) |
| **月之暗面** | moonshot-v1-128k | 超长PDF | [moonshot.cn](https://moonshot.cn) |
| **豆包** | doubao-pro-32k | 快速响应 | [volcengine.com](https://volcengine.com) |
| **自定义** | 任意 | 任何OpenAI兼容接口 | — |

---

## 快速开始

### 方式一：Web界面（推荐新手，无需写代码）

```bash
git clone https://github.com/your-username/PaperScholar.git
cd PaperScholar
pip install openai gradio
python src/web_ui.py
# 打开浏览器 http://localhost:7860
```

Web界面包含8大功能标签页：
- 👨‍🏫 导师审查（多风格）
- ✨ 去AI腔
- 🖊️ 学术润色（中式英语矫正）
- 💡 创新性检测
- 📝 Rebuttal生成
- 🏦 证据库构建
- 🗺️ 写作蓝图
- 🔬 论文拆解

### 方式二：命令行（完整工作流）

```bash
pip install openai

cp paperscholar_config.example.json paperscholar_config.json
# 编辑配置文件，填入API Key

# 从素材构建论文
python src/orchestrator.py \
  --config paperscholar_config.json \
  --inputs 我的笔记.txt 参考文献.txt \
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

# 去AI腔检查
python src/orchestrator.py \
  --config paperscholar_config.json \
  --inputs 初稿.txt \
  --skill ai_tone
```

### 方式三：Claude Code / Codex 技能

```bash
# macOS / Linux
chmod +x install.sh && ./install.sh

# Windows
.\install.ps1
```

安装后在 Claude Code 输入 `/paperscholar`，在 Codex 输入 `$paperscholar`。

---

## 完整工作流

```
[原始材料 / 初稿]
        │
   ┌────▼────┐
   │  收录   │  验证配置，收集文件
   └────┬────┘
        │
   ┌────▼──────┐
   │  场景研究  │  学习目标期刊/会议规范（在写作前）
   └────┬──────┘
        │
   ┌────▼──────────┐
   │  证据库构建    │  提取每个Claim → 分配证据ID → 记录来源
   │  (PaperForge) │  铁律：无来源的Claim不能出现
   └────┬──────────┘
        │
   ┌────▼──────┐
   │  写作蓝图  │  各章节结构 + 每节写作动机
   └────┬──────┘
        │
   ┌────▼────────────────────────┐
   │  构建 or 改写                │
   │  (每个Claim引用证据ID)       │
   └────┬────────────────────────┘
        │
   ┌────▼────────────────────────────────┐
   │  后处理（并行执行）                   │
   │  • 导师审查（评分表 + 修改指令）      │
   │  • AI腔检测与去除                   │
   │  • 创新性评级                       │
   │  • 最终审计（对照证据库）            │
   │  • 翻译包（如开启）                 │
   └────┬────────────────────────────────┘
        │
   [输出文件]
```

---

## 输出文件说明

```
论文输出/
  paperscholar_config.json      # 本次配置（不含API Key）
  research_dossier.md           # 场景画像 + 材料分析
  evidence_bank.md              # 证据库（每个Claim有ID和来源）
  section_blueprint.md          # 章节蓝图 + 每节写作动机
  draft_full.md                 # 完整论文草稿
  writing_rationale_matrix.json # 每章写法的决策理由
  tutor_review.md               # ⭐ 导师审查报告（含评分表）
  ai_tone_check.md              # AI腔检测与修改建议
  innovation_check.md           # 创新性评级报告
  revision_audit.md             # 最终审计（对照证据库）
  translation_package.md        # 中英双语输出（如开启）
  rebuttal.md                   # Rebuttal草稿（如申请）
```

最重要的两个文件：
- **`tutor_review.md`** — 告诉你哪里有问题，评分精确到每个维度
- **`evidence_bank.md`** — 确保论文中每个Claim都有真实来源

---

## 中文特色场景

| 场景 | 说明 | 关键要求 |
|------|------|---------|
| `thesis` | 硕士/博士学位论文 | GB/T 7714引用格式，中英双摘要，章节用中文数字 |
| `proposal` | 国自然/开题报告 | 突出创新性和可行性，研究计划具体可量化 |
| `competition` | 数学建模竞赛 | 摘要自包含，灵敏度分析必须有，代码附录 |

---

## 导师风格说明

| 风格 | 模拟对象 | 适用场景 |
|------|---------|---------|
| `strict` | 严格中文科研导师 | 通用论文审查 |
| `neurips` | NeurIPS Area Chair | 机器学习论文 |
| `cvpr` | CVPR审稿人 | 计算机视觉 |
| `acl` | ACL审稿人 | 自然语言处理 |
| `iclr` | ICLR审稿人 | 深度学习 |
| `nature` | Nature/Science审稿人 | 高影响力基础研究 |

---

## 配置文件说明

```json
{
  "provider": "deepseek",
  "model": "deepseek-chat",
  "api_key": "你的API Key",
  "scene": "journal",
  "workflow": "build",
  "research_depth": "flash",
  "output_language": "Chinese",
  "translation_package": false,
  "tutor_style": "strict",
  "cn_scene": ""
}
```

| 字段 | 可选值 | 说明 |
|------|--------|------|
| `provider` | `deepseek/anthropic/openai/qwen/glm/moonshot/doubao/custom` | AI提供商 |
| `scene` | `journal/conference/report/competition/thesis/proposal` | 论文类型 |
| `workflow` | `build`（从素材构建）/ `rewrite`（改写） | 工作流模式 |
| `research_depth` | `flash`（快速）/ `pro`（深入） | 场景研究深度 |
| `output_language` | `Chinese` / `English` | 草稿语言 |
| `translation_package` | `true/false` | 是否生成双语翻译包 |
| `tutor_style` | `strict/neurips/cvpr/acl/iclr/nature` | 导师/审稿人风格 |
| `cn_scene` | `thesis/proposal/competition`（留空则用通用模板）| 中文专属场景 |

---

## 开发贡献

```bash
# 运行测试
pip install pytest
pytest tests/ -v

# 参与贡献
# 添加新导师风格 → 编辑 src/prompts/prompts.py 的 TUTOR_MAP
# 添加新中文场景 → 编辑 src/prompts/prompts.py 的 CN_TEMPLATES
# 优化提示词 → 所有提示词统一在 src/prompts/prompts.py
```

欢迎 PR！特别欢迎：
- 新的导师风格（不同领域审稿风格）
- 新的中文场景模板
- 提示词优化

---

## 致谢

PaperScholar 建立在三个开源项目的基础上：

- **[PaperForge](https://github.com/your-username/PaperForge)** — 证据链约束 + 场景审计
- **[PaperSpine](https://github.com/WUBING2023/PaperSpine)** — 蓝图优先工作流
- **[PaperMind](https://github.com/your-username/PaperMind)** — 中文科研生态 + 导师模式

---

## 路线图

- [x] 导师模式（6种风格）
- [x] 去AI腔检测
- [x] 创新性检测
- [x] Rebuttal生成
- [x] 证据库强制约束
- [x] 蓝图优先工作流
- [x] Web界面
- [x] 8+ 模型支持 + 任务路由
- [x] 中文场景模板（学位论文/国自然/数学建模）
- [ ] 引文图谱可视化
- [ ] Semantic Scholar API（自动验证引用真实性）
- [ ] LaTeX实时编译检查
- [ ] VS Code插件
- [ ] PDF/Word直接输入处理

---

## License

MIT License — 自由使用、修改、分发。详见 [LICENSE](LICENSE)。
