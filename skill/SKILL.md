---
name: ai-cert-planner
description: AI考证复习规划师。根据考试目标、当前基础、每天可用时间，生成并动态调整个性化复习计划；支持每日反馈纠偏、艾宾浩斯复习调度、模考弱项分析。触发词：帮我规划考证、生成复习计划、调整学习计划、分析模考弱项。
created: 2026-07-12
version: 1.0.0
tags:
  - study
  - exam
  - planner
  - ebbinghaus
  - ai-coach
agent_created: true
disable: false
---

# AI 考证复习规划师

一句话定位：把「AI 私人教练」嵌入备考流程。不是输出一张固定表格，而是根据你的基础、时间、遗忘曲线和每日反馈，持续生成明天该学什么、复习什么、重点攻哪块。

## 核心能力（AI 不可替代的部分）

- **从自然语言里提取结构**：用户说"我 9 月考 PMP，每天 2 小时，项目管理基础一般"，AI 自动解析出考试、截止日期、每日时长、基础水平、科目范围。
- **动态纠偏**：用户每天反馈"今天只完成 70%，风险管理听得懂，挣值管理没懂"，AI 自动重排后续计划，把没懂的知识点提前、压缩已掌握内容。
- **遗忘曲线驱动的复习**：不是按顺序再过一遍，而是根据艾宾浩斯曲线计算每个知识点在哪些天必须复习，避免"会的反复学、不会的没练"。
- **弱项诊断**：从模考成绩或错题分布里识别失分原因，调整复习重心到高频失分点。

## 输入字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| exam | string | 是 | 考试名称，如 "PMP"、"系统架构设计师"、"考研数学一" |
| deadline | string | 是 | 考试日期，格式 `YYYY-MM-DD` |
| daily_hours | float | 是 | 每天可用于复习的小时数 |
| current_level | string | 是 | 基础水平：`beginner` / `intermediate` / `advanced` |
| subjects | list | 是 | 科目/知识模块列表，每个元素含 `name` 和 `weight`（分值权重 0-1） |
| user_id | string | 否 | 用户标识，用于持久化学习档案 |
| feedback | object | 否 | 昨日反馈：`completed`（完成率 0-1）、`mastered_topics`（已掌握）、`struggling_topics`（未掌握） |
| mock_scores | list | 否 | 模考分数记录，每个元素含 `subject`、`score`、`total`、`wrong_tags` |

## 使用流程

### 第一步：理解用户现状

读取用户输入，识别缺失字段。如果缺少 exam、deadline、daily_hours、current_level、subjects 中任意一项，先询问补全，不要直接生成计划。

将用户输入写入临时文件 `workspace/ai-cert-planner/state.json`，作为后续步骤的输入。

### 第二步：生成基线计划

调用 `scripts/plan_generator.py`，传入 `state.json`，生成基线计划 `baseline_plan.json`：

```bash
python scripts/plan_generator.py --input state.json --output baseline_plan.json
```

脚本会基于考试截止日期反推总天数，按科目权重、基础水平、每日可用时间分配每日学习任务。基础水平越低，给该科目分配的前置时间越多；权重越高，分配的总时长越多。

### 第三步：处理每日反馈（如有）

如果用户提供了昨日反馈，调用 `scripts/daily_adjust.py`：

```bash
python scripts/daily_adjust.py --plan baseline_plan.json --feedback feedback.json --output adjusted_plan.json
```

脚本规则：

- `completed` < 0.6：降低后续 3 天任务量 20%，并标红未掌握主题。
- `struggling_topics` 中的主题：在后续 3 天内插入专项复习，优先安排。
- `mastered_topics` 中的主题：减少其后续出现频次，但保留艾宾浩斯复习点。

### 第四步：安排复习与弱项强化

调用 `scripts/ebbinghaus_review.py` 和 `scripts/weak_point_analyzer.py`：

```bash
python scripts/ebbinghaus_review.py --plan adjusted_plan.json --output plan_with_review.json
python scripts/weak_point_analyzer.py --scores mock_scores.json --output weak_points.json
```

- `ebbinghaus_review.py` 在每个新学主题的后面第 1、2、4、7、15 天插入 5-10 分钟快速复习。
- `weak_point_analyzer.py` 从模考分数和错题标签中输出失分率最高的 3 个主题及建议复习动作。

### 第五步：输出明日计划与整体状态

读取 `plan_with_review.json` 和 `weak_points.json`，用自然语言输出：

1. 明日学习任务（含科目、章节、建议时长、优先级）。
2. 明日复习任务（艾宾浩斯触发）。
3. 当前整体进度与风险预警（如进度落后 X 天）。
4. 弱项建议（如果提供了模考数据）。

输出格式示例：

```
📅 明日计划（2024-07-15）

🎯 新学任务
- 项目管理：风险管理（第 5 章） — 60 分钟，高优先级
- 质量管理：质量规划工具 — 40 分钟，中优先级

🔄 复习任务
- 整合管理（第 4 章）— 第 7 天复习，10 分钟
- 范围管理（第 5 章）— 第 2 天复习，10 分钟

⚠️ 弱项提醒
- 挣值管理（EVM）：失分率 45%，建议重做 10 道典型题

📊 整体进度：已完成 12/60 天，落后 1.5 天，建议周末补 2 小时
```

## 边界条件

- 当考试日期距今不足 7 天时，只生成冲刺计划，不再插入新学内容，重点做复习和错题。
- 当 `daily_hours` < 0.5 小时时，提示用户时间不足以完成目标，建议调整考试日期或优先级。
- 当某个主题连续 3 天出现在 `struggling_topics` 中，标记为"顽固弱项"，建议换学习方式或寻求帮助。
- 不替用户报名考试、不获取考试真题，只提供复习计划。

## 失败处理

- 脚本返回非 0：读取 stderr，向用户解释错误原因，并给出可执行的修正建议（如补全 subjects 字段）。
- 输入日期格式错误：提示使用 `YYYY-MM-DD`，并给出示例。
- 没有模考数据：跳过弱项分析，只输出计划与复习任务。
