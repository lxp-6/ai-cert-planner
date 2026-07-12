# 测试记录

## 测试环境

- 操作系统：Windows 11（win32）
- Python 版本：3.13.12（managed）
- 运行路径：`C:\Users\林秀萍lxp\WorkBuddy\2026-07-12-10-06-44\ai-cert-planner`
- 测试日期：2026-07-12

## 测试目标

验证 AI 考证复习规划师 Skill 的核心脚本链能否正确运行：

1. 从考生输入生成基线计划
2. 根据每日反馈动态调整计划
3. 按艾宾浩斯遗忘曲线插入复习任务
4. 从模考分数分析弱项并给出建议

## 测试数据

- `data/sample_inputs.json`：PMP 项目管理认证考试的考生基础信息
- `data/daily_feedback.json`：昨日完成率 50%，成本/风险管理未掌握
- `data/mock_scores.json`：6 次模拟考试成绩及错题标签

## 测试步骤与执行结果

### 步骤 1：生成基线计划

```bash
python skill/scripts/plan_generator.py --input data/sample_inputs.json --output tests/baseline_plan.json
```

**输出：**

```
已生成 PMP项目管理认证 复习计划，共 80 天，162 个任务。
```

**结果说明：**

- 考试日期：2026-09-30
- 剩余天数：80 天
- 每日可用时间：2.0 小时
- 总计划时长：160.0 小时
- 计划按天贪婪填充，每天约 2 个 60 分钟学习块，符合 daily_hours 限制。

基线计划前两条任务示例：

```json
{
  "day": 1,
  "date": "2026-07-12",
  "exam": "PMP项目管理认证",
  "subject": "项目整合管理",
  "task": "学习 项目整合管理 模块",
  "duration": 60,
  "priority": "medium",
  "status": "planned",
  "review": false
}
```

### 步骤 2：根据每日反馈调整计划

```bash
python skill/scripts/daily_adjust.py --plan tests/baseline_plan.json --feedback data/daily_feedback.json --output tests/adjusted_plan.json
```

**输出：**

```
已根据反馈调整计划。
完成率: 50%
弱项: 项目成本管理, 项目风险管理
```

**结果说明：**

- 完成率低于 60%，后续任务时长压缩 20%。
- `项目成本管理` 和 `项目风险管理` 被标记为弱项，后续 3 天各插入 30 分钟专项突破任务。
- 已掌握的 `项目质量管理` 新学任务时长压缩。

### 步骤 3：插入艾宾浩斯复习任务

```bash
python skill/scripts/ebbinghaus_review.py --plan tests/adjusted_plan.json --output tests/plan_with_review.json
```

**输出：**

```
已插入 50 个艾宾浩斯复习任务。
```

**结果说明：**

- 为每个科目的首次学习日期后推 1、2、4、7、15 天插入复习任务。
- 超过考试日期或早于今天的复习点被自动跳过。

### 步骤 4：分析模考弱项

```bash
python skill/scripts/weak_point_analyzer.py --scores data/mock_scores.json --output tests/weak_points.json
```

**输出：**

```
弱项分析完成。
- 项目成本管理 失分率 42%
- 项目风险管理 失分率 39%
- 项目进度管理 失分率 22%
```

**结果说明：**

- 识别出失分率最高的科目为 `项目成本管理`（42%）和 `项目风险管理`（39%）。
- 错题标签中 `挣值管理`、`成本估算`、`储备分析`  wrong_rate 均为 1.0，建议专项训练。

## 测试结论

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 基线计划生成 | 通过 | 任务按天分块，时长符合 daily_hours |
| 每日反馈调整 | 通过 | 弱项插入专项任务，已掌握科目压缩 |
| 艾宾浩斯复习 | 通过 | 自动插入 50 个复习点，考后任务已过滤 |
| 弱项分析 | 通过 | 科目和标签失分率正确排序 |
| 纯 Python 标准库 | 通过 | 无第三方依赖 |

## 测试输出文件

- `tests/baseline_plan.json`：基线计划
- `tests/adjusted_plan.json`：反馈调整后的计划
- `tests/plan_with_review.json`：含复习任务的计划
- `tests/weak_points.json`：弱项分析结果
