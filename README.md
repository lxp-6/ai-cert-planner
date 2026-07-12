# AI 考证复习规划师

一个将 AI 作为"私人教练"的考证复习规划 Skill。根据考试目标、当前基础、每天可用时间，生成并动态调整个性化复习计划。

## 选题背景

传统复习计划通常是固定表格：提前排好每天要学什么，一旦某天没完成、某个知识点没听懂，后续计划就会全部乱掉。考生常见问题：

- 网上经验贴不适合自己的基础和时间。
- 计划赶不上变化，昨天没完成的任务不会自动后移。
- 会的知识点反复学，不会的知识点一直没练。

AI 考证复习规划师通过自然语言理解考生现状，持续读取每日反馈，动态调整后续计划，并结合艾宾浩斯遗忘曲线和模考弱项分析，让计划真正跟着人走。

## 核心功能

| 功能 | 说明 |
|------|------|
| **基线计划生成** | 根据考试日期、每日可用时间、科目权重生成基线日计划 |
| **每日反馈调整** | 完成率低自动减量，已掌握科目压缩，未掌握科目插入专项训练 |
| **艾宾浩斯复习** | 在新学知识后第 1、2、4、7、15 天自动插入复习点 |
| **弱项分析** | 从模考分数和错题标签识别失分率最高的科目和知识点 |

## 仓库结构

```
ai-cert-planner/
├── skill/                       # Skill 文件
│   ├── SKILL.md                 # 技能定义文件（含 yaml 前端配置）
│   ├── scripts/                 # 核心脚本
│   │   ├── plan_generator.py        # 生成基线计划
│   │   ├── daily_adjust.py          # 根据反馈调整计划
│   │   ├── ebbinghaus_review.py     # 插入艾宾浩斯复习任务
│   │   └── weak_point_analyzer.py   # 分析模考弱项
│   └── references/              # 参考文档
│       ├── input-schema.md          # 输入字段说明
│       ├── output-example.md        # 输出示例
│       └── ebbinghaus-curve.md      # 艾宾浩斯遗忘曲线参考
├── data/                        # 测试数据
│   ├── sample_inputs.json           # 考生基础信息样本
│   ├── daily_feedback.json          # 每日反馈样本
│   └── mock_scores.json             # 模考分数样本
├── tests/                       # 测试记录与输出
│   ├── test_record.md               # 测试记录
│   ├── baseline_plan.json           # 基线计划输出
│   ├── adjusted_plan.json           # 调整后的计划输出
│   ├── plan_with_review.json        # 含复习任务的计划输出
│   └── weak_points.json             # 弱项分析输出
├── iteration/                   # 迭代升级说明
│   └── iteration_log.md             # 按 5 步迭代法记录的迭代过程
└── README.md                    # 项目说明
```

## 使用方式

### 1. 作为 WorkBuddy Skill 使用

将 `skill/` 目录复制到 WorkBuddy 技能目录即可：

```bash
# 项目级（当前工作空间）
cp -r skill/ <workspace>/.workbuddy/skills/ai-cert-planner/

# 用户级（跨项目使用）
cp -r skill/ ~/.workbuddy/skills/ai-cert-planner/
```

触发词：

- 帮我规划考证
- 生成复习计划
- 调整学习计划
- 分析模考弱项

### 2. 直接运行脚本

所有脚本仅依赖 Python 标准库，无需安装第三方包。

```bash
# 1. 生成基线计划
python skill/scripts/plan_generator.py --input data/sample_inputs.json --output tests/baseline_plan.json

# 2. 根据反馈调整
python skill/scripts/daily_adjust.py --plan tests/baseline_plan.json --feedback data/daily_feedback.json --output tests/adjusted_plan.json

# 3. 插入艾宾浩斯复习
python skill/scripts/ebbinghaus_review.py --plan tests/adjusted_plan.json --output tests/plan_with_review.json

# 4. 分析模考弱项
python skill/scripts/weak_point_analyzer.py --scores data/mock_scores.json --output tests/weak_points.json
```

## 输入示例

`data/sample_inputs.json`：

```json
{
  "exam": "PMP项目管理认证",
  "deadline": "2026-09-30",
  "daily_hours": 2.0,
  "current_level": "intermediate",
  "subjects": [
    {"name": "项目整合管理", "weight": 0.15},
    {"name": "项目范围管理", "weight": 0.12},
    {"name": "项目进度管理", "weight": 0.15},
    {"name": "项目成本管理", "weight": 0.10},
    {"name": "项目质量管理", "weight": 0.10}
  ]
}
```

## 输出示例

AI 代理读取脚本输出后，会用自然语言生成如下明日计划：

```
📅 明日计划（2026-07-13）

🎯 新学任务
- 项目整合管理：学习 项目整合管理 模块 — 60 分钟，中优先级
- 项目进度管理：学习 项目进度管理 模块 — 60 分钟，中优先级

🔄 复习任务
- 项目风险管理：艾宾浩斯复习 — 10 分钟，第 1 天复习点

⚠️ 弱项提醒
- 项目成本管理：失分率 42%，建议重做 10 道挣值管理典型题
- 项目风险管理：失分率 39%，建议专项训练风险应对策略

📊 整体进度：第 1/80 天，剩余 79 天
```

## 测试记录

详见 `tests/test_record.md`。

## 迭代记录

详见 `iteration/iteration_log.md`，记录了至少 2 次按 5 步迭代法进行的优化。

## 技术约束

- 仅使用 Python 标准库（`argparse`, `json`, `datetime`, `collections`）。
- 无第三方依赖、无 API 调用、无网络请求。
- 每个脚本代码简洁，核心逻辑聚焦单一职责。

## 许可证

MIT
