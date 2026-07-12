# 输出示例

## 明日计划输出（自然语言）

```
📅 明日计划（2024-07-15）

🎯 新学任务
- 项目风险管理：风险识别与定性分析 — 60 分钟，高优先级
- 项目质量管理：质量规划工具与技术 — 40 分钟，中优先级

🔄 复习任务
- 项目整合管理（第 4 章）— 第 7 天复习，10 分钟
- 项目范围管理（第 5 章）— 第 2 天复习，10 分钟

⚠️ 弱项提醒
- 项目成本管理：失分率 45%，建议重做 10 道挣值管理典型题

📊 整体进度：已完成 12/60 天，落后 1.5 天，建议周末补 2 小时
```

## 计划 JSON 结构示例

```json
{
  "exam": "PMP",
  "deadline": "2024-09-30",
  "days_remaining": 77,
  "daily_hours": 2.0,
  "current_level": "intermediate",
  "total_plan_hours": 154.0,
  "plan": [
    {
      "day": 1,
      "date": "2024-07-15",
      "exam": "PMP",
      "subject": "项目整合管理",
      "task": "学习 项目整合管理 模块",
      "duration": 45,
      "priority": "high",
      "status": "planned",
      "review": false
    },
    {
      "day": 2,
      "date": "2024-07-16",
      "exam": "PMP",
      "subject": "项目整合管理",
      "task": "艾宾浩斯复习：项目整合管理",
      "duration": 10,
      "priority": "medium",
      "status": "planned",
      "review": true,
      "review_stage": 1,
      "note": "第 1 天遗忘曲线复习点"
    }
  ]
}
```

## 弱项分析 JSON 示例

```json
{
  "top_weak_subjects": [
    {
      "subject": "项目成本管理",
      "loss_rate": 0.45,
      "average_score": 55.0,
      "suggestion": "重点复习"
    }
  ],
  "top_weak_tags": [
    {
      "tag": "挣值管理",
      "wrong_rate": 0.60,
      "suggestion": "专项训练"
    }
  ],
  "action_plan": [
    "项目成本管理: 重点复习"
  ]
}
```
