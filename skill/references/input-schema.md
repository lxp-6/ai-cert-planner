# 输入格式说明

`AI 考证复习规划师` Skill 处理的输入必须是一个 JSON 对象。字段分为两类：

- **核心字段**：缺少任意一项时，AI 会询问用户补全，不会直接生成计划。
- **可选字段**：有则增强计划，无则跳过相关功能。

## 核心字段

```json
{
  "exam": "PMP",
  "deadline": "2024-09-30",
  "daily_hours": 2.0,
  "current_level": "intermediate",
  "subjects": [
    {"name": "项目整合管理", "weight": 0.15},
    {"name": "项目范围管理", "weight": 0.12},
    {"name": "项目进度管理", "weight": 0.15},
    {"name": "项目成本管理", "weight": 0.10},
    {"name": "项目质量管理", "weight": 0.10},
    {"name": "项目资源管理", "weight": 0.08},
    {"name": "项目沟通管理", "weight": 0.08},
    {"name": "项目风险管理", "weight": 0.12},
    {"name": "项目采购管理", "weight": 0.05},
    {"name": "项目相关方管理", "weight": 0.05}
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `exam` | string | 考试名称，决定输出文案中的称呼 |
| `deadline` | string | 考试日期，格式 `YYYY-MM-DD` |
| `daily_hours` | number | 每天可用于复习的小时数，建议 0.5 ~ 8 |
| `current_level` | string | 基础水平：`beginner` / `intermediate` / `advanced` |
| `subjects` | array | 科目/知识模块，每项包含 `name` 和 `weight`（0-1） |

## 可选字段

### 每日反馈

```json
{
  "completed": 0.7,
  "mastered_topics": ["项目质量管理"],
  "struggling_topics": ["项目成本管理"]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `completed` | number | 昨日计划完成率，0-1 |
| `mastered_topics` | array | 已经掌握的科目/主题名 |
| `struggling_topics` | array | 未掌握或模糊的科目/主题名 |

### 模考分数

```json
[
  {
    "subject": "项目成本管理",
    "score": 55,
    "total": 100,
    "wrong_tags": ["挣值管理", "成本估算"]
  }
]
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `subject` | string | 科目名 |
| `score` | number | 实际得分 |
| `total` | number | 满分 |
| `wrong_tags` | array | 错题标签，用于细化弱项 |
