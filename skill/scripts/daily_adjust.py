import argparse
import json
from datetime import datetime, timedelta


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def adjust_plan(plan_data, feedback):
    plan = plan_data["plan"]
    completed = feedback.get("completed", 1.0)
    mastered = set(feedback.get("mastered_topics", []))
    struggling = set(feedback.get("struggling_topics", []))

    today = datetime.today().date()

    for task in plan:
        task_date = datetime.strptime(task["date"], "%Y-%m-%d").date()
        if task_date <= today:
            continue

        # 完成率偏低：后续任务减量
        if completed < 0.6:
            task["duration"] = round(task["duration"] * 0.8, 0)
            task["note"] = (task.get("note", "") + " 任务减量20%").strip()

        # 未掌握主题：提前并升高优先级
        if task["subject"] in struggling:
            task["priority"] = "high"
            task["note"] = (task.get("note", "") + " 弱项优先").strip()

        # 已掌握主题：减少出现频次，但保留复习点
        if task["subject"] in mastered and not task.get("review"):
            task["duration"] = max(15, round(task["duration"] * 0.6, 0))
            task["note"] = (task.get("note", "") + " 已掌握，压缩新学").strip()

    # 若存在未掌握主题，从今天起连续 3 天插入专项任务
    if struggling:
        for offset in range(1, 4):
            for subject in struggling:
                plan.append({
                    "day": offset,
                    "date": (today + timedelta(days=offset)).strftime("%Y-%m-%d"),
                    "exam": plan_data["exam"],
                    "subject": subject,
                    "task": f"专项突破：{subject} 典型题/错题重做",
                    "duration": 30,
                    "priority": "high",
                    "status": "planned",
                    "review": False,
                    "note": "基于昨日反馈插入弱项训练"
                })

    plan.sort(key=lambda x: (x["date"], x["priority"] != "high"))
    plan_data["plan"] = plan
    plan_data["last_feedback"] = feedback
    return plan_data


def main():
    parser = argparse.ArgumentParser(description="根据每日反馈动态调整复习计划")
    parser.add_argument("--plan", required=True, help="基线计划 JSON 路径")
    parser.add_argument("--feedback", required=True, help="反馈 JSON 路径")
    parser.add_argument("--output", required=True, help="输出调整后计划 JSON 路径")
    args = parser.parse_args()

    plan_data = load_json(args.plan)
    feedback = load_json(args.feedback)
    adjusted = adjust_plan(plan_data, feedback)
    save_json(args.output, adjusted)

    print("已根据反馈调整计划。")
    print(f"完成率: {feedback.get('completed', 1.0):.0%}")
    print(f"弱项: {', '.join(feedback.get('struggling_topics', [])) or '无'}")


if __name__ == "__main__":
    main()
